from django.shortcuts import get_object_or_404
from ..models import CustomUser,Profile
from .permisions import isOwnerOrReadonly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer,ProfileSerializer
from rest_framework import filters, generics, serializers, status, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated                       



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

class UserListView(generics.ListAPIView):
    
    queryset = CustomUser.objects.all()
    serializer_class =RegisterSerializer

class profile_Viewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,isOwnerOrReadonly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    def list(self, request):
        
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        
            queryset = Profile.objects.all()
            profile = get_object_or_404(queryset,owner__pk=pk)
            if profile is not None:
            # profile = get_object_or_404(queryset, pk=pk)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            else:
                return Response(serializers.get_error_detail)
    serializer = ProfileSerializer()
    def perform_create(self,serializer_class):
        serializer_class.save(owner=self.request.user)

    def partial_update(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, owner__pk=pk)
        serializer=ProfileSerializer(profile,data=request.data,partial=True)
        if serializer.is_valid():
           serializer.save()
           return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, owner__pk=pk)
      
        serializer=ProfileSerializer(profile,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)

    def  destroy(self, request, pk=None):
            queryset = Profile.objects.all()
            book = get_object_or_404(queryset, owner__pk=pk)
            try:
                book.delete()
            
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 