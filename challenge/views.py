from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView , DeleteView
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Q
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .models import LecRecord, LecInfo
# from .forms import BestLecForm
from django.contrib.auth.mixins import LoginRequiredMixin

class RecordUpdateView(UpdateView):
    pass

class RecordDeleteView(DeleteView):
    model = LecRecord
    success_url = reverse_lazy('challenge:lec_record_list')
    success_message = "record is removed"

    def delete(self, request, *args, **kwargs):
            messages.success(self.request, self.success_message)
            return super(RecordDeleteView, self).delete(request, *args, **kwargs)

# best20_delete = Best20DeleteView.as_view()


class LecRecordListView(LoginRequiredMixin,ListView):
    model = LecRecord
    paginate_by = 20
    ordering = ['-created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LecRecordListView, self).get_context_data(**kwargs)
        context['LecInfo'] = LecInfo.objects.get(id=1)
        return context
# list_display = ['id', 'author','current_class', 'perfection', 'note' , 'git_url' , 'created']


class CreateRecordView(CreateView):
    model = LecRecord
    fields = ['current_class','perfection','note', 'git_url']

    def form_valid(self, form):
        print("CreateRecordView 실행")
        fn = form.save(commit=False)
        fn.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('challenge:lec_record_list')
