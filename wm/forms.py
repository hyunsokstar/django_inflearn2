from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import MyShortCut

# class Category(models.Model):
#     name = models.CharField(max_length=25, unique=True)
#     description = models.TextField(blank=True)
#     slug = models.SlugField(unique=True, allow_unicode=True)
#     author = models.ForeignKey(User, on_delete=True)

# class MyShortCut(models.Model):
#     category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)


# category 모델이 foreignkey인데
# 입력시 카테고리 선택 목록의 내용들에 (author = 본인)의 조건을 걸고 싶다.
class MyShortCutForm_input(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title', 'content1', 'category']

# class MyShortCutCreateView_input(LoginRequiredMixin,CreateView):
#     model = MyShortCut
#     form_class = MyShortCutForm_input
#     # fields = ['title','content1','category']
#
#     def form_valid(self, form):
#         print("완료 명단 입력 뷰 실행1")
#         ty = Type.objects.get(type_name="input")
#         ms = form.save(commit=False)
#         ms.author = self.request.user
#         ms.type= ty
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('wm:my_shortcut_list')
