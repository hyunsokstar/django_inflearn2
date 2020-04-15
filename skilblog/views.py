from django.shortcuts import render , get_object_or_404, redirect, resolve_url
from .models import SkilBlogTitle, SkilBlogContent, LikeForSkilBlogTitle, CommentForSkilBlogTitle
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from .forms import SkilBlogContentForm
from wm.models import Type
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ModifySkilBlogTitleForm
from django.db.models import F

# Create your views here.

# 1122
# modify_comment_for_sbt

def modify_comment_for_sbt(request):

    comment_id = request.POST['comment_id']
    comment_text_for_modify = request.POST['comment_text_for_modify']
    cfbt=CommentForSkilBlogTitle.objects.filter(Q(id=comment_id)).update(content = comment_text_for_modify)

    return JsonResponse({
        'message': '댓글 수정 성공',
        'comment_id':comment_id,
        'comment_text_for_modify':comment_text_for_modify,
    })

def delete_comment_for_sbt(request):

    comment_id = request.POST['comment_id']
    ckbt=CommentForSkilBlogTitle.objects.filter(Q(id=comment_id)).delete()

    return JsonResponse({
        'message': '댓글 삭제 성공',
        'comment_id':comment_id,
    })

def insert_comment_for_sbt(request):
    sbt_id = request.POST['sbt_id']
    sbt =  get_object_or_404(SkilBlogTitle, pk=sbt_id)
    content = request.POST['content']

    comment = CommentForSkilBlogTitle.objects.create(author=request.user, sbt = sbt, content = content)

    return JsonResponse({
        'message': '댓글 입력 성공',
        'id':comment.id,
        'content':comment.content,
        'author':comment.author.username,
        'created_at':comment.created_at
    })

def like_skil_blog_title(request, id):
    print('id : ', id)
    sbt =  get_object_or_404(SkilBlogTitle, pk=id)
    like_count = LikeForSkilBlogTitle.objects.filter(Q(author=request.user) & Q(sbt=sbt)).count()
    print("내가 강의 추천한 개수 : ", like_count)

    if like_count < 1:
        sbt = LikeForSkilBlogTitle.objects.create(author=request.user, sbt = sbt)
        SkilBlogTitle.objects.filter(Q(id=id)).update(reputation = F('reputation') + 1)
        print('좋아요 추가')
    else:
        LikeForSkilBlogTitle.objects.filter(Q(author=request.user) & Q(sbt=sbt)).delete()
        SkilBlogTitle.objects.filter(Q(id=id)).update(reputation = F('reputation') + -1)
        print('추천을 삭제')
    return HttpResponseRedirect(reverse_lazy('skilblog:SkilBlogTitleList'))

class modify_skil_blog_title_list(UpdateView):
    model = SkilBlogTitle
    form_class = ModifySkilBlogTitleForm

    def get_object(self, queryset=None):
        sbt = super(modify_skil_blog_title_list, self).get_object()
        if sbt.author != self.request.user:
            raise PermissionError('수정 권한이 없습니다.')
        return sbt

class delete_skil_blog_title_list(DeleteView):
    model = SkilBlogTitle
    success_url = reverse_lazy('skilblog:SkilBlogTitleList')
    success_message = "SkilBlogTitleList 항목이 삭제 되었습니다."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(delete_skil_blog_title_list, self).delete(request, *args, **kwargs)

class modify_skilblog_content2_by_summernote(UpdateView):
    model = SkilBlogContent
    form_class = SkilBlogContentForm

    def get_template_names(self):
        return ['skilblog/SkilBlogContent_summernote_form.html']

    def form_valid(self, form):
        form = form.save(commit=False)
        form.save()
        sbc_id = self.kwargs['pk']
        sbt_id= SkilBlogContent.objects.get(id = sbc_id).sbt.id

        return HttpResponseRedirect(reverse('skilblog:SkilBlogContentList', kwargs={'id':sbt_id}))


def edit_skil_blog_for_content2(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('skilblogcontent의 content2를 modify')
        print('id : ', id)
        print("content2 : ", content2)
        todo = SkilBlogContent.objects.filter(Q(id=id)).update(content2 = content2)
        print('update 성공');

        return JsonResponse({
            'message': 'skil blog 내용 수정 성공',
        })
    else:
        return redirect('/todo')

def edit_skil_blog_for_content1(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')
        print('skilnotecontent를 ajax로 update')
        print('id : ', id)
        print("content1 : ", content1)
        todo = SkilBlogContent.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': 'skilblog content업데이트 성공',
        })
    else:
        return redirect('/todo')

class createViewForSkillBlogContentUsingSummerNote(CreateView):
    model = SkilBlogContent
    form_class = SkilBlogContentForm

    def get_template_names(self):
        return ['skilblog/SkilBlogContent_summernote_form.html']

    def form_valid(self, form):
        print("createViewForSkillBlogContentUsingSummerNote 클래스뷰 실행");
        ty = Type.objects.get(type_name="summer_note")
        skil_blog_title_id = self.kwargs['skil_blog_title_id']
        print("skil_blog_title_id : ", skil_blog_title_id)
        # sbt = get_object_or_404(SkilBlogTitleList, id=skil_blog_title_id)
        sbt=SkilBlogTitle.objects.get(id=skil_blog_title_id)

        sb = form.save(commit=False)
        sb.sbt= sbt
        sb.author = self.request.user
        sb.type= ty

        return super().form_valid(form)

    def form_invalid(self):
        print("form이 유효하지 않다.")

    def get_success_url(self):
        return reverse('skilblog:SkilBlogContentList', kwargs={'id':self.kwargs['skil_blog_title_id']})



def delete_sbc_content(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = SkilBlogContent.objects.filter(Q(id=id)).delete()
        print('MyShortCut delete 성공 id : ' , id);
        return JsonResponse({
            'message': '스킬 블로그 콘텐트 삭제 성공',
        })
    else:
        return redirect('/todo')

def sbc_modify(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = SkilBlogContent.objects.filter(Q(id=id)).update(title=title)
        print('스킬 블로그 내용 수정 성공 id : ' , id);
        return JsonResponse({
            'message': '스킬 블로그 내용 수정 성공',
            'title':title
        })
    else:
        return redirect('/todo')

class SkilBlogTitleList(LoginRequiredMixin,ListView):
    model = SkilBlogTitle
    paginate_by = 10
    user = 0

    def get_queryset(self):
        return SkilBlogTitle.objects.all().order_by('-created')

def SkilBlogContentList(request,id):
    print('SkilBlogTitle id : ',id)

    # sbt = skil blog title
    sbt= SkilBlogTitle.objects.get(id = id)
    print("title : ", sbt.title)
    sbc = SkilBlogContent.objects.filter(Q(sbt=sbt)).order_by('-created')
    print("sbc : ", sbc)

    return render(request, 'skilblog/SkilBlogContentList.html', {
        "sbc": sbc,
        "sbt":sbt,
        "title":sbt.title,
        "author":sbt.author,
        "skil_blog_title_id":id
    })
