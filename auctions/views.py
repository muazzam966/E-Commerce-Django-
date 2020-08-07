from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest,Http404
from django.shortcuts import render ,get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User, Listing, Comment, Bid, Watch, Closedbid
from datetime import datetime
# import form class from django 
from django import forms 
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required




def index(request):
    item = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "item" : item
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def add(request):
    from .forms import Listing
    
    if request.method == 'POST':
        # create object of form
        form = Listing(request.POST or None, request.FILES or None)
        # check if form data is valid
        if form.is_valid():
            # save the form data to model
            form.save()
            # Do something with the author (model instance)
            return render(request, 'auctions/uploading.html', {'message': 'Successful Uploaded'})
        else:
            return render(request, 'auctions/addlist.html', {'form': form})

    else:
        form = Listing()
        return render(request, 'auctions/addlist.html', {'form': form})



@login_required
def addwatchlist (request, listing_id):
   if request.user.username:
        w = Watch()
        w.user = request.user.username
        w.listingid = listing_id
        w.save()
        return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))


def removewatchlist(request,listing_id):
    if request.user.username:
        try:
            w = Watch.objects.filter(user=request.user.username,listingid=listing_id)
            w.delete()
            return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))
        except:
             return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))


@login_required
def watchlistpage(request, username):
    if request.user.username:
        
        w = Watch.objects.filter(user=username)
        items = []
        for i in w:
            items.append(Listing.objects.filter(id=i.listingid))

        return render(request, "auctions/watchlist.html", {
                 "items": items
                  }) 
       


def listingpage(request, listing_id):

    item=Listing.objects.get(id=listing_id) 

    try:
        comments = Comment.objects.filter(listing_id=listing_id)
    except:
        comments = None 

    if request.user.username:
        try:
            if Watch.objects.filter(user=request.user.username,listingid=listing_id):
                condition = True
            else:
                condition = False
        except:
            condition = False
        try:
            a = Listing.objects.get(id=listing_id)
            if a.user_id == request.user:
                owner=True
            else:
                owner=False
        except:
            return redirect('index')   
    else:
        condition=False
        owner=False
    return render(request, "auctions/listingpage.html", {
        "item": item, "condition" : condition, "owner":owner, "comments" :comments
         })          

def bidsubmit(request, listing_id):
    current_bid = Listing.objects.get(id=listing_id)
    current_bid = current_bid.price
    if request.method == "POST":
        user_bid = int(request.POST["bid"])
        if user_bid > current_bid:
            listing_items = Listing.objects.get(id=listing_id)
            listing_items.price = user_bid
            listing_items.save()
            try:
                if Bid.objects.filter(id=listing_id):
                    bidrow = Bid.objects.filter(id=listing_id)
                    bidrow.delete()
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.title = listing_items.title
                bidtable.listing_id = listing_id
                bidtable.bid = user_bid
                bidtable.save()
                
            except:
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.title = listing_items.title
                bidtable.listing_id = listing_id
                bidtable.bid = user_bid
                bidtable.save()
            
            messages.success(request, 'Bid successful')
            return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))
        else :
            messages.success(request, 'Bid price should be greater than current price')
            return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))


def closebid(request,listing_id):
    if request.user.username:
        try:
            listingrow = Listing.objects.get(id=listing_id)
        except:
            return redirect('index')
        cb = Closedbid()
        title = listingrow.title
        cb.owner = listingrow.user_id
        cb.listing_id = listing_id
        try:
            bidrow = Bid.objects.get(listing_id=listing_id,bid=listingrow.price)
            cb.winner = bidrow.user
            cb.winprice = bidrow.bid
            cb.save()
            bidrow.delete()
        except:
            cb.winner = listingrow.user_id
            cb.winprice = listingrow.price
            cb.save()
        try:
            if Watchlist.objects.filter(listingid=listing_id):
                watchrow = Watchlist.objects.filter(listingid=listing_id)
                watchrow.delete()
            else:
                pass
        except:
            pass
        try:
            crow = Comment.objects.filter(listing_id=listing_id)
            crow.delete()
        except:
            pass
        try:
            brow = Bid.objects.filter(listing_id=listing_id)
            brow.delete()
        except:
            pass
        try:
            cblist=Closedbid.objects.get(listing_id=listing_id)
        except:
            cb.owner = listingrow.user_id
            cb.winner = listingrow.user_id
            cb.listing_id = listing_id
            cb.winprice = listingrow.price
            cb.save()
            cblist=Closedbid.objects.get(listing_id=listing_id)
        listingrow.delete()
        return render(request,"auctions/winningpage.html",{
            "cb":cblist,
            "title":title
        })   

    else:
        return redirect('index')


def cmntsubmit(request,listing_id):
    if request.method == "POST":
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = dt
        c.listing_id = listing_id
        c.save()
        return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))
    else :
        return redirect('index')


def categories(request):
    items=Listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")
   
    return render(request,"auctions/categpage.html",{
        "items": items
    })

def category(request,category):
    catitems = Listing.objects.filter(category=category)
    return render(request,"auctions/category.html",{
        "items":catitems,
        "cat":category,
    })