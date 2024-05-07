from django.contrib import admin
from .models import Profile,Post_Upload,Post_Like,FollowersCount

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post_Upload)
admin.site.register(Post_Like)
admin.site.register(FollowersCount)


