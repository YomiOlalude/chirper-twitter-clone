from rest_framework import serializers

from chirper.settings import MAX_CHIRP_LENGTH
from .models import Chirp
from django.conf import settings

MAX_CHIRP_LENGTH = settings.MAX_CHIRP_LENGTH
CHIRP_ACTION_OPTIONS = settings.CHIRP_ACTION_OPTIONS

class ChirpActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in CHIRP_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action")
        return value

class ChirpCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Chirp
        fields = ["id", "content", "likes"]

    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        if len(value) > MAX_CHIRP_LENGTH:
            raise serializers.ValidationError("This Chirp is too long")
        return value

class ChirpSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = ChirpCreateSerializer(read_only=True)

    class Meta:
        model = Chirp
        fields = ["id", "content", "likes", "is_rechirp", "parent"]

    def get_likes(self, obj):
        return obj.likes.count()
    

