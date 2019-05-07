from django.contrib import admin
from django.urls import path, include
from . import views

app_name= 'todo'

urlpatterns = [
    path('', views.TodoList.as_view() , name="todo_list"),
    path('complete/', views.TodoListByComplete.as_view() , name="todo_list_by_complete"),
    path('<int:id>/edit/', views.todo_edit, name='todo_edit'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('new/',views.todo_new , name ="todo_new"),
    path('<int:id>/todo_complete/',views.todo_complete , name ="todo_complete"),

]
