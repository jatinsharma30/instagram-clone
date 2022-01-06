from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from datetime import datetime
from django.utils.timezone import utc

# Create your models here.
def profile_upload_location(instance,filename):
    return "%s/%s/%s" %(instance.id,'profile',filename)

class User(AbstractUser):
    profileImage=models.ImageField(upload_to=profile_upload_location,default='Default-Profile-Picture-Download-PNG-Image.png')
    discription=models.TextField(blank=True,null=True,max_length=100)

def post_upload_location(instance,filename):
    return "%s/%s/%s" %(instance.user.id,'post',filename)

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    post=models.ImageField(null=False,blank=False,upload_to=post_upload_location)
    description=models.TextField(blank=True,null=True,max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name='like',blank=True)
    def __str__(self):
        return self.user.username + ' ' + str(self.upload_date)
    def postUploadTime(self):
        days=int((datetime.utcnow().replace(tzinfo=utc)-self.upload_date).days)
        hours=int((datetime.utcnow().replace(tzinfo=utc)-self.upload_date).total_seconds()//3600)
        minutes=int((datetime.utcnow().replace(tzinfo=utc)-self.upload_date).total_seconds()//60)
        seconds=int((datetime.utcnow().replace(tzinfo=utc)-self.upload_date).total_seconds())
        if days>0:
            return f"{days} day ago"
        elif hours>0:
            return f"{hours} hours ago"
        elif minutes>0:
            return f"{minutes} minutes ago"
        else:
            return f"{seconds} seconds ago"
      

class Follow(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='Follow')
    follow=models.ManyToManyField(User)
    def __str__(self):
        return self.user.username


class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    reply=models.ForeignKey('self',null=True,related_name='replies',on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s -%s'%(self.post.id,self.user.username,self.id)
    def commentPostTime(self):
        days=int((datetime.utcnow().replace(tzinfo=utc)-self.date_added).days)
        hours=int((datetime.utcnow().replace(tzinfo=utc)-self.date_added).total_seconds()//3600)
        minutes=int((datetime.utcnow().replace(tzinfo=utc)-self.date_added).total_seconds()//60)
        seconds=int((datetime.utcnow().replace(tzinfo=utc)-self.date_added).total_seconds())
        if days>0:
            return f"{days} day ago"
        elif hours>0:
            return f"{hours} hours ago"
        elif minutes>0:
            return f"{minutes} minutes ago"
        else:
            return f"{seconds} seconds ago"
        
