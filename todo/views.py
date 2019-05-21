# from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .forms import TodoForm
from django.urls import reverse_lazy
from django.db.models import Q
from . forms import CommentForm
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Todo, CommentForTodo, Category

# create your view
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


def delete_comment_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = CommentForTodo.objects.filter(Q(id=id)).delete()
        print('delete 성공');
        return JsonResponse({
            'message': '댓글 삭제 성공',
        })
    else:
        return redirect('/todo')

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


class TodoListByComplete(LoginRequiredMixin,ListView):
    model = Todo
    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False))

    def get_template_names(self):
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


def new_comment(request, pk):
    print("댓글 입력 함수 기반뷰 실행")
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.todo = todo
            comment.author = request.user
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
        return ['todo/_todo_detail.html']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(todoDetail, self).get_context_data(**kwargs)
        context['comments'] = CommentForTodo.objects.filter(todo=self.object.pk)
        context['detail_id'] = self.object.pk
        context['comment_form'] = CommentForm()
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
        return ['todo/todo_list_by_card.html']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all().order_by('-created')
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time="")).order_by('-created')

class TodoSearch(ListView):
    def get_template_names(self):
        return ['todo/todo_list_search.html']

    def get_queryset(self):
        print("실행 확인")
        q = self.kwargs['q']
        object_list = Todo.objects.filter(Q(title__contains=q) | Q(content__contains=q) & ~Q(elapsed_time="")).order_by('-created')
        print("result : ", object_list)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodoSearch, self).get_context_data(**kwargs)
        context['search_word'] = self.kwargs['q']
        return context

def todo_complete(request, id):
    if request.user.is_authenticated():
        todo = get_object_or_404(Todo, id=id)
        now_diff = todo.now_diff
        print("now_diff : ", now_diff)
        Todo.objects.filter(Q(id=id)).update(elapsed_time = now_diff)
        Todo.objects.filter(Q(id=id)).update(category = None)
        print("todo 목록을 저장하였습니다.")
        return redirect('/todo')
    else:
        return redirect('accouts/login')

class todo_delete_view(DeleteView):
    model = Todo
    success_url = reverse_lazy('todo:todo_list')
    # success_message = "delete was complted"
todo_delete = todo_delete_view.as_view()

def todo_new(request):
    if request.method=="POST":
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
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
