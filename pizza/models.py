from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Item(models.Model):
    item_type = models.CharField(max_length=64)
    item_name = models.CharField(max_length=64)
    item_size = models.CharField(max_length=10,choices=(("Small","S"),("Large","L"),("NA","N")),default=None,null=True)
    price = models.FloatField(default=1)

    def __str__(self):
        return f"{self.item_type} -- {self.item_name} -- {self.item_size}"

class User_order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time_ordered=models.CharField(max_length=64) 
    status=models.CharField(max_length=64,choices=(("Processing","Processing"),("Completed","Completed"),("Could not be Completed","Could not be Completed")),default="Processing",null=True)
    price=models.FloatField()

    def __str__(self):
        return f"#{self.id} -- {self.status}"

class Order(models.Model):
    order = models.ForeignKey(User_order,on_delete=models.CASCADE,related_name="order_info")
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_cost = models.FloatField()
    
    def __str__(self):
        return f"#{self.order.id} -- [{self.item}] -- {self.quantity} -- {self.order.status}"        






