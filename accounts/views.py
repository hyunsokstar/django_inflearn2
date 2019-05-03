from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

def signup(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():    # 입력한 값이 있을 경우 True를 반환
            user = form.save()
            return redirect(settings.LOGIN_URL)
    else:   # 입력한 값이 없을 경우
        form = UserCreationForm()
    return render(request, 'accounts/signup_form.html',{
        'form':form,
    })
# Create your views here.
def profile(request):
    return render(request, 'accounts/profile.html')
