from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Q
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .models import StudentRecord, LecInfo , RecommandLecInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LecInfoForm

# 1122

def recommand_lecture(request, id):
    lecture =  get_object_or_404(LecInfo, pk=id)
    recommand_count = RecommandLecInfo.objects.filter(Q(author=request.user) & Q(lecinfo=lecture)).count()
    print("내가 강의 추천한 개수 : ", recommand_count)
    print('id : ', id)

    id = str(id)

    if recommand_count < 1:
        lecinfo = RecommandLecInfo.objects.create(author=request.user, lecinfo= lecture)
        print('추천을 추가')
    else:
        RecommandLecInfo.objects.filter(Q(author=request.user) & Q(lecinfo=lecture)).delete()
        print('추천을 삭제')

    return redirect("/challenge/"+id)
    # return reverse('challenge:lec_record_list', kwargs={'classification': id})



class CreatelecInfo(CreateView):
    model = LecInfo
    fields = ['lec_name','teacher', 'lec_url','git_url','start_time','deadline']
    success_message = "강의 정보 기록을 입력하였습니다."

    def form_valid(self, form):

        print("CreateRecordView 실행")
        fn = form.save(commit=False)
        fn.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        classnum = self.kwargs['classification']
        return reverse('challenge:lecinfo_list')

class RecordUpdateView(UpdateView):
    model = StudentRecord
    fields = ['current_class']
    success_url = reverse_lazy('challenge:lec_record_list')
    success_message = "record is modified"

    def get_success_url(self):
        classnum = self.kwargs['classification']
        return reverse('challenge:lec_record_list', kwargs={'classification': classnum})


class LecInfoUpdateView(UpdateView):
    model = LecInfo
    fields = ['lec_name','teacher','lec_url','git_url']

    def get_success_url(self):
        classnum = self.kwargs['classification']
        return reverse('challenge:lec_record_list', kwargs={'classification': classnum})


class RecordDeleteView(DeleteView):
    model = StudentRecord
    success_message = "record is removed"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RecordDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        classnum = self.kwargs['classification']
        return reverse('challenge:lec_record_list', kwargs={'classification': classnum})

class LecRecordListView(LoginRequiredMixin,ListView):
    model = StudentRecord
    paginate_by = 20
    ordering = ['-created']

    def get_queryset(self):
        print("PostSearch 확인")
        classnum = self.kwargs['classification']
        object_list = StudentRecord.objects.filter(classification=classnum).order_by('-created')
        print("result : ", object_list)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        classnum = self.kwargs['classification']
        lec_info = LecInfo.objects.get(id=classnum)
        context = super(LecRecordListView, self).get_context_data(**kwargs)
        context['LecInfo'] = lec_info
        context['recommnad_count'] = RecommandLecInfo.objects.filter(lecinfo=lec_info).count()

        return context

class LecInfoListView(LoginRequiredMixin,ListView):
    model = LecInfo
    paginate_by = 20

class CreateRecordView_11(CreateView):
    model = StudentRecord
    fields = ['current_class','github_url']
    success_message = "강의 수강 기록을 입력하였습니다."

    def form_valid(self, form):
        classnum = self.kwargs['classification']

        print("CreateRecordView 실행")
        fn = form.save(commit=False)
        fn.author = self.request.user

        lec = LecInfo.objects.get(id=classnum)
        fn.classification = lec

        return super().form_valid(form)

    def get_success_url(self):
        classnum = self.kwargs['classification']
        return reverse('challenge:lec_record_list', kwargs={'classification': classnum})
