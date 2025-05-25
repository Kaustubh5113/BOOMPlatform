from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    # define user-related API endpoints here later
     path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
