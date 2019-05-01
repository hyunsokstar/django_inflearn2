from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),

]
