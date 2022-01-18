from django.urls import path
from chat import views

urlpatterns = [
    path('',views.inbox,name='inbox'),
    path('chatBox/<str:user>/',views.chatBox,name='chatBox'),
    path('postMessage',views.postMessage,name='postMessage')
]