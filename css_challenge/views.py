from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CssImage

class CssImageList(LoginRequiredMixin,ListView):
    model = CssImage
    paginate_by = 10

    def get_template_names(self):
        return ['css_challenge/css_image_list.html']

css_image_list = CssImageList.as_view()
