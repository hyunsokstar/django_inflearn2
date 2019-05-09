from django.contrib import admin
from django.urls import path, include
from . import views

app_name= 'todo'

urlpatterns = [
    path('<int:id>/edit/', views.todo_edit, name='todo_edit'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('new/',views.todo_new , name ="todo_new"),
    path('<int:id>/todo_complete/',views.todo_complete , name ="todo_complete"),
    path('search/<str:q>/', views.TodoSearch.as_view()),

    # todo
    path('<int:pk>/', views.todoDetail.as_view(), name='todo_detail'),
    path('card', views.TodoList_by_card.as_view() , name="todo_list_by_card"),
    path('', views.TodoList.as_view() , name="todo_list"),
    path('complete_bycard/', views.TodoListByComplete_by_card.as_view() , name="todo_complete_list_by_card"),
    # path('complete/', views.TodoListByComplete_by_card)




]
