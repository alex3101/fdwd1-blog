from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'management/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)