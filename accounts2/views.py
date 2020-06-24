from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from . forms import SignupForm
from django.contrib.auth import login as auth_login
from django.views.generic import ListView
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as AuthPasswordChangeView,
)

def update_for_profile(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        profile_email = request.POST.get('profile_email','')
        profile_public = request.POST.get('profile_public','')
        profile_github = request.POST.get('profile_github','')
        profile_site1 = request.POST.get('profile_site1','')
        profile_site2 = request.POST.get('profile_site2','')
        profile_site3 = request.POST.get('profile_site3','')
        profile_site4 = request.POST.get('profile_site4','')
        profile_id = request.POST.get('profile_id','')

        print("update_for_profile (view) 실행")

        MyProfile = request.user.profile

        todo = Profile.objects.filter(id=profile_id).update(
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
