from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from account.api.permisions import isOwnerOrReadonly
from ..models import Post
from .serializers import PostSerializer



class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,isOwnerOrReadonly]
    def list(self, request):
        
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        
            queryset = Post.objects.all()
            post = get_object_or_404(queryset,pk=pk)
            if post is not None:
            # profile = get_object_or_404(queryset, pk=pk)
                serializer = PostSerializer(post)
                return Response(serializer.data)
            else:
                return Response(serializers.get_error_detail)
    
    serializer = PostSerializer()
    def perform_create(self,serializer_class):
        serializer_class.save(owner=self.request.user)

    def partial_update(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, post)
        serializer=PostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
           serializer.save()
           return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, post)
        serializer=PostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    
    def  destroy(self, request, pk=None):
            print(request.user)
            queryset = Post.objects.all()
            post = get_object_or_404(queryset, pk=pk)
            self.check_object_permissions(request, post)
            try:
                post.delete()
            
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 