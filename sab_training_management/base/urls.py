from django.urls import path
from .views import CustomLoginView, CustomRegistrationView
from . import views
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('',views.login),
    path('registration/', CustomRegistrationView.as_view(), name='registration'),
    path('registration/form1', views.form1),
]