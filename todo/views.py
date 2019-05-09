# from django.views.generic import ListView
from .models import Todo
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TodoForm
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

# create your view

class todoDetail(DetailView):
    model = Todo
    def get_template_names(self):
        if self.request.is_ajax():
            return ['todo/_todo_detail.html']
        return ['todo/todo_detail.html']

class TodoList(ListView):
    model = Todo
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all().order_by('-created')
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time="")).order_by('-created')


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
    todo = get_object_or_404(Todo, id=id)
    now_diff = todo.now_diff
    print("now_diff : ", now_diff)
    Todo.objects.filter(Q(id=id)).update(elapsed_time = now_diff)
    print("todo 목록을 저장하였습니다.")
    return redirect('/todo')

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
        return ['todo/todo_list_complete.html']
