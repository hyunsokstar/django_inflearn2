from django.contrib import admin
from django.urls import path, include
from . import views

app_name= 'todo'
urlpatterns = [
    path('<int:id>/edit/', views.todo_edit, name='todo_edit'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('new/',views.todo_new , name ="todo_new"),
    path('search/<str:q>/', views.TodoSearch.as_view()),

    # todo
    # 상세 보기
    path('<int:pk>/', views.todoDetail.as_view(), name='todo_detail'),
    path('card', views.TodoList_by_card.as_view() , name="todo_list_by_card"),
    path('', views.TodoList.as_view() , name="todo_list"),
    path('complete_bycard/', views.TodoListByComplete_by_card.as_view() , name="todo_complete_list_by_card"),
    path('<int:pk>/new_comment/', views.new_comment),

    # todo 댓글 수정 뷰
    path('edit_comment/<int:pk>/', views.CommentUpdate.as_view(), name="edit_url"),

    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_url"),
    path('<int:id>/todo_complete/',views.todo_complete , name ="todo_complete"),
    path('<int:id>/todo_help/', views.todo_help, name="todo_help"),

    path('<int:id>/todo_help_cancle/', views.todo_help_cancle, name="todo_help_cancle"),

    path('category/<str:slug>/', views.TodoListByCategory.as_view() , name="total_ucomplete_todo_list"),

    path('todolist/complete/me/', views.TodoCompleteListByMe.as_view() , name="todo_complete_list_byme"),
    path('todolist/uncomplete/me', views.TodoUnCompleteListByMe.as_view() , name="todo_complete_list_byme"),

    path('completeList/total/', views.TodoListByComplete_total.as_view() , name="todo_complete_list_total"),

    path('update_comment_ajax/<int:id>', views.update_comment_ajax , name='update_comment_ajax'),
    path('delete_comment_ajax/<int:id>', views.delete_comment_ajax , name='delete_comment_ajax'),

    path('<int:pk>/update/', views.CommentUpdate.as_view()),

    # ex1
    path('new/admin',views.todo_new_admin, name ="todo_new_admin"),

    # Cork
    # path('cowork/list',views.CoworkList.as_view(), name ="cowork_list"),


]
