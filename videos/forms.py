from django import forms
from .models import Video
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from .models import Comment

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_type', 'video_file', 'video_url', 'price', 'image']

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_type', 'video_file', 'video_url', 'image', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter video title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter video description'}),
            'video_type': forms.Select(),
            'video_file': forms.ClearableFileInput(),
            'video_url': forms.URLInput(attrs={'placeholder': 'Enter video URL if not uploading a file'}),
            'image': forms.ClearableFileInput(),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

