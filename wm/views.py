from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import MyShortCut, Type
from django.contrib.auth.models import User

from django.db.models import F
from django.db.models import Q

from django.urls import reverse
from django.http import HttpResponse, JsonResponse


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
            return MyShortCut.objects.all().order_by('-created')
        else:
            return MyShortCut.objects.filter(Q(author=self.request.user)).order_by('-created')

class MyShortCutCreateView_textarea(LoginRequiredMixin,CreateView):
    model = MyShortCut
    fields = ['title','content2']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")

        ty = Type.objects.get(type_name="textarea")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')

class MyShortCutCreateView_input(LoginRequiredMixin,CreateView):
    model = MyShortCut
    fields = ['title','content1']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행1")
        ty = Type.objects.get(type_name="input")
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')
