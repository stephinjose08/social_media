from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from ..models import CustomUser,Profile,blockusers
from django.contrib.auth.hashers import make_password



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

    
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone
        

        return token
   
# class followlistSerializer(serializers.ModelSerializer):
#     owner=serializers.ReadOnlyField(source="owner.username")
#     class Meta:
#         model=followlist
#         fields="__all__"
class blockeduserSerializers(serializers.ModelSerializer):
    class Meta:
        model=blockusers
        fields='__all__'


class profile_addSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source="owner.username")
    
    class Meta:
        model=Profile
        exclude=('following','followers')
        # fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(source="owner.username")
    following=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    followers=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    
    class Meta:
        model=Profile
        #exclude=('following','followers')
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    profile_data=ProfileSerializer(read_only=True)
    bloked_users=serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    # followers=followlistSerializer(read_only=True,many=True)
    class Meta:
        model = CustomUser
        fields = ['username','phone', 'email', 'password','id','is_active','profile_data','bloked_users']
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


 
    
        
   