from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import RegistrationForm, CategoryForm, PostForm
from .models import Post, Category

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        # query post yang statusnya 1 = published
        posts = Post.objects.filter(status=1).order_by('id')
        categories = Category.objects.all().order_by('name')
        return render(request, self.template_name, {'posts':posts, 'categories':categories})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'


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
        try:
            category = Category.objects.get(id=id)
            form = CategoryForm(instance=category)
            return render(request, self.template_name, {'form':form, 'category':category})
        except Exception as error:
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


class PostAllView(LoginRequiredMixin, ListView):
    model=Post
    template_name='post/post_list.html'


class PostEditView(LoginRequiredMixin, TemplateView):
    template_name = 'post/post_edit.html'
    id = None

    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
            form = PostForm(instance=post)
            return render(request, self.template_name, {'form':form, 'post':post})
        except Exception as error:
            messages.error(request, error)
            return HttpResponseRedirect(reverse('post-all'))

    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                updated_post = form.save()
                messages.success(request, "Post successfully updated")
                return HttpResponseRedirect(reverse('post-all'))
            else:
                messages.error(request, "Please correct your input")
                return render(request, self.template_name, {'form':form, 'post':post} )
        except Exception as error:
                messages.error(request, error)
                return render(request, self.template_name, {'form':form, 'post':post} )


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request):
        return render(request, self.template_name)