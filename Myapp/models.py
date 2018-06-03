from django.db import models

# Create your models here.
class User(models.Model):
    uname=models.CharField(max_length=20,unique=True)
    upwd=models.CharField(max_length=20)

    #用于关联用户上传的头像图片
    uicon=models.ImageField(null=True,blank=True,default=None)