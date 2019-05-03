from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('tag/<str:slug>/', views.PostListByTag.as_view()),

    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('create/', views.PostCreate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),

    path('delete_comment/<int:pk>/', views.delete_comment),

]
