from django.db import models
# Create your models here.

class user(models.Model):
    user_id=models.AutoField(primary_key=True, default=None)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50, default=None)
    email=models.CharField(max_length=200, unique=True)
    phonenumber=models.CharField(max_length=10, default=None)
    password=models.CharField(max_length=100)
    role=models.CharField(max_length=10)
    
    def __str__(self):
         return str(self.user_id)
