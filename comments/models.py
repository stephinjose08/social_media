from django.db import models
from account.models import CustomUser
from post.models import Post
# Create your models here.


class Comment(models.Model):
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    comment=models.CharField(max_length=200)
    comment_image=models.ImageField(upload_to='comment_img',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment 

