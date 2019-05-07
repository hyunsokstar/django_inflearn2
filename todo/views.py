# from django.views.generic import ListView
from .models import Todo
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TodoForm
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

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

class TodoList(ListView):
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
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time=""))


class TodoListByComplete(ListView):
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
