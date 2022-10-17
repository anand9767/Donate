from email.policy import default
from statistics import mode
from django.db import models

# Create your models here.

class MenuItem(models.Model):
    name = models.TextField()
    image = models.TextField(blank = True,default = '')
    type = models.TextField(blank = True)
    quantity = models.TextField(blank = True)


class Item(models.Model):
    name = models.TextField(blank = True)
    image = models.TextField(blank = True)
    price = models.CharField(max_length = 10,default = '')
    menuItem = models.ForeignKey(MenuItem,related_name='itemname',on_delete = models.DO_NOTHING)
    description = models.TextField(blank = True)
    ingredients = models.TextField(blank = True)
    nutritionalValue = models.TextField(blank = True)
