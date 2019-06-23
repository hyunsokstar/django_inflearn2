from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .forms import TodoForm, TodoAdminForm
from django.db.models import F
from django.db.models import Q

from . forms import CommentForm, CommentForm_TextArea

from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Todo, CommentForTodo, Category, TodoType, TeamInfo, TeamMember
from django.contrib.auth.models import User
from accounts2.models import Profile
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.urls import reverse

from django.http import HttpResponseRedirect

# 1122 for todo

# class TeamMember(models.Model):
#     team = models.ForeignKey(TeamInfo, on_delete=models.CASCADE)
#     member = models.ForeignKey(User, on_delete=True)
#     position = models.CharField(max_length=50,default="member")

def delete_team_member(request):
    print("팀 멤버 정보 삭제 22")
    if request.method == "POST" and request.is_ajax():
        option = ""
        team_memeber_id = request.POST['team_memeber_id']
        member = request.POST['member']
        team_id = request.POST['team_id']

        print("team_memeber_id : ", team_memeber_id)
        print("member : ", member)
        print("team_id : ", team_id)

        dr = TeamMember.objects.filter(Q(id=team_memeber_id)).delete()

        return JsonResponse({
            'message': '멤버 탈퇴 성공 : '+ member,
        })

def team_register(request):
    print("team_register view 실행")
    if request.method == "POST" and request.is_ajax():
        option = ""
        teamId = request.POST['teamId']
        userId = request.POST['userId']

        ti_obj = TeamInfo.objects.get(Q(id=teamId))

        tm = TeamMember.objects.filter(Q(team=teamId) & Q(member=userId))
        print("tm : " , tm)

        if not tm:
            print("팀 가입")
            option="가입"
            ti, is_created = TeamMember.objects.get_or_create(
                team=ti_obj,
                member=request.user
            )
            TeamInfo.objects.filter(id=teamId).update(member_count = F('member_count')+1)

        else:
            print("팀 탈퇴")
            option = "탈퇴"
            dr = TeamMember.objects.filter(Q(team=teamId) & Q(member=userId)).delete()
            print("dr : ", dr)
            TeamInfo.objects.filter(id=teamId).update(member_count = F('member_count')-1)

        return JsonResponse({
            'message': '팀' + option + '성공',
            "option":option
        })
    else:
        return reverse_lazy('todo:TeamInfoListView')


class UncompleteTodoListByUserId_admin(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        print("user_id : ", user_id)
        user = User.objects.get(username=user_id)
        print("user : " , user.id)

        return Todo.objects.filter(Q(elapsed_time__isnull=True) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(username=user_id)
        print("user_id : ", user_id)
        print("user : ", user)

        # 유저 이름
        context['user_name'] = self.kwargs['user_id']

        # 카테고리 정보
        context['category_list'] = Category.objects.all()
        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        context['current_state_for_list'] = "미완료"

        context['team_leader_name']=self.kwargs['team_leader_name']

        return context

    def get_template_names(self):
            return ['todo/uncomplete_todo_list_for_user_by_admin.html']

class CompleteTodoListByUserId_admin(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(username=user_id)
        print("user : " , user.id)
        print("완료 목록 출력 ")

        return Todo.objects.filter(Q(elapsed_time__isnull=False) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        user_id = self.kwargs['user_id']
        user = User.objects.get(username=user_id)
        context = super(type(self), self).get_context_data(**kwargs)

        # 유저 이름
        context['user_name'] = self.kwargs['user_id']

        # 카테고리 정보
        context['category_list'] = Category.objects.all()

        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=False)).count()


        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        context['current_state_for_list'] = "완료"
        context['team_leader_name'] = self.kwargs['team_leader_name']
        return context

    def get_template_names(self):
            return ['todo/complete_todo_list_for_user_by_admin.html']


def delete_team_info(request,team_id):
    user = request.user
    if request.method == "GET" and request.is_ajax():
        # team_info_id = request.POST['team_info_id']
        team_info_id = team_id
        ti = TeamInfo.objects.filter(Q(id=team_info_id)).delete()
        print('delete_team_info 성공');
        return JsonResponse({
            'message': '댓글 삭제 성공',
        })
    else:
        return JsonResponse({
            'message': '댓글 삭제 실패',
        })

# def register_for_team(request, team_id):
#     print("team_id : " , team_id)
#
#     team_name = TeamInfo.objects.get(id = team_id).team_name
#
#     Profile.objects.filter(Q(user=request.user.id)).update(team = team_id)
#     TeamInfo.objects.filter(id=team_id).update(member_count = F('member_count')+1)
#     member_count=TeamInfo.objects.get(id=team_id).member_count
#
#     messages.success(request, '{} 회원이 {}팀에 가입했습니다./'.format(request.user, team_name))
#     messages.success(request, '{}팀의 회원수가 {}명이 되었습니다./'.format(team_name, member_count))
#
#     return HttpResponseRedirect(reverse('todo:team_member_list' , kwargs={'team_info_id': team_id}))
#
# def unregister_for_team(request, team_id):
#     print("team_id : " , team_id)
#     team_name = TeamInfo.objects.get(id = team_id).team_name
#
#     Profile.objects.filter(Q(user=request.user.id)).update(team = "")
#     TeamInfo.objects.filter(id=team_id).update(member_count = F('member_count')-1)
#     member_count=TeamInfo.objects.get(id=team_id).member_count
#
#     messages.success(request, '{} 회원이 {}팀에서 탈퇴했습니다./'.format(request.user,team_name))
#     messages.success(request, '{}팀의 회원수가 {}명이 되었습니다./'.format(team_name, member_count))
#
#     return HttpResponseRedirect(reverse('todo:team_member_list' , kwargs={'team_info_id': team_id}))

class team_member_list_view(LoginRequiredMixin,ListView):
    model = TeamMember
    paginate_by = 40

    def get_queryset(self):
        team_info_id = self.kwargs['team_info_id']
        print("team_info_id : " , team_info_id)
        return TeamMember.objects.filter(team=team_info_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        team_info_id = self.kwargs['team_info_id']
        ti = TeamInfo.objects.get(id=team_info_id)
        print("ti : ", ti)
        context["team_id"] = ti.id
        context['team_name'] = ti.team_name
        context['team_leader_name'] = ti.leader.username
        return context

    def get_template_names(self):
        print("team member list page를 출력")
        return ['todo/teammember_list.html']


class TeamInfoCreateView(CreateView):
    model = TeamInfo
    fields = ['team_name','team_description']
    success_url = reverse_lazy('todo:TeamInfoListView')

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행")
        ti = form.save(commit=False)
        ti.leader = self.request.user
        return super().form_valid(form)


class TeamInfoListView(LoginRequiredMixin,ListView):
    model = TeamInfo
    paginate_by = 20


def isnert_todo_popup_by_admin(request,user_name):
    print("isnert_todo_popup_by_admin 호출")
    print("user_name : ", user_name)

    return render(request, 'todo/insert_todo_by_admin.html', {
        'foo': 'bar',
    })

class TodoListByAdmin(LoginRequiredMixin,ListView):
    model = Todo
    paginate_by = 20

    def get_queryset(self):
        return Todo.objects.filter(Q(elapsed_time__isnull=False) & Q(author = self.request.user)).order_by('-created')

    def get_template_names(self):
        print("admin page를 출력")
        return ['todo/todo_list_by_admin.html']

class CompleteTodoListByUserId(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        print("user_id : ", user_id)
        user = User.objects.get(username=user_id)
        print("user : " , user.id)

        return Todo.objects.filter(Q(elapsed_time__isnull=False) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        # 카테고리 정보
        context['category_list'] = Category.objects.all()
        # 미완료 개수
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        return context

    def get_template_names(self):
            return ['todo/todo_list_total.html']

class UncompleteTodoListByUserId(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        print("user_id : ", user_id)
        user = User.objects.get(username=user_id)
        print("user : " , user.id)

        return Todo.objects.filter(Q(elapsed_time__isnull=True) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        # 카테고리 정보
        context['category_list'] = Category.objects.all()
        # 미완료 개수
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        return context

    def get_template_names(self):
            return ['todo/todo_list_total.html']

@login_required
def todo_delete_ajax(request):
    todo_ids = request.POST.getlist('todo_arr[]')
    if todo_ids:
        Todo.objects.filter(pk__in=todo_ids, author=request.user).delete()

    return redirect('/todo')

def todo_status_list(request):
    print("todo_status_list 실행")

    users = User.objects.all()

    return render(request, 'todo/todo_status_list.html', {
        'users': users,
    })

def FinisherList(request, id):
    fl = Finisher.objects.filter(Q(bestlec=id))
    print("fl : ", fl)
    print('해당 id에 대한 FinisherList')
    return render(request, 'bestlec/finisher_list.html', {
        'fl': fl,
        'fn_id':id
    })

def todo_new_admin(request,user_name):
    if request.user.is_superuser:
        print("관리자는 입력할 수 있습니다.")
    else:
        messages.success(request,'관리자가 아니면 입력할 수 없습니다.')
        return redirect('/todo/category/_none')
    user = User.objects.get(username=user_name)

    if request.method=="POST":
        form = TodoAdminForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = user
            todo.director = request.user
            todo.save()
            return redirect('/todo/todolist/uncomplete/admin/'+user_name)
    else:
        form = TodoAdminForm()
    return render(request, 'todo/insert_todo_form_by_admin.html',{
        'user_name': user.username,
        'form':form
    })

class CommentUpdate(UpdateView):
    model = CommentForTodo
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment


class TodoListByComplete_total(LoginRequiredMixin,ListView):
    model = Todo
    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(elapsed_time__isnull=False))

    def get_template_names(self):
        return ['todo/todo_list_complete_total.html']
        # 카테고리 목록
    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()
        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        return context

def delete_comment_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = CommentForTodo.objects.filter(Q(id=id)).delete()
        print('delete 성공');
        return JsonResponse({
            'message': '댓글 삭제 성공',
        })
    else:
        return redirect('/myshortcut')


def update_comment_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        title = request.POST['title']
        file_name = request.POST['file_name']
        text = request.POST['text']

        print('id : ', id)
        print("title(view) : ", title)
        print("file_name : ", file_name)
        print("text : ", text)
        todo = CommentForTodo.objects.filter(Q(id=id)).update(title = title, file_name = file_name , text = text)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def todo_help(request, id):
    todo = get_object_or_404(Todo, id=id)
    now_diff = todo.now_diff
    print("now_diff : ", now_diff)
    Todo.objects.filter(Q(id=id)).update(category = 2)
    print("핼프를 요청 id:",id)
    return redirect('/todo')

def todo_help_cancle(request, id):
    print("todo_help_cancle")
    todo = get_object_or_404(Todo, id=id)
    now_diff = todo.now_diff
    print("now_diff : ", now_diff)
    Todo.objects.filter(Q(id=id)).update(category = "")
    print("핼프를 요청 id:",id)
    return redirect('/todo')

class TodoCompleteListByMe(LoginRequiredMixin,ListView):
    model = Todo

    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            list_count = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False))
            print("list_count  ", list_count)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False))

    def get_template_names(self):
        print("todo list complete 호출")
        return ['todo/todo_list_complete.html']
        # 카테고리 목록
    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()
        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        return context



class TodoUnCompleteListByMe(LoginRequiredMixin,ListView):
    model = Todo
    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True))

    def get_template_names(self):
        return ['todo/todo_list.html']
        # 카테고리 목록
    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()
        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        return context


class TodoListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        print('slug : ', slug)

        if slug == '_none':
            category = None
            return Todo.objects.filter(Q(elapsed_time__isnull=True)).order_by('-created')
        else:
            # 카테고리가 없는 경우 전체 목록
            category = Category.objects.get(slug=slug)
            return Todo.objects.filter(Q(elapsed_time__isnull=True) & Q(category=category)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        # 미완료이면서 카테고리가 있는것
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category
        return context

    def get_template_names(self):
            return ['todo/todo_list_total.html']


def delete_comment(request, pk):
    comment = CommentForTodo.objects.get(pk=pk)
    todo = comment.todo

    if request.user == comment.author:
        comment.delete()
        return redirect('/todo')
    else:
        return redirect('/todo/')

class CommentUpdate(UpdateView):
    model = CommentForTodo
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment

def new_comment_summer_note(request, pk):
    print("댓글 입력 함수 기반뷰 실행")
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        ty = TodoType.objects.get(type_name="summer_note")


        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.todo = todo
            comment.author = request.user
            if comment.author == request.user:
                comment.user_type = 1
            else:
                comment.user_type = 2
            comment.type= ty
            comment.save()

            if request.is_ajax():
                return JsonResponse({
                    'author': comment.author.username,
                    'title': comment.title,
                    'file_name': comment.file_name,
                    'text':comment.text,
                    'created_at':comment.created_at,
                    'edit_id':pk,
                    'delete_id':pk
                })
            return redirect(comment.get_absolute_url())

        else:
            return JsonResponse(comment_form.errors,is_success=False)
    else:
        return redirect('/todo/')

def new_comment_text_area(request, pk):
    print("댓글 입력 함수 기반뷰 실행")
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        ty = TodoType.objects.get(type_name="text_area")

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.todo = todo
            comment.author = request.user

            if comment.author == request.user:
                comment.user_type = 1
            else:
                comment.user_type = 2

            comment.type= ty
            comment.save()

            if request.is_ajax():
                return JsonResponse({
                    'author': comment.author.username,
                    'title': comment.title,
                    'file_name': comment.file_name,
                    'text':comment.text,
                    'created_at':comment.created_at,
                    'edit_id':pk,
                    'delete_id':pk
                })
            return redirect(comment.get_absolute_url())

        else:
            return JsonResponse(comment_form.errors,is_success=False)
    else:
        return redirect('/todo/')

# todo 상세 보기
class todoDetail(DetailView):
    model = Todo
    def get_template_names(self):
        if self.request.is_ajax():
            return ['todo/_todo_detail.html']
        return ['todo/todo_detail.html']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(todoDetail, self).get_context_data(**kwargs)
        context['comments_list_my'] = CommentForTodo.objects.filter(todo=self.object.pk, author=self.request.user)
        context['comments_list_commenter'] = CommentForTodo.objects.filter(Q(todo=self.object.pk) & ~Q(author=self.request.user))
        context['detail_id'] = self.object.pk
        context['comment_form'] = CommentForm()
        context['comment_form_text_area'] = CommentForm_TextArea()

        return context

class TodoList(LoginRequiredMixin,ListView):
    model = Todo
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Todo.objects.all().order_by('-created')
        else:
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodoList, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['category_list'] = Category.objects.all()
        context['todos_without_category'] = Todo.objects.filter(category=None).count()

        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        return context

class TodoList_by_card(ListView):
    model = Todo
    paginate_by = 2

    def get_template_names(self):
        return ['todo/todo_list_search.html']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all().order_by('-created')
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time !=None)).order_by('-created')

class TodoSearch(ListView):
    def get_template_names(self):
        return ['todo/todo_list_search.html']
    # Q(elapsed_time = None)
    def get_queryset(self):
        print("실행 확인")
        q = self.kwargs['q']
        object_list = Todo.objects.filter(Q(title__contains=q) & Q(elapsed_time__isnull=False) ).order_by('-created')
        print("result : ", object_list)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodoSearch, self).get_context_data(**kwargs)
        context['search_word'] = self.kwargs['q']
        return context

def todo_complete(request, id):
    if request.user.is_authenticated:
        todo = get_object_or_404(Todo, id=id)
        now_diff = todo.now_diff()
        print("now_diff : ", now_diff)
        Todo.objects.filter(Q(id=id)).update(elapsed_time = now_diff)
        Todo.objects.filter(Q(id=id)).update(category = None)
        Todo.objects.filter(Q(id=id)).update(completion = "complete")

        Profile.objects.filter(Q(user=request.user.id)).update(completecount = F('completecount')+1, uncompletecount = F('uncompletecount')-1)
        messages.success(request,'할일 : {} 를 완료 처리 하였습니다 ~!'.format(todo))

        print("todo 완료 업데이트 완료 ")

        return redirect('/todo')
    else:
        return redirect('accouts/login')

# class todo_delete_view(DeleteView):
#     model = Todo
#     success_url = reverse_lazy('todo:todo_list')
#     # success_message = "delete was complted"
# todo_delete = todo_delete_view.as_view()

def todo_delete(request, pk):
    # template = 'todo/todo_confirm_delete.html'
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()

    if todo.completion == "uncomplete":
        Profile.objects.filter(Q(user=request.user.id)).update(uncompletecount = F('uncompletecount')-1)
    else:
        Profile.objects.filter(Q(user=request.user.id)).update(completecount = F('completecount')-1)

    print("todo" , todo , '를 삭제')
    return redirect('todo:todo_list')

    # AttributeError: '__proxy__' object has no attribute 'get'

def todo_new(request):
    if request.method=="POST":
        form = TodoForm(request.POST, request.FILES)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            print('todo를 저장했습니다')
            Profile.objects.filter(Q(user=request.user.id)).update(uncompletecount = F('uncompletecount')+1)
            print('uncompletecount를 +1')

            return redirect('/todo/')

    else:
        form = TodoForm()
    return render(request, 'todo/post_form.html',{
        'form':form
    })

def todo_edit(request, id):
    todo = get_object_or_404(Todo, id=id)

    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            post = form.save()
            return redirect('/todo')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/edit_form.html', {
        'form': form,
    })

class TodoListByComplete_by_card(ListView):
    model = Todo
    def get_queryset(self):
        # print(Todo.objects.all().count())
        # print(Todo.objects.filter(Q(author=self.request.user)).count())
        # print(Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time="")).count())
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & ~Q(elapsed_time=""))

    def get_template_names(self):
        return ['todo/todo_list_complete_card.html']
