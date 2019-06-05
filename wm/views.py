from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import MyShortCut, Type, Category
from django.contrib.auth.models import User

from django.db.models import F
from django.db.models import Q

from django.urls import reverse
from django.http import HttpResponse, JsonResponse

# MyShortcutListByCategory

def update_shortcut1_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST['content1']

        print('shortcut을 ajax로 update')
        print('id : ', id)
        print("content1 : ", content1)
        todo = MyShortCut.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def update_shortcut2_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content2 = request.POST['content2']

        print('shortcut을 ajax로 update')
        print('id : ', id)
        print("content2 : ", content2)
        todo = MyShortCut.objects.filter(Q(id=id)).update(content2 = content2)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')


class MyShortcutListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
        return MyShortCut.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = MyShortCut.objects.filter(category=None,author=self.request.user).count()
        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        return context


def delete_shortcut_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = MyShortCut.objects.filter(Q(id=id)).delete()
        print('MyShortCut delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 삭제 성공',
        })
    else:
        return redirect('/todo')


# Create your views here.
class MyShortCutListView(LoginRequiredMixin,ListView):
    model = MyShortCut
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return MyShortCut.objects.filter(author=self.request.user).order_by('-created')
        else:
            return MyShortCut.objects.filter(Q(author=self.request.user)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
            context = super(MyShortCutListView, self).get_context_data(**kwargs)
            context['category_list'] = Category.objects.all()
            context['posts_without_category'] = MyShortCut.objects.filter(category=None, author=self.request.user).count()

            return context

class MyShortCutCreateView_input(LoginRequiredMixin,CreateView):
    model = MyShortCut
    fields = ['title','content1','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행1")
        ty = Type.objects.get(type_name="input")
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')

class MyShortCutCreateView_textarea(LoginRequiredMixin,CreateView):
    model = MyShortCut
    fields = ['title','content2','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")

        ty = Type.objects.get(type_name="textarea")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')
