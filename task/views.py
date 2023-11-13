from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from user.models import BaseUser
from .forms import TaskForm, TaskFilterForm
from user.forms import UserForm,CustomPasswordChangeForm,UserFilterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.models import Q


# Create your views here.

# Authentication Views
class Loginview(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

# Home View
class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'
    login_url = reverse_lazy('login')

    def get(self, request):
        if request.user.is_superuser:
            first_task = Task.objects.first()
            user_name = request.user.username if request.user else "Guest"
        else:
            first_task = Task.objects.filter(assigned=request.user)
            user_name = request.user.username if request.user else "Guest"
        context = {'task': first_task, 'user_name': user_name}
        return render(request, self.template_name, context)

# Task List View
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        is_superuser = self.request.user.is_superuser

        if is_superuser:
            tasks = Task.objects.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(date__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(assigned__firstname__icontains=search_query) |
                Q(assigned__lastname__icontains=search_query)
            )
        else:
            tasks = Task.objects.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(date__icontains=search_query) |
                Q(status__icontains=search_query)
            ).filter(assigned=self.request.user)

        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_filter_form'] = TaskFilterForm(self.request.GET)
        return context

# Add Task View
class AddTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'add_task.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        task = form.save(commit=False)
        assigned_user_id = self.request.POST.get('assigned', None)
        if assigned_user_id:
            task.assigned = BaseUser.objects.get(pk=assigned_user_id)
        else:
            task.assigned = None
        task.save()
        return redirect('task_list')

# Edit Task View
class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'edit_task.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        task = form.save(commit=False)
        assigned_user_id = self.request.POST.get('assigned', None)
        if assigned_user_id:
            task.assigned = BaseUser.objects.get(pk=assigned_user_id)
        else:
            task.assigned = None
        task.save()
        return redirect('task_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.object.id  # Pass the user's ID to the template
        return context
    
    
# Delete Task View
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'delete_task.html'
    success_url = reverse_lazy('task_list')
    login_url = reverse_lazy('login')
