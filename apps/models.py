from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import datetime
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.

class Blog(models.Model):
    image = models.ImageField(upload_to='blog/image/')
    name = models.CharField(max_length=100)
    text = models.TextField()
    shortname =  models.CharField(max_length=20)
    template = models.FileField(upload_to='blog/template/')

class ProfilePicture(models.Model):
    img = models.ImageField(upload_to='profilepic/',default='profilepic/default.jpg',)#ProcessedImageField(upload_to='profilepic/',processors=[ResizeToFill(100,100)] , default='profilepic/default.jpg', format='JPEG' , options ={'quality': 60})

    def __str__(self):
        return (Account.objects.get(id=self.id).email)

class FeedbackClass(models.Model):
    email = models.CharField(max_length=100)
    feedback = models.TextField()

    def __str__(self):
        return (self.email)


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, first_name , last_name , password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
		    email = self.normalize_email(email),
		    username = username,
            first_name = first_name,
            last_name = last_name
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, first_name , last_name , password):
		user = self.create_user(
		    email = self.normalize_email(email),
		    password = password,
		    username = username,
            first_name = first_name,
            last_name = last_name,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class user(models.Model):

    dob=models.DateField(default=datetime(1990,1,1))
    sex = models.CharField(max_length=10)
    bio = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    pincode = models.IntegerField(default=0)

    def __str__(self):
        return (Account.objects.get(id=self.id).email)



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email' , max_length=60 , unique=True)
    username = models.CharField(max_length=60 , unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50 , default='')
    country = models.CharField(max_length=50 , default='')
    phone_number = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return (self.first_name+' '+self.last_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

