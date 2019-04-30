from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView,DetailView

# Create your views here.
class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')

    # 클래스뷰에서 리스트 객체 이외에 추가로 필요한 객체를 넘길때 get_context_data을 사용
    # context = super(PostList, self).get_context_data(**kwargs) 은 형식적으로 알아 두자
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        return context
