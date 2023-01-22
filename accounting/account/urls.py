from django.urls import path
from account import views

urlpatterns = [
    # path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('passchange/', views.passchange, name='passchange'),
    path('dhulehome/', views.dhule_home, name="dhulehome"),
    path('solapurhome/', views.solapur_home, name="solapurhome"),
    path('adminhome/', views.admin_home, name="adminhome"),
    path('userdetail/<int:id>', views.user_detail, name='userdetail')
]