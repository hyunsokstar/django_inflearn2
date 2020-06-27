from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from . forms import SignupForm
from django.contrib.auth import login as auth_login
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from wm.models import RecommandationUserAboutSkillNote
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q


from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as AuthPasswordChangeView,
)


def delete_login_user(request):
    if request.method == "POST" and request.is_ajax():
        userId = request.POST['userId']
        print("userId : ", userId)
        result1 = RecommandationUserAboutSkillNote.objects.filter(Q(author_id=userId)).delete()
        result2 = User.objects.filter(Q(username=userId)).delete()
        print('회원 정보 삭제 (좋아요 목록 삭제 성공) ' , result1);
        print('회원 정보 삭제 (회원 정보 삭제 성공) ' , result2);

        return JsonResponse({
            'message': '좋아요 정보 유저 정보 삭제 성공 ',
        })
    else:
        return redirect('/wm/myshorcut/')

def user_profile_information_view(request,user):
    print("my_profile_information_view 실행")
    print("my_profile_information_view 실행 user : ", user)

    # profile_user = User.objects.filter(username=user)
    profile_user = User.objects.get(username=user)
    profile_user_id = profile_user.id
    print("profile_user : ", profile_user)
    print("profile_user_id : ", profile_user_id)

    user_favorite = [] # 유저가 좋아하는 사람 목록 담을 배열
    user_favorite_list = RecommandationUserAboutSkillNote.objects.filter(author_id=profile_user) # 유저가 좋아하는 사람 목록 검색

    print("user_favorite_list : ", user_favorite_list)


    for x in user_favorite_list:
        print("내가 추천한 user_id : ",x.user_id)
        user_favorite.append(x.user_id)

    my_favorite_user_list = User.objects.filter(id__in=user_favorite).order_by('-profile__skill_note_reputation');
    print("my_favorite_user_list : ", my_favorite_user_list)

    return render(request, 'accounts2/user_profile.html', {
        "profile_user" : profile_user,
        "my_favorite_user_list" : my_favorite_user_list,
    })


def update_for_profile(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        profile_user = request.POST.get('profile_user','')
        profile_email = request.POST.get('profile_email','')
        profile_public = request.POST.get('profile_public','')
        profile_github = request.POST.get('profile_github','')
        profile_site1 = request.POST.get('profile_site1','')
        profile_site2 = request.POST.get('profile_site2','')
        profile_site3 = request.POST.get('profile_site3','')
        profile_site4 = request.POST.get('profile_site4','')
        profile_id = request.POST.get('profile_id','')

        print("update_for_profile (view) 실행")

        user_exists = User.objects.get(username = profile_user)
        print("user_exists : ", user_exists)

        if(user_exists !=None and user_exists.username!=request.user.username):
            return JsonResponse({
                'message':'업데이트 실패 , user 중복'
            })


        user = User.objects.filter(username=request.user.username).update(username=profile_user)
        print("user : ", user)

        profile = Profile.objects.filter(id=profile_id).update(
            email = profile_email,
            public = profile_public,
            github = profile_github,
            site1 = profile_site1,
            site2 = profile_site2,
            site3 = profile_site3,
            site4 = profile_site4)
        print('update_for_profile Success !!!!!!!!!');

        return JsonResponse({
            'message': 'MyProfile Update Success',
        })
    else:
        return redirect('/todo')

class my_profile_information_view(LoginRequiredMixin,ListView):
    paginate_by = 10
    # if 'q' in request.GET:
    #     query = request.GET.get('q')
    #     print("query : ", query)

    def get_template_names(self):
        if self.request.is_ajax():
            print("user list ajax 요청 확인")
            return ['accounts2/my_profile.html']
        return ['accounts2/my_profile.html']


    def get_queryset(self):
        print("my_profile_information_view 실행")
        # object_list = User.objects.all().order_by('-profile__skill_note_reputation');
        object_list = User.objects.filter(username=self.request.user);
        return object_list


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)

        my_favorite = []
        ru = RecommandationUserAboutSkillNote.objects.filter(author_id=self.request.user)

        for x in ru:
            print("내가 추천한 user_id : ",x.user_id)
            my_favorite.append(x.user_id)

        my_favorite_user_list = User.objects.filter(id__in=my_favorite).order_by('-profile__skill_note_reputation');
        print("my_favorite_user_list : ", my_favorite_user_list)


        context['my_favorite_user_list'] = my_favorite_user_list


        return context



class member_list_view(ListView):
    paginate_by = 20

    def get_template_names(self):
        if self.request.is_ajax():
            print("user list ajax 요청 확인")
            return ['wm/_user_list_for_memo.html']
        return ['wm/user_list_for_memo.html']

    def get_queryset(self):
        print("실행 확인 겟 쿼리셋")
        query = self.request.GET.get('q')
        print("query : ", query)

        if query != None:
            object_list = User.objects.all().filter(Q(username__contains=query))
            return object_list
        else:
            object_list = User.objects.all().order_by('-profile__skill_note_reputation');
            print("result : ", object_list)
            return object_list

member_list = member_list_view.as_view()


def logout(request):
    messages.success(request, '로그아웃되었습니다.')
    return logout_then_login(request)

def signup(request):
    print('회원 가입 뷰 실행 22')
    if request.method=="POST":
        form = SignupForm(request.POST)
        if form.is_valid():    # 입력한 값이 있을 경우 True를 반환
            user = form.save()

            auth_login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')
            redirect_url = request.GET.get("next",settings.LOGIN_REDIRECT_URL)

            return redirect(redirect_url)

    else:   # 입력한 값이 없을 경우
        form = SignupForm()
    return render(request, 'accounts2/signup_form.html',{
        'form':form,
    })


# Create your views here.
def profile(request):
    return render(request, 'accounts2/profile.html')
