from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.homepage, name='main'),
    path('b', views.index, name='test'),
    #path('<int>/', views.user, name='userpage'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="logout"),
    path('luthers', views.list_classes, name='list'),
    path('luthers/', views.list_classes, name='list'),
    path('luthers/<str:whichDept>', views.call_api, name="luthers"),
    path('luthers/user/', views.user_page_base, name="user_page_base"),
    path('luthers/friends/', views.Friends, name="friendspage"),
    path('luthers/user/<str:username>', views.user_page, name="user_page"),
    path('users', views.list_users, name='user'),
    path('luthers/shoppingcart/', views.shoppingcart, name='shoppingcart'),
    path('luthers/Calender/', views.Calender, name='calender'),
    path('luthers/class/<int:pk>', views.specificClass, name='specificClass'),
    path('luthers/class/<int:pk>/rate', views.rateSpecificClass, name='rateSpecificClass')
]
