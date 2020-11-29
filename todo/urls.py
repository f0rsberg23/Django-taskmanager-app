"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import IndexView, SignInView, SignUpView, LogoutView, UserPageView, TaskDeleteView, TaskCompleteView, TaskDeleteAllView, TaskEditView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signin', SignInView.as_view(), name='signin'),
    path('signup', SignUpView.as_view(), name= 'signup'),
    path('users/<str:username>', UserPageView.as_view(), name='userpage'),
    path('delete/<int:id>', TaskDeleteView.as_view(), name= 'message_delete'),
    path('complete/<int:id>', TaskCompleteView.as_view(), name= 'complete'),
    path('deleteall/<str:username>', TaskDeleteAllView.as_view(), name= 'delete'),
    path('edit/<int:id>', TaskEditView.as_view(), name= 'edit'),
]
