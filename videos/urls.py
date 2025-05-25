from django.urls import path
from .views import UploadVideoView, VideoFeedView
from . import views
from django.contrib.auth import views as auth_views
from .views import wallet_view
urlpatterns = [
    # define user-related API endpoints here later
    path('upload/', UploadVideoView.as_view(), name='upload_video'),
    path('feed/', VideoFeedView.as_view(), name='video_feed'),
      
    path('', views.home, name='home'),
    path('videos/', views.video_list, name='video_list'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_video, name='upload_video'),
    path('purchase/<int:video_id>/', views.purchase_video, name='purchase_video'),
    path('profile/', views.profile, name='profile'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
     path('upload/', UploadVideoView.as_view(), name='upload_video'),
    path('shorts/', views.short_videos, name='short_videos'),
    path('video/delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('wallet/', wallet_view, name='wallet'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('wallet/', views.wallet_view, name='wallet'),
    

]
