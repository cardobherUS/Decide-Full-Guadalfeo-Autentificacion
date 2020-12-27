from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, IndexUserView, LoginUserView, RegisterView, RegisterUserView


urlpatterns = [
    path('index/', IndexUserView.as_view()),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('auth/login/', LoginUserView.as_view()),
    path('auth/register/', RegisterUserView.as_view()),
]
