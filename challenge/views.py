from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Q
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .models import StudentRecord, LecInfo, RecommandLecInfo, challenge_subject
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LecInfoForm


# 1122
# 대주제는 챌린지 목록 소주제는 강의 목록
# LecInfoDeleteView
class LecInfoDeleteView(DeleteView):
	model = LecInfo
	success_message = "challenge is removed"

	def get_success_url(self):
		challenge_title = self.object.challenge.title
		print("challenge_title : ", challenge_title)
		return reverse('challenge:lecinfo_list_for_challenge', kwargs={'challenge_title':challenge_title})

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(LecInfoDeleteView, self).delete(request, *args, **kwargs)



def lecinfo_list_for_challenge(request, challenge_title):
	print ("challenge subject 과목 관련 리스트를 출력 합니다.")
	challenge = challenge_subject.objects.get (title=challenge_title)
	lecinfo_list = LecInfo.objects.filter (challenge=challenge)
	print ('lecinfo_list : ', lecinfo_list)

	return render (request, 'challenge/lecinfo_list.html', {
		"lecinfo_list": lecinfo_list,
		"challenge_title": challenge_title,
		"challenge_id":challenge.id
	})


# 할일 미완료 목록 리스트 출력
class ChallengeSubjectList (LoginRequiredMixin, ListView):
	model = challenge_subject
	paginate_by = 18
	template_name = 'challenge/challenge_list.html'


def challenge_list(request):
	return render (request, 'challenge/challenge_list.html', {
	})


def recommand_lecture(request, id):
	lecture = get_object_or_404 (LecInfo, pk=id)
	recommand_count = RecommandLecInfo.objects.filter (
		Q (author=request.user) & Q (lecinfo=lecture)).count ()
	print ("내가 강의 추천한 개수 : ", recommand_count)
	print ('id : ', id)

	id = str (id)

	if recommand_count < 1:
		lecinfo = RecommandLecInfo.objects.create (
			author=request.user, lecinfo=lecture)
		print ('추천을 추가')
	else:
		RecommandLecInfo.objects.filter (
			Q (author=request.user) & Q (lecinfo=lecture)).delete ()
		print ('추천을 삭제')

	return redirect ("/challenge/" + id)


# return reverse('challenge:lec_record_list', kwargs={'classification': id})


class CreatelecInfo (CreateView):
	model = LecInfo
	form_class = LecInfoForm
	success_message = "강의 정보 기록을 입력하였습니다."
	challenge_title = ""

	def get_template_names(self):
		return ['challenge/lecinfo_form.html']

	def form_valid(self, form):
		print ("CreateLecInfo 실행")
		fn = form.save (commit=False)
		fn.challenge = challenge_subject.objects.get(title=self.kwargs["challenge_title"])
		self.challenge_title = fn.challenge.title
		fn.manager = self.request.user
		return super ().form_valid (form)

	def get_context_data(self, **kwargs):
		ctx = super(CreatelecInfo, self).get_context_data(**kwargs)
		ctx['challenge_subject'] = self.kwargs["challenge_title"]
		return ctx

	def get_success_url(self):
		print("self.challenge_title : ", self.challenge_title)
		return reverse ('challenge:lecinfo_list_for_challenge', kwargs={'challenge_title':self.challenge_title})


class RecordUpdateView (UpdateView):
	model = StudentRecord
	fields = ['current_class']
	success_url = reverse_lazy ('challenge:lec_record_list')
	success_message = "record is modified"

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})


class LecInfoUpdateView (UpdateView):
	model = LecInfo
	fields = ['lec_name', 'manager', 'lec_url', 'git_url']

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})


class RecordDeleteView (DeleteView):
	model = StudentRecord
	success_message = "record is removed"

	def delete(self, request, *args, **kwargs):
		messages.success (self.request, self.success_message)
		return super (RecordDeleteView, self).delete (request, *args, **kwargs)

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})


class LecRecordListView (LoginRequiredMixin, ListView):
	model = StudentRecord
	paginate_by = 20
	ordering = ['-created']

	def get_queryset(self):
		print ("PostSearch 확인")
		classnum = self.kwargs['classification']
		object_list = StudentRecord.objects.filter (classification=classnum).order_by ('-created')
		print ("result : ", object_list)
		return object_list

	def get_context_data(self, *, object_list=None, **kwargs):
		classnum = self.kwargs['classification']
		lec_info = LecInfo.objects.get (id=classnum)
		context = super (LecRecordListView, self).get_context_data (**kwargs)
		context['LecInfo'] = lec_info
		context['recommnad_count'] = RecommandLecInfo.objects.filter (
			lecinfo=lec_info).count ()

		return context


class LecInfoListView (LoginRequiredMixin, ListView):
	model = LecInfo
	paginate_by = 20


	def get_context_data(self, *, object_list=None, **kwargs):
		classnum = self.kwargs['challenge_title']
		return context


class CreateRecordView_11 (CreateView):
	model = StudentRecord
	fields = ['current_class', 'github_url']
	success_message = "강의 수강 기록을 입력하였습니다."

	def form_valid(self, form):
		classnum = self.kwargs['classification']

		print ("CreateRecordView 실행")
		fn = form.save (commit=False)
		fn.author = self.request.user

		lec = LecInfo.objects.get (id=classnum)
		fn.classification = lec

		return super ().form_valid (form)

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})
