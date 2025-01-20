
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True,null=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, unique=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)

  #  objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password','phone_number']



    def __str__(self):
        return self.email

class Contact(models.Model):
    related_to =models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, unique=True)
    
    def __str__(self):
        return f"{self.phone_number} is contact related to {self.related}" 
    



class SpamReport(models.Model):
   created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='reports')
   phone_number = models.CharField(max_length=13)
   

   def __str__(self):
       return f"Spam Report for {self.phone_number} created by {self.created_by}"
   
  
