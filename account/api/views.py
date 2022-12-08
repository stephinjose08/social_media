from django.shortcuts import get_object_or_404
from ..models import CustomUser,Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer,ProfileSerializer
from rest_framework import filters, generics, serializers, status, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
                          



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateView(APIView):
    def post(self,request):
        username=request.data['username']
        if CustomUser.objects.filter(username=username).exists():
            return Response({"detail":"Username already exist try another"},status=status.HTTP_403_FORBIDDEN)
        else:
            serializer=RegisterSerializer(data=request.data)
            if serializer.is_valid():

                    account=serializer.save()
                    
                    refresh = RefreshToken.for_user(account)

                    return Response({
                        'username':account.username,
                    
                        'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    },status=status.HTTP_201_CREATED)
                    
                    #return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)


class profile_Viewset(viewsets.ModelViewSet):
    def list(self, request):
     
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        
            queryset = Profile.objects.all()
            profile = get_object_or_404(queryset, pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
    # serializer = ProfileSerializer()
    # def perform_create(self,request,serializer):
    #     # here you will send `created_by` in the `validated_data` 
        
    #     serializer.save(data=request.data,owner=self.request.user)
    #     return Response(status=status.HTTP_201_CREATED)
    def create(self,request):
        
        serializer=ProfileSerializer(data=request.data,owner=self.request.user)
        
        if serializer.is_valid():
           serializer.save()
           return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

