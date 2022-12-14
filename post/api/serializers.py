
from rest_framework import serializers
from ..models import Post
from comments.api.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source="owner.username")
    comments=CommentSerializer(read_only=True,many=True)
    class Meta:
        model=Post
        fields="__all__"