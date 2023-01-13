from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Post
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Home page
@login_required(login_url='login')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    return render(request, "index.html", {'user_profile': user_profile})

# Add posts
def adddiary(request):
    if request.method == 'POST':
        user = request.user.username
        title = request.POST['title']
        body = request.POST['body']

        x = datetime.today()

        dayW = x.strftime("%a")
        month = x.strftime("%B")
        dayA = x.strftime("%d")
        year = x.strftime("%Y")
        time = x.strftime("%H:%M")

        post_d = (dayW +" "+ month +" "+ dayA +"," +" "+ year )

        new_post = Post.objects.create(user=user, title=title, body=body, post_d=post_d, post_t=time)
        new_post.save()

        return redirect('/')
    else: 
        return render(request, 'adddiary.html')

# Get posts
def feed(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk).order_by("-created_at")
    user_post_length = len(user_posts)

    # >>>> pagination start
    
    page_num = request.GET.get('page', 1)
    paginator = Paginator(user_posts, 4) # one post per page

    try:
        page_obj = paginator.page(page_num) # to return the page as far as the page number is valid
    except PageNotAnInteger:
        page_obj = paginator.page(1) # to deliver the first page if page is not an integer 
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages) # to deliver the last page if page is out of range

    # >>>> pagination end

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'page_obj': page_obj
    }

    return render(request, 'feed.html', context)    

# Register
def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('register')
        else: 
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            #log user in
            auth.login(request, user)


            #create a profile
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('settings')

    else:
        return render(request, "register.html")

# User settings
@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        """ if request.FILES.get('image') == None:
            image = user_profile.profileimg

            user_profile.profileimg = image
            user_profile.save() """

        if request.FILES.get('image') != None:
            image = request.FILES.get('image') 
            user_profile.profileimg = image
            user_profile.save()

        return redirect('settings')       

    return render(request, 'settings.html', {'user_profile': user_profile})

# Login
def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')   

    else:    
        return render(request, "login.html")            

# Logout
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')  

# Delete Post
@login_required(login_url='login')
def delete(request):
        
        if request.method == "POST":
            post_id = request.POST["item"]
            
            delete_post = Post.objects.get(id=post_id)
            delete_post.delete()

        return redirect('/')

