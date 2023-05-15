
from django.db import models

# Create your models here.
class Category(models.Model):
    cat_name=models.CharField(max_length=30)

    def __str__(self):
        return self.cat_name

    class Meta:
        db_table='Category'

class Food(models.Model):
    item_name=models.CharField(max_length=100)
    price=models.FloatField(default=300)
    description=models.CharField(max_length=100)
    imageurl=models.ImageField(upload_to='images',default='abc.jpg')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)


    class Meta:
        db_table='Food'