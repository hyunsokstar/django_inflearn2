from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from . forms import SignupForm
from django.contrib.auth import login as auth_login
from django.views.generic import ListView

from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as AuthPasswordChangeView,
)


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
    return render(request, 'accounts/signup_form.html',{
        'form':form,
    })


# Create your views here.
def profile(request):
    return render(request, 'accounts/profile.html')
