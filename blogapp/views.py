from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import RegistrationForm, CategoryForm
from .models import Post, Category

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
            messages.success(request, "Category successfully added")
            return HttpResponseRedirect(reverse('category-list'))
        else:
            messages.error(request, "Please correct your input")
            return render(request, self.template_name, {'form':form})


class CategoryEditView(LoginRequiredMixin, TemplateView):
    template_name = 'management/category_edit.html'
    id = None

    def get(self, request, id):
        category = Category.objects.get(id=id)
        if category:
            form = CategoryForm(instance=category)
            return render(request, self.template_name, {'form':form, 'category':category})
        else:
            messages.error(request, "Category can't be found")
            return HttpResponseRedirect(reverse('category-list'))

    def post(self, request, id):
        category = Category.objects.get(id=id)
        
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            updated_category = form.save()
            messages.success(request, "Category {0} successfully updated".format(updated_category.name))
            return HttpResponseRedirect(reverse('category-list'))
        else:
            
            messages.error(request, "There was an issue updating your category")
            return render(request, self.template_name, {'form':form})


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'management/category_list.html'
    # context_object_name = 'categories'

class PostCreateView(TemplateView):
    pass

class PostAllView(ListView):
    model=Post
    template_name='post/post_list.html'
    # using ListView
