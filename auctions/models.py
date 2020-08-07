from django.contrib.auth.models import AbstractUser
from django.db import models

# import form class from django 
from django import forms
from django.forms import ModelForm 


class User(AbstractUser):
    pass

class Watch(models.Model):
    listingid = models.IntegerField(null=True)
    user = models.CharField(blank=True, max_length=64)

    def __str__(self):
        return f"{self.user}"
        

class Listing(models.Model):
    CATEGORIES = (
        ("Electronics", 'Electronics'),
        ("Cloth", 'Cloth'),
        ("Shoes", 'Shoes'),
    )
    title = models.CharField(max_length=64)
    photo=models.ImageField(upload_to="gallery")
    description = models.CharField(max_length=255, default="")
    date=models.DateTimeField(default="")
    category = models.CharField(max_length=64, default="", choices=CATEGORIES)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, default="", related_name="Listings")
    price=models.IntegerField(default=0)
    wlist = models.ManyToManyField(Watch, blank=True, null=True, related_name="list")

    def __str__(self):
        return f"{self.title}: {self.photo} to {self.date}"

class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64, default="")
    listing_id = models.IntegerField(default=0)
    bid = models.IntegerField(default=0)

class Closedbid(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listing_id = models.IntegerField(default=0)
    winprice = models.IntegerField(default=0)    

class Comment(models.Model):
    user = models.CharField(max_length=64, default="")
    time = models.CharField(max_length=64, default="")
    comment = models.CharField(max_length=250, default="")
    listing_id = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.comment}"    


