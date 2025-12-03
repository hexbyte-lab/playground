from django.conf.urls.static import static
from django.urls import path

from Login_System import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_user/', views.login_user, name='login-user'),
    path('logout_user/', views.logout_user, name='logout-user'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change-password')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
