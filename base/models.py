from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField()
    bio = models.TextField(max_length=300, blank=True)
    password = models.CharField(max_length=100)
    profileImg = models.ImageField(upload_to='images/profile_images',default="images/blank-profile-piicture.png")
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


