from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Post, LikedPost, FollowersCount
from itertools import chain
# Create your views here.
@login_required(login_url='signin')
def index(res):
    user_object = User.objects.get(username=res.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=res.user.username)
    for users in user_following:
        user_following_list.append(users.user)
        
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))
    
    posts = Post.objects.all()
    return render(res, 'index.html',{'user_profile':user_profile,'posts':feed_list})

@login_required(login_url='signin')
def search(res):
    return render(res,  'search.html')

@login_required(login_url='signin')
def settings(res):
    user_profile = Profile.objects.get(user=res.user)
    
    if res.method == 'POST':
        if res.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = res.POST['bio']
            location = res.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if res.FILES.get('image') != None:
            image = res.FILES.get('image')
            bio = res.POST['bio']
            location = res.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('settings')
            
             
            
    
    return render(res, 'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(res):
    if res.method == 'POST':
        user = res.user.username
        image = res.FILES.get('image_upload')
        caption = res.POST['caption']
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()  
        
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(res):
    username = res.user.username
    post_id = res.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    
    like_filter = LikedPost.objects.filter(post_id=post_id,username=username).first()
    if like_filter == None:
        new_like= LikedPost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/') 
    
def profile(res, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    follower = res.user.username
    user = pk
    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
        
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    
        
    
    context = {
        'user_object' :user_object,
        'user_profile' : user_profile,
        'user_post_length' : user_posts,
        'user_posts' : user_posts,
        'button_text' : button_text,
        'user_post_length' : user_post_length,
        'user_followers' : user_followers,
        'user_following' : user_following,
    }
    return render(res, 'profile.html', context)    

def signup(res):

    if res.method =='POST':
        username = res.POST['username']
        email = res.POST['email']
        password = res.POST['password']
        password2 = res.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(res,'email taken')
                return  redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(res, 'Username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(res, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')



        else:
            messages.info(res,'Inconsistent password')
            return redirect('signup')
    else:
        return render(res, 'signup.html')


@login_required(login_url='signin')
def follow(res):
    if res.method == 'POST':
        follower = res.POST['follower']
        user = res.POST['user']
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower= FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

def signin(res):

    if res.method == 'POST':
        username = res.POST['username']
        password = res.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(res,user)
            return redirect('/')
        else:
            messages.info(res, 'Invalid credentials')

            return redirect('signin')

    else:
        return render(res,'signin.html')


@login_required(login_url='signin')
def logout(res):
    auth.logout(res)
    return redirect('signin')