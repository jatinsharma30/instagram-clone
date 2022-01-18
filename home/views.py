#for search
from django.http.response import JsonResponse
import json

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Comment, User,Post,Follow

from django.db.models import Q

# Create your views here.
@login_required
def home(request):
    user=request.user
    posts=None
    #home page posts
    try:
        followings=Follow.objects.get(user=request.user)
        posts=Post.objects.filter(user__in=followings.follow.all()).order_by('upload_date')
    except Follow.DoesNotExist:
        followings=None
    if followings==None:
        suggestion=User.objects.all().exclude(id=request.user.id)[:5]
    else:
        print(followings.follow.all())
        suggestion=User.objects.all().exclude(id__in=followings.follow.all()).exclude(id=request.user.id)[:5]
    print(suggestion)
    params={'user':user,'posts':posts,'suggestions':suggestion}
    return render(request,'home.html',params)

@login_required
def suggested(request):
    try:
        followings=Follow.objects.get(user=request.user)
        posts=Post.objects.filter(user__in=followings.follow.all()).order_by('upload_date')
    except Follow.DoesNotExist:
        followings=None
    if followings==None:
        suggestion=User.objects.all().exclude(id=request.user.id)
    else:
        print(followings.follow.all())
        suggestion=User.objects.all().exclude(id__in=followings.follow.all()).exclude(id=request.user.id)
    param={'suggestions':suggestion}
    return render(request,'suggested.html',param)

def handleLogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        user1 = authenticate(email=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        elif user1 is not None:
            login(request,user1)
            return redirect('home')
        # A backend authenticated the credentials
        else:
            messages.error(request,'Wrong username/email or password')
        # No backend authenticated the credentials
    return render(request,'login.html')

def handleSignup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        name=request.POST['name']
        password=request.POST['password']
        print(username,name,email,password)
        if User.objects.filter(email=email).exists():
            messages.error(request,'email id already taken')
        elif User.objects.filter(username=username).exists():
            messages.error(request,'username taken kindly login or enter another username')
        else:
            user = User.objects.create_user(username=username,email=email,password=password,first_name=name)
            user.save()
            login(request,user)
            return redirect('home')
    return render(request,'signup.html')

def handleLogout(request):
    logout(request)
    return redirect('handleLogin')
    

@login_required
def profile(request,user):
    kuser=User.objects.get(username=user)
    post=Post.objects.filter(user=kuser)
    try:
        following=Follow.objects.get(user=kuser)
    except Follow.DoesNotExist:
        following=None
    followers=Follow.objects.filter(follow=kuser)
    #to check logged in user follow the profile user
    try:
        following_=Follow.objects.get(user=request.user)
        if kuser in following_.follow.all():
            status='following'
        else:
            status='notFollowing'

    except Follow.DoesNotExist:
        status='notFollowing'
    print(status)
    param={'user':kuser,'posts':post,'following':following,'followers':followers,'status':status}
    return render(request,'profile.html',param)
    

@login_required
def editProfile(request):
    return render(request,'editProfile.html')

@login_required
def addPost(request):
    if request.method=='POST':
        post=request.FILES['post']
        print(post)
        addPost=Post.objects.create(user=request.user,post=post)
        addPost.save()
    return redirect(request.META['HTTP_REFERER']) 

def test(request):
    if request.method=='POST':
        data = json.loads(request.body)
        username=data['username']
        # print(username)
        users=User.objects.filter(username__contains=username).values('username','profileImage')
        # print(users)
        users_list=list(users)
        return JsonResponse(users_list,safe=False)

#to handle follow and unfollow
@login_required
def follow(request):
    if request.method=='POST':
        status=request.POST['followStatus']
        user=request.POST['user']
        try:
            follow_=Follow.objects.get(user=request.user)
            
        except Follow.DoesNotExist:
            follow_=Follow.objects.create(user=request.user)
                
        if status=='follow':
            follow_.follow.add(user)
            follow_.save()
            
        else:
            follow_.follow.remove(user)
        user=User.objects.get(id=user)
    # return redirect(f'profile/{user.username}')
    return redirect(request.META['HTTP_REFERER']) 

@login_required
def like(request):
    if request.method =="POST":
        data = json.loads(request.body)
        postId=data['postId']
        post=Post.objects.filter(id=postId).first()
        if request.user in post.like.all():
            post.like.remove(request.user)
            likeStatus='unlike'
            post.save()
        else:
            post.like.add(request.user)
            likeStatus='liked'
            post.save()
        if post.like.all().count()==0:
            print('no likes')
            data={
                'likeStatus':'no like'
            }
        else:
            print(post.like.first().profileImage.url)
            data={
                'count':post.like.all().count(),
                'likeStatus':likeStatus,
                'firstUserUsername': post.like.first().username,
                'firstUserProfile':post.like.first().profileImage.url
            } 
    return JsonResponse(data)

@login_required
def addComment(request):
    if request.method=='POST':
        comment=request.POST['comment']
        post_=request.POST['postId']
        post=Post.objects.get(id=post_)
        commentId=request.POST['commentId']
        if commentId!="":
            reply=Comment.objects.get(id=commentId)
            comment_=Comment.objects.create(user=request.user,post=post,body=comment,reply=reply)
            print('reply')
        else:
            comment_=Comment.objects.create(user=request.user,post=post,body=comment)
            print('n')
        print(post_,comment)
        comment_.save()
    return redirect(request.META['HTTP_REFERER']) 

def changeProfile(request):
    if request.method=='POST':
        img=request.FILES['profile']
        user=User.objects.get(id=request.user.id)
        user.profileImage=img
        user.save()
    return redirect(request.META['HTTP_REFERER'])  

@login_required
def updateProfileInfo(request):
    if request.method=='POST':
        username=request.POST['username']   
        name=request.POST['name']   
        bio=request.POST['bio']   
        email=request.POST['email']
        user=User.objects.get(id=request.user.id)
        if username!="":
            user.username=username
        if name!="":
            user.first_name=name
        if bio!="":
            user.discription=bio
        if email!="":
            user.email=email
        user.save()
    return redirect(request.META['HTTP_REFERER'])  

def isUsernameValid(request):
    if request.method=='POST':
        data = json.loads(request.body)
        username=data['username']
        print(User.objects.filter(username=username).exists())
        if username == request.user.username:
            return JsonResponse('available',safe=False)
        elif username.isalnum()==False:
            return JsonResponse('not available',safe=False)           
        elif User.objects.filter(username=username).exists():
            return JsonResponse('not available',safe=False)           
        else:
            return JsonResponse('available',safe=False)

@login_required
def changePassword(request):
    if request.method=='POST':
        password=request.POST['password']
        password1=request.POST['password1']
        oldPassword=request.POST['oldPassword']
        if password==password1 and request.user.check_password(oldPassword):

            try:
                user=User.objects.get(id=request.user.id)
                newPassword=user.set_password(password)
                user.save()
                messages.success(request,'password changed!!')
                return redirect('editProfile')    
            except Exception as e:
                messages.error(request,'wrong password!! issue')
        else:
            messages.error(request,'wrong password!!')
    return redirect(request.META['HTTP_REFERER'])    

