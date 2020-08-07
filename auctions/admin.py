from django.contrib import admin
from .models import User, Listing, Bid,Comment, Watch, Closedbid
# Register your models here.

class Listingadmin(admin.ModelAdmin):
    list_display = ("__str__", "title", "price")

class Watchadmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "listingid")

class Bidadmin(admin.ModelAdmin):
    list_display= ("__str__", "user", "title", "bid")   

class Commentadmin(admin.ModelAdmin):
    list_display= ("__str__", "user", "comment")  

class Closedbidadmin(admin.ModelAdmin):
    list_display= ("__str__", "owner", "winner", "winprice")             

    

admin.site.register(User)
admin.site.register(Listing, Listingadmin)
admin.site.register(Bid, Bidadmin)
admin.site.register(Comment, Commentadmin)
admin.site.register(Watch, Watchadmin)
admin.site.register(Closedbid, Closedbidadmin)