from django.db import models
from users.models import CustomUser
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Video(models.Model):
    VIDEO_TYPE_CHOICES = (
        ('short', 'Short Form'),
        ('long', 'Long Form'),
    )
    
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # Price in ₹
    description = models.TextField()
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES)
    video_file = models.FileField(upload_to='videos/')
    duration = models.FloatField(null=True, blank=True)  # Duration in minutes or seconds?
    video_url = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='video_thumbnails/', null=True, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)  # ₹500 default

    def __str__(self):
        return f"{self.user.username}'s Wallet - ₹{self.balance}"

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'video')  # Prevent duplicate purchases

    def __str__(self):
        return f"{self.user.username} purchased {self.video.title}"


class Gift(models.Model):
    gifter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='gifts_given')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    
class VideoPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance) 