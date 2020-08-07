from django import forms
from django.forms import ModelForm 
from .models import Listing, Bid

class Listing(ModelForm): 
    # specify the name of model to use 
    class Meta: 
        model = Listing 
        fields = 'title' , 'photo' ,'description', 'date', 'category', 'price', 'user_id'
       