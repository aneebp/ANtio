from django.db import models
from django.contrib.auth.models import User
import uuid



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField()
    bio = models.TextField(max_length=300, blank=True)
    password = models.CharField(max_length=100)
    profileImg = models.ImageField(upload_to='profile_images',default="images/blank-profile-picture.png")
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name



class Post_Upload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_pic = models.ForeignKey(Profile,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    no_of_like = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-created']
    

class Post_Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username
    

    
class FollowersCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')


    def __str__(self):
        return self.user.username
    