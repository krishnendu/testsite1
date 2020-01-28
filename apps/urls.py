from django.urls import include,path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('<str:username>/feedback',views.feedback_view, name='feedback'),
    path('<str:username>/edit',views.editprofile, name='editprofile'),
    path('createblog/',views.createblog, name='createblog'),
    path('blog/<str:shortname>',views.blog_view, name='blog_view'),
    path('blog/<str:shortname>/edit',views.editblog, name='editblog'),
    
    path('<str:username>/changeprofilepic/',views.profilepic, name='profilepic'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_change_form.html'), name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),


    path('<str:username>/',views.profile, name='profile'),
]
