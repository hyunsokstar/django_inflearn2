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

from .models import MyShortCut, Type, Category, CategoryNick, CommentForShortCut
from django.http import HttpResponseRedirect

# 1122
# def search_by_id_and_word():
# 	pass
	
	
def copyForCategorySubjectToMyCategory(request):
	author = request.POST['author']
	original_category = request.POST['original_category']
	destination_category = request.POST['destination_category']
	
	print("author : ", author)
	print("original_category : ", original_category)
	print("destination_category : ", destination_category)
	
	MyShortCut.objects.filter(Q(author=request.user) & Q(category=destination_category)).delete()
	
	user_id = User.objects.get(username=author).id
	ca_id = Category.objects.get(name=original_category)
	
	list_for_copy = MyShortCut.objects.filter(Q(author=user_id) & Q(category = ca_id))

	category = Category.objects.get(id=destination_category)

	for p in list_for_copy:
		profile = MyShortCut.objects.create(
			author = request.user,
			title = p.title,
			content1 = p.content1,
			content2 = p.content2,
			type_id = p.type_id,
			category = category,
		)
	return JsonResponse({
		'message': author+'의 '+ original_category +'를 나의 ' +destination_category +'로 복사 했습니다',
	})
	
def search_by_id_and_word(request):
	
	search_user_id = request.POST['search_user_id']

	if(search_user_id == "all"):
		search_word = request.POST['search_word']
		object_list = MyShortCut.objects.filter(Q(title__icontains=search_word)).order_by('-created')
		print("search_user_id : ", search_user_id)
		print("search_word : ", search_word)
		print("object_list : ", object_list)
		
		return render(request, 'wm/MyShortCut_list_for_search.html', {
			'object_list': object_list
		})				
	else:
		user = User.objects.get(username=search_user_id)
		
		search_word = request.POST['search_word']
		object_list = MyShortCut.objects.filter(Q(title__icontains=search_word) & Q(author=user)).order_by('-created')
		
		print("search_user_id : ", search_user_id)
		print("search_word : ", search_word)
		print("object_list : ", object_list)
		
		return render(request, 'wm/MyShortCut_list_for_search.html', {
			'object_list': object_list
		})
	

def delete_comment_for_my_shortcut(request, shortcut_comment_id):
    print('shortcut_comment_id : ' , shortcut_comment_id)
    co = CommentForShortCut.objects.filter(id=shortcut_comment_id).delete()

    return JsonResponse({
        'message': '댓글 삭제 성공',
    })

def update_comment_for_my_shortcut(request, shortcut_comment_id):
    print('shortcut_comment_id : ' , shortcut_comment_id)
    co = CommentForShortCut.objects.filter(id=shortcut_comment_id).update(
        title= request.POST['title'],
        content = request.POST['content']
    )

    return JsonResponse({
        'message': '댓글 수정 성공',
    })

def new_comment_for_my_shortcut(request, shortcut_id):
    print('shortcut_id : ' , shortcut_id)
    shortcut = MyShortCut.objects.get(id=shortcut_id)
    co = CommentForShortCut.objects.create(
        shortcut= shortcut,
        author = request.user,
        title="default title",
        content = "default content"
    )

    return JsonResponse({
        'message': shortcut.title+ '에 대해 comment 추가 성공 ',
        'comment_id':co.id,
        'comment_title':co.title,
        'comment_content':co.content,
    })

def create_new4_textarea(request):
    print("create_new4_textarea 실행")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    # title = request.POST['title']

    wm1 = MyShortCut.objects.create(
        author = request.user,
        title="title1",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm2 = MyShortCut.objects.create(
        author = request.user,
        title="title2",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm3 = MyShortCut.objects.create(
        author = request.user,
        title="title3",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm4 = MyShortCut.objects.create(
        author = request.user,
        title="title4",
        type= ty,
        category = ca,
        content2 = ""
    )
    wm5 = MyShortCut.objects.create(
        author = request.user,
        title="title5",
        type= ty,
        category = ca,
        content2 = ""
    )

    print("wm1 : ", wm1)

    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm1.id,
        'shortcut_title':wm1.title,
        'shortcut_content2':wm1.content2,
    })

# myshortcut_row, shorcut_id, shorcut_content
def create_new1_input(request):
    print("create_new1_input 실행")
    ty = Type.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = ""
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content':wm.content1,
    })

def create_new2_textarea(request):
    print("create_new2_textarea 실행")
    ty = Type.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = Category.objects.get(id=category_id)
    title = request.POST['title']

    wm = MyShortCut.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content2 = ""
    )
    print("wm : ", wm)
    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':wm.id,
        'shortcut_title':wm.title,
        'shortcut_content2':wm.content2,
    })

def update_category_by_ajax(request):
    shortcut_ids = request.POST.getlist('shortcut_arr[]')
    category = request.POST['category']

    if shortcut_ids:
        MyShortCut.objects.filter(pk__in=shortcut_ids, author=request.user).update(category=category)

    return redirect('/wm/myshortcut')

def delete_myshortcut_by_ajax(request):
    shortcut_ids = request.POST.getlist('shortcut_arr[]')
    if shortcut_ids:
        MyShortCut.objects.filter(pk__in=shortcut_ids, author=request.user).delete()

    return redirect('/wm/myshortcut')


def update_my_shortcut_subject(request):
    if request.method == "POST" and request.is_ajax():
        shortcut_subject = request.POST['shortcut_subject']

        print('update shortcut_subject : ',shortcut_subject)
        pf = Profile.objects.filter(user=request.user).update(subject_of_memo = shortcut_subject)

        print('shortcut_subject success : ' , shortcut_subject);

        return JsonResponse({
            'message': 'shortcut_subject update 성공 : ' +shortcut_subject
        })
    else:
        return redirect('/wm/shortcut')

def user_list_for_memo(request):
    if request.method == 'GET':
        user_list = User.objects.all()

        return render(request, 'wm/user_list_for_memo.html', {
            "user_list" : user_list
        })
    else:
        return HttpResponse("Request method is not a GET")

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

def update_shortcut_nick2(request):
    if request.method == "POST" and request.is_ajax():
        ca_id = CategoryNick.objects.get(author=request.user).id
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
            author=user,
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

    def form_valid(self, form):
        form = form.save(commit=False)
        form.save()
        return HttpResponseRedirect(reverse('wm:my_shortcut_list'))

    def get_template_names(self):
        return ['wm/myshortcut_summernote_form.html']

def update_shorcut_id_for_user(request, id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        user_id = request.POST['user_id']
        original_userId = id
        option=""
        original_user = ""

        user_exist = User.objects.filter(username = user_id)
        original_user = user_id
        print("user_exist : ", user_exist)

        if user_exist:
            option = "메모장 유저를 " + user_id + "로 업데이트 하였습니다."
            todo = Profile.objects.filter(Q(user=id)).update(shortcut_user_id = user_id)
            print("메모장 유저를 {}로 교체 ".format(user_id))
        else:
            original_user = User.objects.get(id = original_userId).username
            print("original_user : ", original_user)
            option = user_id+ "유저가 없으므로 업데이트를 하지 않았습니다."
            print("유저를 업데이트 하지 않았습니다.")

        return JsonResponse({
            'message': option,
            'original_id': original_user
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
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        pf = Profile.objects.filter(Q(user=self.request.user)).update(selected_category_id = category.id)
        print('category id update 성공')

        print("user 정보 : ", )

        user = User.objects.get(Q(username = self.request.user.profile.shortcut_user_id))

        print('user : ' , user)

        return MyShortCut.objects.filter(category=category, author=user).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
        user = User.objects.get(Q(username = self.request.user.profile.shortcut_user_id))

        context = super(type(self), self).get_context_data(**kwargs)
        context['posts_without_category'] = MyShortCut.objects.filter(category=None,author=user).count()
        context['category_list'] = Category.objects.all()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category
            context['category_nick'] = CategoryNick.objects.values_list(slug, flat=True).get(author=user)

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

def update_shortcut_ajax(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = MyShortCut.objects.filter(Q(id=id)).update(title=title)
        print('MyShortCut update 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 업데이트 성공',
            'title':title
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

            cn = CategoryNick.objects.get_or_create(
                author=self.request.user,
            )

            context = super(MyShortCutListView, self).get_context_data(**kwargs)
            context['category_list'] = Category.objects.all()

            category = Category.objects.get(id=self.request.user.profile.selected_category_id)
            context['category'] = category
            context['category_nick'] = CategoryNick.objects.values_list(category.slug, flat=True).get(author=self.request.user)

            context['posts_without_category'] = MyShortCut.objects.filter(category=None, author=self.request.user).count()
            # context['comments_list'] = CommentForShorCut.objects.all()

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
