from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout ,login as log_in
#from django.contrib.auth.models import User
from .models import Account,ProfilePicture,FeedbackClass,user,Blog
from django.core.exceptions import ValidationError
from django.conf import settings
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
#from .models import user,FeedbackClass
from .forms import ProfilePictureForm , UserForm ,BlogForm

def navbar(req):

    log='Log in'
    url='login'
    username='login'
    name='Krishnendu Chatterjee'
    phone_number='+917003033085'
    email='krishnenduchatterjee25@gmail.com'
    welcome=''
    admin=False
    if req.user.is_authenticated:
        log='Log out'
        url='logout'
        username=req.user.username
        admin=req.user.is_admin
        welcome='Welcome '+username
    nav={ 'profile' : { 'name' : 'Profile' , 'url' : username , 'welcome' : welcome , 'admin' : admin},
    'log' : { 'name' : log , 'url' : url},
    'register' : {'name' : 'Register' , 'url' : 'register'},
    'copyright' : { 'name' : name , 'phone_number' : phone_number , 'email' : email ,}
    }
    return nav


def home(req):
    blog=Blog.objects.all()
    ob1={ 'blogs' : blog }
    ob1.update(navbar(req))
    return render(req ,'home.html',ob1)

def blog_view(req,shortname):
    template = Blog.objects.get(shortname=shortname).template
    print(template.url)
    return render(req , template.url.split('/')[-1], navbar(req))
def register(req):
    if(req.method=='POST'):
        email=req.POST["email"]
        username=req.POST["username"]
        first_name=req.POST["first_name"]
        last_name=req.POST["last_name"]
        country=req.POST["country"]
        phone_number=req.POST["phone_number"]
        password=req.POST["password"]
        confirm_password=req.POST["confirm_password"]
        if(Account.objects.filter(email=email).exists()):
            messages.error(req,"Email Id already exists")
        if(Account.objects.filter(username=username).exists()):
            messages.error(req,"Username already exists")
        if(password!=confirm_password):
            messages.error(req,"Passwords doesn't match")
        else:
            user=Account.objects.create_user(email=email,username=username,first_name=first_name,last_name=last_name)
            user.country=country
            user.phone_number=phone_number
            user.set_password(password)
            user.save()
            return redirect('/login')
    else:
        return render(req,'register.html',navbar(req))
    return render(req,'register.html',navbar(req))


def login(req):
    if(req.method=='POST'):
        email = req.POST['email']
        password = req.POST['password']
        try:
            user = authenticate(req, email=Account.objects.get(username=email).email, password=password)
        except:
            user = authenticate(req, email=email , password=password)
        if user is not None:
            log_in(req, user)
            return redirect('/'+req.user.username)
        else:
            messages.error(req,"Username or Password does not match")
            return render(req,'login.html',navbar(req))

    else:
        return render(req,'login.html',navbar(req))



def logout_view(req):
    logout(req)
    return redirect('/')


def profile(req,username):
    if not req.user.is_authenticated or not req.user.username==username:
        print('NOT Authenticated')
        return redirect('%s?next=%s' % (settings.LOGIN_URL, req.path))
    print('Authenticated')
    try:
        ob1={'user' : Account.objects.get(username=req.user.username)}
        ob1.update(navbar(req))
        ob2={ 'feedback' : {'name' : 'Feedback Form', 'url' : '/'+username+'/feedback'} }
        ob3={ 'username' : req.user.username }
        ob4={ 'pp' : ProfilePicture.objects.get(id=Account.objects.get(username=username).id).img }
        ob5={ 'user1' : user.objects.get(id=Account.objects.get(username=username).id) }
        ob1.update(ob2)
        ob1.update(ob3)
        ob1.update(ob4)
        ob1.update(ob5)
        return render(req,'userinfo.html',ob1)
    except:
        pp=ProfilePicture(id=req.user.id)
        pp.save()
        user1=user(id=req.user.id)
        user1.save()
        return redirect('/'+username)

def profilepic(req,username):
    if not req.user.is_authenticated or not req.user.username==username:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, req.path))
    id=Account.objects.get(username=username).id
    instance =get_object_or_404(ProfilePicture, id=id)
    form=ProfilePictureForm(req.POST or None, req.FILES or None ,instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/'+username)
    ob1={'form' : form}
    ob1.update(navbar(req))
    return render(req,'changeprofilepic.html',ob1)


def editprofile(req,username):
    if( not req.user.is_authenticated or req.user.username != username ):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, req.path))
    id=user.objects.get(id=Account.objects.get(username=username).id).id
    instance =get_object_or_404(user, id=id)
    form=UserForm(req.POST or None,instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/'+username)
    ob1={'form' : form}
    ob1.update(navbar(req))
    return render(req,'edit.html',ob1)

def feedback_view(req,username):
    if( not req.user.is_authenticated or req.user.username != username ):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, req.path))
    email=Account.objects.get(username=username).email
    if(req.method=='POST'):
        feedback=req.POST['feedback']
        obj=FeedbackClass(email=email,feedback=feedback)
        obj.save()
        return redirect('/'+username)
    else:
        return render(req,'feedback.html',navbar(req))

def editblog(req,shortname):
    if( not req.user.is_authenticated or not req.user.is_admin ):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, req.path))
    id=Blog.objects.get(shortname=shortname).id
    instance =get_object_or_404(Blog, id=id)
    #if(req.method == 'POST'):
    form=BlogForm(req.POST or None, req.FILES or None ,instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/')
    ob1={'form' : form}
    ob1.update(navbar(req))
    return render(req,'editblog.html',ob1)

def createblog(req):
    if( not req.user.is_authenticated or not req.user.is_admin ):
        return redirect('%s?next=%s' % (settings.LOGIN_URL, req.path))
    if(req.method=='POST'):
        form=BlogForm(req.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    else:
        form=BlogForm()
        ob1={'form' : form}
        ob1.update(navbar(req))
        return render(req,'editblog.html',ob1)