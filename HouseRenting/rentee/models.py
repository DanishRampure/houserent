from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
from owner.models import Property,Files
from loginapp.models import user
class Reviews(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, related_name='reviews',)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(max_length=500, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id.first_name

    class Meta:
        # it  a unique constraint on (user_id, property_id) to ensure a user can only give one review per property
        unique_together = ('user_id', 'property_id')

class About(models.Model):
    misson = models.TextField()
    vision = models.TextField()
    image = models.ImageField(upload_to='about/')

    def __str__(self):
        return str(self.id)
    
class WishList(models.Model):
    user_id = models.ForeignKey(user,on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property,on_delete = models.CASCADE)
