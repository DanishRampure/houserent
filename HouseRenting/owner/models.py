from django.db import models
from loginapp.models import user


class Property(models.Model):
    city = models.CharField(max_length=100)
    flat_name = models.CharField(max_length=100, blank=True)
    furnished = models.BooleanField(default=False)
    avg_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    address = models.CharField(max_length=500)
    ramount = models.IntegerField()
    area = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50)
    choices = models.CharField(max_length=50)
    myImage = models.ImageField(null=True, blank=True, upload_to='images/', default="")
    total_flats = models.IntegerField()
    totfloors = models.IntegerField(null=True, blank=True)
    flat_type = models.CharField(max_length=100, blank=True)
    parking = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Available")
    availability_date = models.CharField(max_length=100, default=None)
    owner_id = models.IntegerField(null=True, blank=True)
    bond = models.IntegerField(null=True, blank=True)
    is_wishlist = models.BooleanField(default=False)


    def __str__(self):
        return self.address


class Files(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    file = models.FileField(upload_to='images/')

    def __str__(self):
        return self.property.address
