from django.db import models
from account.models import CustomUser
# Create your models here.
class Post(models.Model):
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="post")
    caption=models.CharField(max_length=200,null=True,blank=True)
    post_image=models.ImageField(upload_to='posts',blank=True)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self) :
        return f'post by {self.owner.username}'
