from django.db import models
from post.models import Post,CustomUser
# Create your models here.

class likes(models.Model):
    post=models.ForeignKey(Post,related_name="likes",on_delete=models.CASCADE)
    likes_by=models.ForeignKey(CustomUser,related_name="liked_by",on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.post.caption

    
        