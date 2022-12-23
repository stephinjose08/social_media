
from rest_framework import serializers
from ..models import Post
from comments.api.serializers import CommentSerializer
from likes.api.serializers import LikeSerializer

class PostSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source="owner.username")
    comments=CommentSerializer(read_only=True,many=True)
    likes=LikeSerializer(read_only=True,many=True)
    number_of_likes=serializers.IntegerField(read_only=True)
    class Meta:
        model=Post
        fields="__all__"