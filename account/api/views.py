from django.shortcuts import get_object_or_404
from ..models import CustomUser,Profile,blockusers
from .permisions import isOwnerOrReadonly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer,ProfileSerializer,profile_addSerializer
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
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,isOwnerOrReadonly]
    def list(self, request):
        
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        
            queryset = Profile.objects.all()
            profile = get_object_or_404(queryset,owner__pk=pk)
            blocklist=blockusers.objects.all()
            list=get_object_or_404(blocklist,user__pk=request.user.id)
            inst=CustomUser.objects.get(id=request.user.id)
            bl=inst.blocked_users.blockedusers.all()
            print("hiiii")
            print(inst.blocked_users.blockedusers.all())
            chekuser=CustomUser.objects.get(id=pk)
            # for user in list.blockedusers.values_list():
            #     print(user)
            if profile is not None:
                if  chekuser  in bl:
                    return Response({"msg":"you are bloked by user"})
                #profile = get_object_or_404(queryset, pk=pk)
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
            profile = get_object_or_404(queryset, owner__pk=pk)
            try:
                profile.delete()
            
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 
    
class followOrUnfollowViewset(APIView):
    def put(self,request,pk=None):
        print(request.user)
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Profile.objects.all()
            followed_by = get_object_or_404(queryset, owner__pk=pk)
        
            if not request.user in followed_by.followers:

                followed_by.followers.add(request.user)
                followed_by.save()
                queryset = Profile.objects.all()
                following = get_object_or_404(queryset, owner__pk=request.user.id)

                following.following.add(followed_by.owner)
                following.save()
            else:
                followed_by.followers.remove(request.user)
                followed_by.save()
                queryset = Profile.objects.all()
                following = get_object_or_404(queryset, owner__pk=request.user.id)

                following.following.remove(followed_by.owner)
                following.save()
            return Response(status=status.HTTP_200_OK)
