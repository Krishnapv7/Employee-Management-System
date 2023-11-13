from django.urls import path
from .views import UserListView,EditUserView,AddUserView,DeleteUserView,ChangePasswordView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('user_list/',UserListView.as_view(),name='user_list'),
    path('add-user/',AddUserView.as_view(),name='add_user'),
    path('edit-user/<int:pk>/',EditUserView.as_view(),name='edit_user'),
    path('delete-user/<int:pk>/',DeleteUserView.as_view(),name='delete_user'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    
]



# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)