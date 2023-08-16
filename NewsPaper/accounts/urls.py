from django.urls import path

from .views import ProfileView, upgrade_me

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='user_detail'),
    path('upgrade/', upgrade_me, name='upgrade'),
]