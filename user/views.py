from django.shortcuts import render,redirect
from .models import BaseUser
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from .forms import UserForm,CustomPasswordChangeForm,UserFilterForm
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.

# User List View
class UserListView(LoginRequiredMixin, ListView):
    model = BaseUser
    template_name = 'user_list.html'
    context_object_name = 'users'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        users = BaseUser.objects.filter(
            Q(username__icontains=search_query) |
            Q(firstname__icontains=search_query) |
            Q(lastname__icontains=search_query) |
            Q(gender=search_query)
        ).filter(is_superuser=False)
        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_filter_form'] = UserFilterForm(self.request.GET)
        return context

# Add User View
class AddUserView(LoginRequiredMixin, CreateView):
    model = BaseUser
    form_class = UserForm
    template_name = 'add_user.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        # Hash the password
        user.set_password(form.cleaned_data['password'])
        assigned_user_id = self.request.POST.get('assigned', None)
        if assigned_user_id:
            user.assigned = BaseUser.objects.get(pk=assigned_user_id)
        else:
            user.assigned = None
        user.save()
        return redirect('user_list')

# Edit User View
class EditUserView(LoginRequiredMixin, UpdateView):
    model = BaseUser
    form_class = UserForm
    template_name = 'edit_user.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        print('form is valid')
        user = form.save(commit=False)

        # Check if assigned user is empty or None
        assigned_user_id = self.request.POST.get('assigned', None)
        if assigned_user_id:
            user.assigned = BaseUser.objects.get(pk=assigned_user_id)
        else:
            user.assigned = None
        
        # Check if a new photo was uploaded
        if 'photo' in self.request.FILES:
            user.photo = self.request.FILES['photo']    
        else:
            # No new photo uploaded, so preserve the existing one
            user.photo = user.photo  # This line ensures the existing photo 
        
        user.save()
        return super().form_valid(form)

# Change Password View
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('user_list')
    login_url = reverse_lazy('login')

# Delete User View
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = BaseUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('user_list')
    login_url = reverse_lazy('login')
