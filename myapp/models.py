from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import AbstractUser,BaseUserManager
import datetime

# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    Type=(('mbbs','Mbbs'),('md','Md'),('ms','Ms'),('bhms','Bhms'),('bams','Bams'),('bpt','Bpt'))
    gender= (('male','Male'), ('female','Female'))
    Role=(('doctor','Doctor'),('patient','Patient'))
    email=models.EmailField(unique=True)
    addres=models.TextField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=10,choices=gender,null=True,blank=True)
    mobile=models.CharField(max_length=20,null=True,blank=True)
    clinicname=models.CharField(max_length=50,null=True,blank=True)
    role=models.CharField(max_length=10,choices=Role,null=True,blank=True)
    types=models.CharField(max_length=10,choices=Type,null=True,blank=True)
    pic=models.FileField(upload_to='profile',default='1.png')
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    
class Slot(models.Model):
    TIMESLOT = (
        ('09:00 am To 10:00 am', '09:00 am To 10:00 am'),
        ('10:00 am To 11:00 am', '10:00 am TO 11:00 am'),
        ('11:00 am To 12:00 pm', '11:00 am To 12:00 pm'),
        ('12:00 pm To 01:00 pm', '12:00 pm To 01:00 pm'),
        ('02:00 pm To 03:00 pm', '02:00 pm To 03:00 pm'),
        ('03:00 pm To 04:00 pm', '03:00 pm To 04:00 pm'),
        ('04:00 pm To 05:00 pm', '04:00 pm To 05:00 pm'),
    )
    WEEKS = (
        ('monday','Monday'),
        ('tuesday','Tuesday'),
        ('wednesday','Wednesday'),
        ('thursday','Thursday'),
        ('friday','Friday'),
        ('saturday','Saturday'),
    )
    doctor=models.ForeignKey(User,on_delete=models.CASCADE)
    weeks=models.CharField(max_length=10,choices=WEEKS)
    timeslot=models.CharField(max_length=50,choices=TIMESLOT)
    avalible_slot=models.IntegerField(default=1)
    
    def __str__(self):
        return self.doctor.email
    
    
class Appointments(models.Model):
    STATUS = (
        ('pending','Pending'),
        ('completed','Completed'),
        ('absent','Absent'),
        ('canceled','Canceled'),
        
    ) 
    slot=models.ForeignKey(Slot,on_delete=models.CASCADE)
    patient=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS,default='pending')
    description= models.TextField(default=None)
    
    def __str__(self):
        return self.patient.email