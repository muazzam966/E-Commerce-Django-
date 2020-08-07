from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlist", views.add, name="addlist"),
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist/<int:listing_id>", views.removewatchlist, name="removewatchlist"),
    path("watchlistpage/<str:username>", views.watchlistpage, name="watchlistpage"),
    path("listingpage/<int:listing_id>", views.listingpage, name="listingpage"),
    path("bidsubmit/<int:listing_id>",views.bidsubmit,name="bidsubmit"),
    path("closebid/<int:listing_id>",views.closebid,name="closebid"),
    path("cmntsubmit/<int:listing_id>",views.cmntsubmit,name="cmntsubmit"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category")   
]
