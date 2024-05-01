from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib import messages,auth
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='signin')
def Home(request):
    context = {}
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

                return redirect('home')
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
def Profile_view(request):
    context = {}
    return render(request, 'profile.html',context)

@login_required(login_url='signin')
def Setting(request):
    print(request.user)
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

