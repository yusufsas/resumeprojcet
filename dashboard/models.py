from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)



class  Account(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", blank=True)
    cv = models.FileField(upload_to="pdf/", blank=True)
    number = models.CharField(max_length=15, blank=True, null=True, verbose_name='GSM Number')
    user_name = models.CharField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Her kayıt işlemi sırasında kullanıcı adını güncelleyin
        if self.user:
            self.user_name = self.user.first_name
        super().save(*args, **kwargs)

    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_EMPLOYEE = 'employee'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_EMPLOYEE, 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Job(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=300)

    def __str__(self):
        return self.name



# Create your models here.
