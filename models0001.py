from django.db import models
from django.db.models.fields import CharField
from AdminApp.models import Food

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "UserInfo"

class Cart(models.Model):
    user = models.ForeignKey(UserInfo,on_delete = models.CASCADE)
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    qty = models.IntegerField()

    class Meta:
        db_table = "Cart"

class Payment(models.Model):
    card_no = models.CharField(max_length = 4)
    expiry = models.CharField(max_length = 10)
    cvv = models.CharField(max_length = 4)
    balance = models.FloatField(default=10000)

    class Meta:
        db_table = "Payment"

class Order_Master(models.Model):
    username = models.CharField(max_length=20)
    date_of_order = models.DateField()
    amount = models.FloatField(default=100)
    item_details = CharField(max_length=100)

    class Meta:
        db_table = "Order_Master"