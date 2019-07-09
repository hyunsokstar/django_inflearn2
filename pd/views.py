from django.shortcuts import render
from .models import MyTask , MySite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView
from django.db.models import Q
from django.urls import reverse

from .forms import MyTaskForm
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpResponse, JsonResponse

def add_mysite_by_ajax(request):

    site_name = request.POST['site_name']
    site_url = request.POST['site_url']

    print( "site_name : " + site_name )
    print( "site_url : " + site_url )

    my_site = MySite.objects.create(site_name=site_name, site_url= site_url, author=request.user)

    print("my_site : " , my_site)

    return JsonResponse({
        'message': 'mysite add 성공',
        "site_id": my_site.id,
    })

def delete_mysite_by_ajax(request):

    print("delete_mysite_by_ajax 수정 실행")
    user = request.user

    if request.method == "POST" and request.is_ajax():

        site_id = request.POST['site_id']
        print('site_id : ', site_id)

        mysite = MySite.objects.filter(Q(id=site_id)).delete()

        print('mysite 삭제 성공');

        return JsonResponse({
            'message': 'mysite delete 성공',
        })
    else:
        return redirect('/pd/private_task_list/')

def update_mysite_by_ajax(request):

    print("update_mysite_by_ajax 실행")

    user = request.user

    if request.method == "POST" and request.is_ajax():

        site_id = request.POST['site_id']
        site_name = request.POST['site_name']
        site_url = request.POST['site_url']

        print('site_id : ', site_id)
        print('site_name : ', site_name)
        print('site_url : ', site_url)

        mysite = MySite.objects.filter(Q(id=site_id)).update(site_name = site_name, site_url = site_url)
        print('mysite update 성공');

        return JsonResponse({
            'message': 'mysite update 성공',
        })
    else:
        return redirect('/pd/private_task_list/')

def delete_mytask_by_ajax(request):

    print("mytask 수정 실행")

    user = request.user

    if request.method == "POST" and request.is_ajax():

        mytask_id = request.POST['mytask_id']
        print('mytask_id : ', mytask_id)

        mytask = MyTask.objects.filter(Q(id=mytask_id)).delete()

        print('mytask 삭제 성공');

        return JsonResponse({
            'message': 'mytask delete 성공',
        })
    else:
        return redirect('/pd/private_task_list/')

def update_mytask_by_ajax(request):

    print("mytask 수정 실행")

    user = request.user

    if request.method == "POST" and request.is_ajax():

        mytask_id = request.POST['mytask_id']
        mytask_github = request.POST['mytask_github']
        mytask_title = request.POST['mytask_title']
        mytask_content = request.POST['mytask_content']
        mytask_shorcut_id = request.POST['mytask_shorcut_id']
        print('mytask_id : ', mytask_id)

        todo = MyTask.objects.filter(Q(id=mytask_id)).update(title = mytask_title, github = mytask_github, content = mytask_content, shortcut_id = mytask_shorcut_id)
        print('mytask update 성공');

        return JsonResponse({
            'message': 'mytask update 성공',
        })
    else:
        return redirect('/pd/private_task_list/')

def mytask_new(request):
    if request.method=="POST":
        form = MyTaskForm(request.POST, request.FILES)
        if form.is_valid():
            mytask = form.save(commit=False)
            mytask.author = request.user
            mytask.save()
            return redirect('/pd/private_task_list')
    else:
        form = MyTaskForm()
    return render(request, 'pd/mytask_form.html',{
        'form':form
    })


class private_desk_list(LoginRequiredMixin,ListView):
    model = MyTask
    paginate_by = 20
    # ordering = ['created_at']

    def get_queryset(self):
        print("private_desk_list 실행 1111")
        object_list = MyTask.objects.filter(Q(author=self.request.user)).order_by('created_at')
        print("result : ", object_list)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(private_desk_list, self).get_context_data(**kwargs)
        context['mysite_list'] = MySite.objects.all()
        return context
