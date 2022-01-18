from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.handleLogin,name='handleLogin'),
    path('signup',views.handleSignup,name='handleSignup'),
    path('logout',views.handleLogout,name='handleLogout'),
    path('home',views.home,name='home'),
    path('profile/<str:user>/',views.profile,name='profile'),
    path('editProfile',views.editProfile,name='editProfile'),
    path('addPost',views.addPost,name='addPost'),
    path('follow',views.follow,name='follow'),
    path('test',views.test,name='test'),
    path('like',views.like,name='like'),
    path('addComment',views.addComment,name='addComment'),
    path('suggested',views.suggested,name='suggested'),
    path('changeProfile',views.changeProfile,name='changeProfile'),#profilePicture
    path('updateProfileInfo',views.updateProfileInfo,name='updateProfileInfo'),
    path('isUsernameValid',views.isUsernameValid,name='isUsernameValid'),
    path('changePassword',views.changePassword,name='changePassword'),
]