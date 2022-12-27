from rest_framework import serializers
from ..models import likes


class LikeSerializer(serializers.ModelSerializer):
    liked_by=serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=likes
        fields='__all__'