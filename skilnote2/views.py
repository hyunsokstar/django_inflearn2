
from django.shortcuts import render

# Create your views here.

def SkilNote2List(request):

    print("샘플 페이지 출력")

    return render(request, 'skilnote2/SkilNote2List.html', {
	})
