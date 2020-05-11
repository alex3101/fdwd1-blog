from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RegistrationForm, CategoryForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # mengambil input dari form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, self.template_name, {'form':form})

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'management/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class CategoryAddView(LoginRequiredMixin, TemplateView):
    template_name = 'management/category_form.html'

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, self.template_name, {'form':form})



class PostCreateView(TemplateView):
    pass
    # using ModelForm

class PostAllView(ListView):
    pass
    # using ListView