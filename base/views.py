from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib import messages,auth
from django.contrib.auth.models import User
from .models import Profile,Post_Upload,Post_Like,FollowersCount,Comment
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import Q
import random
from django.core.exceptions import MultipleObjectsReturned

# Create your views here.

@login_required(login_url='signin')
def Home(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post_Upload.objects.all()
    #show only the user posts you following 
    user_following_list = FollowersCount.objects.filter(user=request.user).values_list('follower', flat=True)
    print(user_following_list)

    feed_lists = Post_Upload.objects.filter(user__in=user_following_list)

    #user suggestion
    all_users = User.objects.exclude(username=request.user.username)

    # Filter out users the current user is already following
    new_suggestion = [user for user in all_users if user.id not in user_following_list]

    # Shuffle the list of suggestions
    random.shuffle(new_suggestion)

    # Limit the number of suggestions to 4
    suggestion_user_profile_list = Profile.objects.filter(user__in=new_suggestion)[:4]

    context = {
        "posts": feed_lists,
        "profile": profile,
        "suggestion_user_profile_list": suggestion_user_profile_list
    }
    return render(request, 'index.html', context)
    return render(request,'index.html',context)


def SignUp(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        Password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if Password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email is already taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.warning(request , "Username is already taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=Password)
                user.save()
                #log user 
                user_log = auth.authenticate(username=username,password=Password)
                auth.login(request, user_log)

                #add to profile db
                user_model = Profile.objects.create(
                    user=request.user,
                    username=username,
                    name=name,
                    email=email,
                    password=Password
                )

                return redirect('setting')
        else:
            messages.warning(request , "Password doesn't match")
            return redirect('signup')


        


    context = {}
    return render(request, 'signup.html',context)

def SignIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.warning(request, "Invalid")
    context = {}
    return render(request, 'signin.html',context)


@login_required(login_url='signin')
def Logout(request):
    
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def Profile_view(request,pk):
    user_object = User.objects.get(username=pk)
    if request.method == "POST":
        follower_username = request.POST['follower']
        user_username = request.POST['user']
        
        # Get User model instances based on usernames
        follower_user = User.objects.get(username=follower_username)
        user_user = User.objects.get(username=user_username)

        followercheck = FollowersCount.objects.filter(follower=follower_user,user=user_user).first()

        if followercheck == None:
             add_follower = FollowersCount.objects.create(follower=follower_user,user=user_user)
             add_follower.save()
             return redirect('profile',pk=pk)
        else:
            delete_follower = FollowersCount.objects.get(follower=follower_user,user=user_user)
            delete_follower.delete()
            return redirect('profile',pk=pk)
    user = request.user
    if FollowersCount.objects.filter(follower=user_object,user=user).exists():
        button_text = "Unfollow"
    else:
        button_text = "Follow"
    
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post_Upload.objects.filter(user=user_object)
    following_count = FollowersCount.objects.filter(follower=user_object).count()
    followers_count = FollowersCount.objects.filter(user=user_object).count()
    post_count = user_post.count()
    context = {
        "user_profile":user_profile,
        "user_post":user_post,
        "post_count":post_count,
        "following_count":following_count,
        "followers_count":followers_count,
        "button_text" : button_text,
        }
    return render(request, 'profile.html',context)

@login_required(login_url='signin')
def Setting(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get('image') == None:
            image = profile.profileImg
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            bio = request.POST['bio']

            profile.name = name
            profile.username = username
            profile.email = email
            profile.profileImg = image
            profile.bio = bio
            profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']
            bio = request.POST['bio']

            profile.name = name
            profile.username = username
            profile.email = email
            profile.profileImg = image
            profile.bio = bio
            profile.save()

        return redirect('home')



    context = {"profile":profile}
    return render(request, 'setting.html',context)



def Upload(request):
    
    if request.method == "POST":
        user = request.user
        profile_pic = Profile.objects.get(user=user)
        image = request.FILES.get('image')
        caption = request.POST['caption']

        new_Post = Post_Upload.objects.create(user=user, image=image , caption=caption,profile_pic=profile_pic)
        new_Post.save()
        return redirect("home")
    else:
        return redirect('home')


def Post_like(request):
    user = request.user
    post_id = request.GET.get('post_id')
    
    post = Post_Upload.objects.get(id=post_id)

    like_filter = Post_Like.objects.filter(user=user , post_id=post_id).first()

    if like_filter == None:
        new_like = Post_Like.objects.create(user=user , post_id=post_id)
        new_like.save()
        post.no_of_like = post.no_of_like+1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.no_of_like = post.no_of_like-1
        post.save()
        return redirect('home') 


def Search(request):
    profile = Profile.objects.get(user=request.user)
    value = request.GET.get('q')
    
    username_profile_list = User.objects.filter(
        Q(username__icontains=value) |
        Q(profile__name__icontains=value) |
        Q(profile__bio__icontains=value)
    )
    # Fetch profiles corresponding to the usernames in username_profile_list
    profile_objects = Profile.objects.filter(user__in=username_profile_list)

    context = {
        "profile": profile,
        "username_profile_list": username_profile_list,
        "profile_objects": profile_objects  # Renamed to plural for clarity
    }
    return render(request, "search.html", context)

def comment(request, username):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')

        try:
            # Attempt to fetch the post
            post = Post_Upload.objects.get(user__username=username)
        except MultipleObjectsReturned:
            # Handle the case where multiple posts are returned
            # You can choose to handle this situation in various ways,
            # such as displaying an error message or redirecting the user.
            # For now, let's redirect the user back to the home page.
            return redirect('home')
        except Post_Upload.DoesNotExist:
            # Handle the case where no post is found
            # You might want to display an error message or handle
            # this situation differently based on your application's requirements.
            return redirect('home')  # Redirecting to home page for now

        # Create a new comment object
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            comment_text=comment_text
        )

        # Redirect back to the home page
        return redirect('home')