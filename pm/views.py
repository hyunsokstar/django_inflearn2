from .models import Manual
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView

from django.urls import reverse

from django.shortcuts import render, redirect

from django.contrib import messages
from .forms import ManualForm

# 1122
class ManulUpdate(UpdateView):
    model = Manual
    form_class = ManualForm

def delete_manual(request, pk):
    manual = Manual.objects.get(pk=pk)

    if request.user == manual.author:
        manual.delete()
        messages.success(request,'메뉴얼을 삭제했습니다.')
        return redirect('/pm/')
    else:
        messages.success(request,'당사자만 삭제 가능합니다.')
        return redirect('/pm/')

class ManualCreateView(CreateView):
    model = Manual
    form_class = ManualForm

    def form_valid(self, form):
        fn = form.save(commit=False)
        fn.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pm:manual_list')

class ManualListView(LoginRequiredMixin,ListView):
    model = Manual
    paginate_by = 20
    # ordering = ['-grade']

class ManualDetailView(DetailView):
    model = Manual
    # def get_template_names(self):
    #     if self.request.is_ajax():
    #         return ['todo/_todo_detail.html']
    #     return ['todo/todo_detail.html']

        # def get_context_data(self, *, object_list=None, **kwargs):
        #     context = super(todoDetail, self).get_context_data(**kwargs)
        #     context['comments'] = CommentForTodo.objects.filter(todo=self.object.pk)
        #     context['detail_id'] = self.object.pk
        #     context['comment_form'] = CommentForm()
        #     return context
