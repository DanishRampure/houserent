from django.db import models

# Create your models here.

class User(models.Model):
  user_id=models.IntegerField(primary_key=True)
  username=models.CharField(max_length=200)
  email=models.EmailField(max_length=254)
  password=models.CharField(max_length=20)
  phone_no=models.CharField(max_length=10)
  isRantee=models.BooleanField(default=False)
  isOwner=models.BooleanField(default=False)

  def __intt__(self):
    return self.user_id

class Property(models.Model): 
    property_id=models.IntegerField(primary_key=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    city=models.CharField(max_length=25)
    address=models.CharField(max_length=200)
    property_type=models.CharField(max_length=50)
    rent_amount=models.IntegerField()
    status=models.BooleanField(default=False)
    bond=models.CharField(max_length=50)
    img=models.CharField(max_length=200)
    area=models.CharField(max_length=200)
    about=models.CharField(max_length=100)
    parking=models.BooleanField(default=False)
    floor=models.CharField(max_length=20)
    # def __str__(self):
    #    return self.username
    
class Reviews(models.Model):
    rating_id=models.IntegerField(primary_key=True)
    property_id=models.ForeignKey(Property, on_delete=models.CASCADE)
    comments=models.CharField(max_length=300)
    rating=models.IntegerField()
    timeperiod=models.IntegerField()

class RentedTable(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    property_id=models.IntegerField()

