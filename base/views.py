from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def loginPage(req):
    page='login'
    if req.user.is_authenticated:
        return redirect('home')

    if req.method=='POST':
        email=req.POST.get('email')
        password=req.POST.get('password')
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(req,'User doesn\'t exist')
        user=authenticate(req,email=email,password=password)
        if user is not None:
            login(req,user)
            return redirect('home')
        else:
            messages.error(req,'invalid password')

    context={'page':page}
    return render(req,'login_register.html',context)

def logoutPage(req):
    logout(req)
    return redirect('home')

def registerPage(req):
    
    form=MyUserCreationForm()
    if req.method=='POST':
        form=MyUserCreationForm(req.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username
            user.save()
            login(req,user)
            return redirect('home')
        else:
            print('form',form.errors)
            messages.error(req,'An error occurred')

    return render(req,'login_register.html',{'form':form})

def home(req):
    q=req.GET.get('q') if req.GET.get('q')!=None else ''

    rooms=Room.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains=q))
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    context={'rooms':rooms,'topics':topics,"room_count":room_count,'room_messages':room_messages}
    return render(req,'home.html',context)


def userProfile(req,id):
    user=User.objects.get(id=id)
    rooms=user.room_set.all()
   
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(req,'profile.html',context)

def room(req,id):
    room=Room.objects.get(id=id)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    
    if req.method=='POST':
        message=Message.objects.create(user=req.user,room=room,
        body=req.POST.get('body'))
        room.participants.add(req.user)
        return redirect('room',id=room.id)

    context={'room':room,"room_messages":room_messages,
    'participants':participants}

    return render(req,'room.html',context)

@login_required(login_url='login')
def createRoom(req):
    form=RoomForm()
    topics=Topic.objects.all()
    if req.method=='POST':
        topic_name=req.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        #form=RoomForm(req.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=req.user
        #     room.save()
        Room.objects.create(
            host=req.user,
            topic=topic,
            name=req.POST.get('name'),
            description=req.POST.get('description')
        )
        return redirect('home')

    context={'form':form,'topics':topics}
    return render(req,'room_form.html',context)

@login_required(login_url='login')
def updateRoom(req,id):
    room=Room.objects.get(id=id)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if req.user!=room.host :
        return HttpResponse('<h1>you are not allowed</h1>')

    if req.method=='POST':
        topic_name=req.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=req.POST.get('name')
        room.topic=topic
        room.description=req.POST.get('description')
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(req,'room_form.html',context)

@login_required(login_url='login')
def deleteRoom(req,id):
    room=Room.objects.get(id=id)
    if req.user!=room.host :
        return HttpResponse('<h1>you are not allowed</h1>')
    if req.method=='POST':
        room.delete()
        return redirect('home')
    context={'obj':room}
    return render(req,'delete.html',context)

@login_required(login_url='login')
def deleteMessage(req,id):
    message=Message.objects.get(id=id)
    
    if req.method =='POST':
        message.delete()
        return redirect('home')
    context={'obj':message}
    return render(req,'delete.html',context)

@login_required(login_url='login')
def updateUser(req):
    user=req.user
    form=UserForm(instance=user)
    if req.method=='POST':
        form=UserForm(req.POST,req.FILES,instance=user)
        form.save()
        return redirect('profile',id=user.id)
    return render(req,'update-user.html',{'form':form})


def topicsPage(req):
    q=req.GET.get('q') if req.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(req,'topics_mobile.html',context)

def activitiesPage(req):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(req,'activity_mobile.html',context)

def notFound(req,exception):
    
    return render(req,'notfound.html')