from rest_framework import permissions

class isOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner==request.user or request.user.is_superuser
        
        # return False

# class isAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):

#         if request.user.is_superuser:
#             return True
        
#         return obj.owner==request.user

class commentPermision(permissions.BasePermission):
    
    def has_object_permission(self, request,view,obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner==request.user or obj.post.owner==request.user or request.user.is_superuser