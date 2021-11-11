from django.urls import path, include
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

from .views import RegisterAPI, LoginAPI, UserViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'user_profile', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view(), name='auth_register'),
    path('login/', LoginAPI.as_view(), name='login_user'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
]
