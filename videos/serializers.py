from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['creator', 'created_at']
