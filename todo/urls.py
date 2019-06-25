from django.contrib import admin
from django.urls import path, include
from . import views

app_name= 'todo'
urlpatterns = [

    path('team_info_list/', views.TeamInfoListView.as_view() , name="TeamInfoListView"),
    path('TeaminfoCreate/', views.TeamInfoCreateView.as_view() , name="create_team_info"),
    # 팀 리스트 삭제
    path('team_info_list/delete/teaminfo/<int:team_id>', views.delete_team_info , name="delete_team_info"),
    path('<int:id>/edit/', views.todo_edit, name='todo_edit'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('new/',views.todo_new , name ="todo_new"),
    path('search/<str:q>/', views.TodoSearch.as_view()),
    path('<int:pk>/', views.todoDetail.as_view(), name='todo_detail'),
    path('card', views.TodoList_by_card.as_view() , name="todo_list_by_card"),
    path('', views.TodoList.as_view() , name="todo_list"),
    path('complete_bycard/', views.TodoListByComplete_by_card.as_view() , name="todo_complete_list_by_card"),
    path('<int:pk>/new_comment/summer_note', views.new_comment_summer_note),
    path('<int:pk>/new_comment/text_area', views.new_comment_text_area),
    path('edit_comment/<int:pk>/', views.CommentUpdate.as_view(), name="edit_url"),
    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_url"),
    path('<int:id>/todo_complete/',views.todo_complete , name ="todo_complete"),
    path('<int:id>/todo_help/', views.todo_help, name="todo_help"),
    path('<int:id>/todo_help_cancle/', views.todo_help_cancle, name="todo_help_cancle"),
    path('category/<str:slug>/', views.TodoListByCategory.as_view() , name="total_ucomplete_todo_list"),
    path('todolist/admin/', views.TodoListByAdmin.as_view() , name="todo_list_by_admin"),
    path('todolist/admin/insert_popup/<str:user_name>', views.isnert_todo_popup_by_admin , name="isnert_todo_popup_by_admin"),
    path('todolist/complete/me/', views.TodoCompleteListByMe.as_view() , name="todo_complete_list_byme"),
    path('todolist/complete/me/todo_delete_ajax/', views.todo_delete_ajax , name="todo_delete_ajax"),
    path('todolist/uncomplete/me', views.TodoUnCompleteListByMe.as_view() , name="todo_uncomplete_list_byme"),
    path('completeList/total/', views.TodoListByComplete_total.as_view() , name="todo_complete_list_total"),
    path('update_comment_ajax/<int:id>', views.update_comment_ajax , name='update_comment_ajax'),
    path('delete_comment_ajax/<int:id>', views.delete_comment_ajax , name='delete_comment_ajax'),
    path('<int:pk>/update/', views.CommentUpdate.as_view()),
    path('new/admin/<str:user_name>',views.todo_new_admin, name ="todo_new_admin"),
    path('status/',views.todo_status_list, name ="todo_status_list"),
    path('todo_delete_ajax/',views.todo_delete_ajax, name ="todo_delete_ajax"),
    path('todolist/uncomplete/<str:user_id>/',views.UncompleteTodoListByUserId.as_view(), name ="TodoListByUserId"),
    path('todolist/complete/<str:user_id>/',views.CompleteTodoListByUserId.as_view(), name ="TodoListByUserId"),

    path('todolist/uncomplete/admin/<str:user_id>/<str:team_leader_name>',views.UncompleteTodoListByUserId_admin.as_view(), name ="todolist_by_user_complete"),
    path('todolist/complete/admin/<str:user_id>/<str:team_leader_name>',views.CompleteTodoListByUserId_admin.as_view(), name ="todolist_by_user_uncomplete"),

    # team
    path('team_register/', views.team_register , name='team_register'),
    path('team_member_list/<int:team_info_id>/delete/team/memeber', views.delete_team_member, name='delete_team_member'),
    path('delete/team/memeber/byajax', views.delete_team_memeber_info_by_memberId, name="delete_team_memeber_info_by_memberId"),

    path('team_member_list/<int:team_info_id>', views.team_member_list_view.as_view() , name="team_member_list"),



]
