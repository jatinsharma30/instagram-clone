from django.shortcuts import render,redirect
from .models import Thread,ThreadManager,ChatMessage
from django.http import Http404
from home.models import Follow

# Create your views here.
def inbox(request):
    qs=Thread.objects.by_user(request.user)
    try:
        follow_=Follow.objects.get(user=request.user)   
    except Follow.DoesNotExist:
        follow_=Follow.objects.create(user=request.user)
    param={'qs':qs,'following':follow_}
    return render(request,'chat/inbox.html',param)

def chatBox(request,user):
    #for message suggestion
    try:
        follow_=Follow.objects.get(user=request.user)   
    except Follow.DoesNotExist:
        follow_=Follow.objects.create(user=request.user)
    #for inbox
    qs=Thread.objects.by_user(request.user)
    #for chat
    obj, created    = Thread.objects.get_or_new(request.user, user)
    if obj == None:
        raise Http404
    # messages=ChatMessage
    param={'qs':qs,'messages':obj,'following':follow_}
    return render(request,'chat/chatbox.html',param)

def postMessage(request):
    if request.method=='POST':
        threadId=request.POST['threadId']
        message=request.POST['message']
        msg=ChatMessage.objects.create(thread_id=threadId,user=request.user,message=message)

        msg.save()
        return redirect(request.META['HTTP_REFERER']) 
