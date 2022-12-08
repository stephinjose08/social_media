from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from ..models import CustomUser,Profile
from django.contrib.auth.hashers import make_password



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

    
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone
        

        return token


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['phone', 'email', 'password','id','is_active']
        extra_kwargs={
            'password':{'write_only':True},
            'is_active':{'default':True}
        }
    def create(self, validated_data):
        pwd = validated_data.pop("password")
        instance=self.Meta.model(**validated_data)
        instance.set_password(pwd)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField()
    class Meta:
        model=Profile
        fields="__all__"
    def create(self, owner,validated_data):

        return Profile.objects.create(owner=owner.user,**validated_data)
        
   