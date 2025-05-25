from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .models import Video
from .serializers import VideoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Video, Purchase
from .forms import VideoUploadForm, SignUpForm
from .forms import VideoForm  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django import forms
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Video, Profile, VideoPurchase
from .forms import CommentForm
from .models import Comment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Wallet
from django.utils.timezone import now


class UploadVideoView(LoginRequiredMixin, View):
    def get(self, request):
        form = VideoForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.creator = request.user
            video.save()
            return redirect('video_list') 
        return render(request, 'upload.html', {'form': form})

class VideoFeedView(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    
    
def home(request):
    videos = Video.objects.order_by('-created_at')[:6]  
    return render(request, 'home.html', {'videos': videos})

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Video, Wallet, Purchase
from django.contrib import messages

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 400})

    user_purchased = Purchase.objects.filter(user=request.user, video=video).exists()

    if request.method == 'POST':
        if user_purchased or video.price == 0:
            messages.info(request, "You already own this video or it is free.")
        else:
            if wallet.balance >= video.price:
                wallet.balance -= video.price
                wallet.save()
                uploader_wallet, created = Wallet.objects.get_or_create(user=video.uploaded_by, defaults={'balance': 400})
                uploader_wallet.balance += video.price
                uploader_wallet.save()

                Purchase.objects.create(user=request.user, video=video)
                messages.success(request, "Purchased successfully!")
                user_purchased = True
            else:
                messages.error(request, "Insufficient balance.")

        return redirect('video_detail', video_id=video.id)

    return render(request, 'video_detail.html', {
        'video': video,
        'wallet': wallet,
        'user_purchased': user_purchased,
    })



@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.creator = request.user
            video.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def purchase_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    Purchase.objects.get_or_create(user=request.user, video=video)
    return redirect('video_detail', video_id=video.id)

@login_required
def profile(request):
    user_videos = Video.objects.filter(creator=request.user)
    purchased_videos = Video.objects.filter(purchase__user=request.user)
    return render(request, 'profile.html', {'user_videos': user_videos, 'purchased_videos': purchased_videos})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@login_required
def buy_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    profile = request.user.profile
    price = video.price

    if profile.wallet_balance >= price:
        profile.wallet_balance -= price
        profile.save()
        VideoPurchase.objects.create(user=request.user, video=video)
        messages.success(request, "Video purchased successfully!")
    else:
        messages.error(request, "Insufficient balance!")

    return redirect('video_detail', video_id=video.id)

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    wallet = Wallet.objects.get(user=request.user)
    user_purchased = Purchase.objects.filter(user=request.user, video=video).exists()

    if request.method == 'POST' and not (user_purchased or video.price == 0):
        if wallet.balance >= video.price:
            wallet.balance -= video.price
            wallet.save()

            Purchase.objects.create(user=request.user, video=video)

            messages.success(request, f'You have successfully purchased "{video.title}". Enjoy watching!')
            user_purchased = True  
        else:
            messages.error(request, 'Insufficient wallet balance. Please add funds.')

    context = {
        'video': video,
        'wallet': wallet,
        'user_purchased': user_purchased,
    }
    return render(request, 'video_detail.html', context)




def short_videos(request):
    short_videos = Video.objects.filter(video_type='short')
    return render(request, 'short_videos.html', {'videos': short_videos})

@login_required
@csrf_exempt
def delete_video(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id, creator=request.user)
        video.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
        
@login_required
def wallet_view(request):
    wallet = getattr(request.user, 'wallet', None)
    return render(request, 'wallet.html', {'wallet': wallet})