# from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, resolve_url

from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.db.models import F
from django.db.models import Q

from django.urls import reverse
from django.http import HttpResponse, JsonResponse

# form import
from .forms import MyShortCutForm_input, MyShortCutForm_summer_note , MyShortCutForm_input_title
from accounts2.models import Profile

from .models import MyShortCut, Type, Category, CategoryNick

# 1122

#  path('update/category/nick/', views.MyShortCutListView.as_view() , name="update_category_nick"),
# 'ca_id':ca_id,
# 'field':field,
# 'ca_nick_update':ca_nick_update,

def update_shortcut_nick(request):
    if request.method == "POST" and request.is_ajax():
        ca_id = int(request.POST['ca_id'])
        field = request.POST['field']
        ca_nick_update = request.POST['ca_nick_update']

        print('update id : ',ca_id)
        print('update field  : ',field)
        print('update value : ',ca_nick_update)
        cn = CategoryNick.objects.filter(id=ca_id).update(**{field: ca_nick_update})
        # .update(field = ca_nick_update)

        # print('update success : ' , update.id);

        return JsonResponse({
            'message': 'shortcut category nick name update 성공 ' +ca_nick_update,
        })
    else:
        return redirect('/wm/shortcut')


def CategoryNickListByUserId(request, user_name):

    if request.method == 'GET':
        print("user_name : ", user_name)
        user = User.objects.get(username=user_name)

        cn = CategoryNick.objects.get_or_create(
            author=user.id,
        )
        print("cn : ", cn)

        cn_my = CategoryNick.objects.get(author=user.id)
        print("cn_my : ", cn_my)


        return render(request, 'wm/categorynick_list.html', {
            "category" : cn_my
        })
    else:
        return HttpResponse("Request method is not a GET")

class modify_myshortcut_by_summer_note(UpdateView):
    model = MyShortCut
    form_class = MyShortCutForm_summer_note

    def get_template_names(self):
        return ['wm/myshortcut_summernote_form.html']

def update_shorcut_id_for_user(request, id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        user_id = request.POST['user_id']

        print('id : ', id)
        todo = Profile.objects.filter(Q(user=id)).update(shortcut_user_id = user_id)

        print('update 성공');

        return JsonResponse({
            'message': 'shortcut user_id 업데이트 성공',
        })
    else:
        return redirect('/todo')



def update_shortcut1_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')

        print('shortcut을 ajax로 update input')
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
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('shortcut을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = MyShortCut.objects.filter(Q(id=id)).update(content2 = content2)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')


def myfunc():
    print("myfunc 실행")


class MyShortcutListByCategory(ListView):

    def get_queryset(self):
        user = self.request.user.profile.shortcut_user_id
        # print("user : ", user)
        print("self.request.user : ", self.request.user)

        if user == "me":
            user = self.request.user
        else:
            user = User.objects.get(username=user)

        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
            pf = Profile.objects.filter(Q(user=self.request.user)).update(selected_category_id = category.id)

            print('category id update 성공')
        return MyShortCut.objects.filter(category=category, author=user).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['posts_without_category'] = MyShortCut.objects.filter(category=None,author=self.request.user).count()
        context['category_list'] = Category.objects.all()

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

class MyShortCutListView(LoginRequiredMixin,ListView):
    model = MyShortCut
    paginate_by = 20
    user = 0

    def get_queryset(self):
        user = self.request.user.profile.shortcut_user_id
        # print("user : ", user)
        print("self.request.user : ", self.request.user)

        if user == "me":
            user = self.request.user
        else:
            user = User.objects.get(username=user)

        print("user : ", user)

        if self.request.user.is_anonymous:
            return MyShortCut.objects.filter(author=self.request.user).order_by('created')
        else:
            selected_category_id = self.request.user.profile.selected_category_id
            return MyShortCut.objects.filter(Q(author=user, category = selected_category_id)).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
            context = super(MyShortCutListView, self).get_context_data(**kwargs)
            context['category_list'] = Category.objects.all()
            context['posts_without_category'] = MyShortCut.objects.filter(category=None, author=self.request.user).count()

            return context

class MyShortCutCreateView_input(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_input
    # fields = ['title','content1','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행11")
        ty = Type.objects.get(type_name="input")
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')




class MyShortCutCreateView_input_title(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_input_title
    # fields = ['title','content1','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")
        ty = Type.objects.get(type_name="input_title")
        print("ty : ", ty)
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')


class MyShortCutCreateView_textarea(LoginRequiredMixin,CreateView):
    model = MyShortCut
    fields = ['title','content2']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")

        ty = Type.objects.get(type_name="textarea")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty

        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')


class MyShortCutCreateView_textarea_summer_note(LoginRequiredMixin,CreateView):
    model = MyShortCut
    form_class = MyShortCutForm_summer_note

    def get_template_names(self):
        return ['wm/myshortcut_summernote_form.html']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행4")

        ty = Type.objects.get(type_name="summer_note")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty

        category_id = self.request.user.profile.selected_category_id
        ca = Category.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wm:my_shortcut_list')
