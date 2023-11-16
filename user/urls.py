from django.urls import path
from .views import UserListView,EditUserView,AddUserView,DeleteUserView,ChangePasswordView


urlpatterns = [
    path('user_list/',UserListView.as_view(),name='user_list'),
    path('add-user/',AddUserView.as_view(),name='add_user'),
    path('edit-user/<int:pk>/',EditUserView.as_view(),name='edit_user'),
    path('delete-user/<int:pk>/',DeleteUserView.as_view(),name='delete_user'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    
]



