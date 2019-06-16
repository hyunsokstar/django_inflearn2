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

    path('<int:pk>/new_comment/summer_note', views.new_comment_summer_note),
    path('<int:pk>/new_comment/text_area', views.new_comment_text_area),

    # todo 댓글 수정 뷰
    path('edit_comment/<int:pk>/', views.CommentUpdate.as_view(), name="edit_url"),

    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_url"),

    path('<int:id>/todo_complete/',views.todo_complete , name ="todo_complete"),

    path('<int:id>/todo_help/', views.todo_help, name="todo_help"),

    path('<int:id>/todo_help_cancle/', views.todo_help_cancle, name="todo_help_cancle"),

    path('category/<str:slug>/', views.TodoListByCategory.as_view() , name="total_ucomplete_todo_list"),

    # 관리자만 할일 리스트를 출력하고 입력하는 페이지를 따로 만들자
    # 관리자가 아니면 이페이지에 접근 불가
    # 현재 로그인 유저(관리자)가 입력한 리스트만 출력
    # 추가 기능
    # 1.(유저 리스트 출력, 클릭시 할일 목록 바로 가기,)
    # 2.할일 분배하기 기능
    # 3.할일에 대해 user들에게 메세지 알림 기능
    # todolist by admin
    path('todolist/admin/', views.TodoListByAdmin.as_view() , name="todo_list_by_admin"),
    path('todolist/admin/insert_popup/<str:user_name>', views.isnert_todo_popup_by_admin , name="isnert_todo_popup_by_admin"),

    path('todolist/complete/me/', views.TodoCompleteListByMe.as_view() , name="todo_complete_list_byme"),
    path('todolist/complete/me/todo_delete_ajax/', views.todo_delete_ajax , name="todo_delete_ajax"),

    path('todolist/uncomplete/me', views.TodoUnCompleteListByMe.as_view() , name="todo_uncomplete_list_byme"),

    path('completeList/total/', views.TodoListByComplete_total.as_view() , name="todo_complete_list_total"),

    path('update_comment_ajax/<int:id>', views.update_comment_ajax , name='update_comment_ajax'),
    path('delete_comment_ajax/<int:id>', views.delete_comment_ajax , name='delete_comment_ajax'),

    path('<int:pk>/update/', views.CommentUpdate.as_view()),

    path('new/admin',views.todo_new_admin, name ="todo_new_admin"),

    # todo(user) 현황
    path('status/',views.todo_status_list, name ="todo_status_list"),
    path('todo_delete_ajax/',views.todo_delete_ajax, name ="todo_delete_ajax"),

    path('todolist/uncomplete/<str:user_id>/',views.UncompleteTodoListByUserId.as_view(), name ="TodoListByUserId"),
    path('todolist/complete/<str:user_id>/',views.CompleteTodoListByUserId.as_view(), name ="TodoListByUserId"),

    # Cork
    # path('cowork/list',views.CoworkList.as_view(), name ="cowork_list"),
    # todo_delete_ajax


]
