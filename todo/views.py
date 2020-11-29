from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, reverse
from django.views import View
from . models import Task
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):
    def get(self, request):
        return render(request, 'todo/index.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class SignInView(View):
    def get(self, request):
        return render(request, 'todo/signin.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username == '' or password == '':
            return render(request, 'todo/signin_error.html', context={'warning':'Invalid data! Fields "Username" and "Password" must not be empty!'})
        user = authenticate(username=username, password=password)
        if User.objects.filter(username=username).exists() and not user:
            return render(request, 'todo/signin.html', context={'user': user, 'warning':'Password is incorrect!'})
        if not user:
            return render(request, 'todo/signin.html', context={'user': user, 'warning':'Username does not exist!'})
            # return self.get(request)
        login(request, user)
        return redirect(reverse('userpage', kwargs={'username':username}))

class SignUpView(View):
    def get(self, request):
        return render(request, 'todo/signup.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        check_user = User.objects.filter(username=username).exists()
        if check_user:
            return render(request, 'todo/signup.html', context={'check_user': check_user, 'warning':'This username already exists!'})
        try:
            user = User.objects.create_user(username = username, password=password)
            login(request, user)
            return redirect(reverse('index'))
        except ValueError:
            return render(request, 'todo/signup_error.html', context={'warning':'Invalid data!'})
        


class UserPageView(View):
    def get(self, request, username):
        try:
            user = User.objects.get(username= username)
        except User.DoesNotExist:
            return redirect(reverse('signup'))
        messages = Task.objects.filter(author=user).order_by('-is_important')
        if not request.user.is_authenticated:
            return redirect(reverse('signin'))
        if user != request.user:
            return HttpResponseForbidden()
        return render(request, 'todo/userpage.html', {'user_': user, 'message': messages})

    def post(self, request, username):
        user = User.objects.get(username=username)
        if user == request.user:
            text = request.POST['text']
            title = request.POST['title']
            important = request.POST.get('important', False)
            message = Task(text=text, author=request.user, title=title, is_important=important)
            message.save()

        return self.get(request, username)

class TaskDeleteView(View):
    def get(self, request, id):
        message = Task.objects.get(pk=id)
        author = message.author
        if message.author == request.user:
            message.delete()

        return redirect(reverse('userpage', kwargs={'username': author.username}))

class TaskCompleteView(View):
    def get(self, request, id):
        message = Task.objects.get(pk=id)
        author = message.author
        if message.author == request.user:
            message.complete = True
            message.save()

        return redirect(reverse('userpage', kwargs={'username': author.username}))


class TaskDeleteAllView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        messages = Task.objects.filter(author=user)
        if user == request.user:
            messages.delete()

        return redirect(reverse('userpage', kwargs={'username': user.username}))


class TaskEditView(View):
    def get(self, request, id):
        message = Task.objects.get(pk=id)
        user = message.author
        if not request.user.is_authenticated:
            return redirect(reverse('signin'))
        if user != request.user:
            return HttpResponseForbidden()
        return render(request, 'todo/edit.html', context={'message':message, 'user_':user})

    def post(self, request, id):
        message = Task.objects.get(pk=id)
        user = message.author
        if user == request.user:
            text = request.POST['text']
            title = request.POST['title']
            message.title = title
            message.text = text
            message.save()

        return redirect(reverse('userpage', kwargs={'username':user}))


