from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Listings, Watchlist, Bid, Comments

CATEGORY_CHOICES = [
    ("", "Select a category"),
    ("fashion", "Fashion"),
    ("electronic", "Electronic"),
    ("home", "Home"),
    ("toys", "Toys"),
    ("music", "Music"),
    ("books", "Books"),
    ('games', "Games"),
    ("sports", "Sports"),
    ("other", "Other"),
]
CONDITION_CHOICES = [
    ("", "Select a category"),
    ("new", "New"),
    ("used", "Used"),
]

class NewListing(forms.Form):
  title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Title'}))
  initialBid = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Initial bid ($)'}))
  image = forms.CharField(max_length=512, required=False ,widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Image (url)'}))
  category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'custom-select mb-3'}))
  condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=False, widget=forms.Select(attrs={'class': 'custom-select mb-3'}))
  description = forms.CharField(max_length=512, required=False, widget=forms.Textarea(attrs={'class': 'form-control md-textarea mb-3', 'rows': 3, 'placeholder': 'Add a description'}))


def index(request):
    
    active_listings = Listings.objects.filter(status='active')
    listings = Listings.objects.all()
    paginator = Paginator(active_listings, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # won_users = User.objects.filter(won_listings__isnull=False)
    # print(won_users)
    if request.user.is_authenticated:
        active_watchlist = []
        watchlists = Watchlist.objects.filter(user=request.user)
        for watchlist in watchlists:    
            for filter_watchlists in watchlist.listings.filter(status='active'):
                active_watchlist.append(filter_watchlists)
        
        
        won_listings = request.user.won_listings.all() # Hacer esto en el template
        return render(request, "auctions/index.html", {
            "listings": page_obj,
            "watchlist_length": len(active_watchlist),
            "won_listings": won_listings
        })
    return render(request, "auctions/index.html", {
        "listings": page_obj
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
            # print(type(user))
        login(request, user)
        return redirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

   
def listing_view(request, id):
    user=request.user
    listing = Listings.objects.get(pk=id)
    comments_list = []
    comments = listing.comments.all()
    for comment in comments:
        comments_list.append({
            'user': comment.user.username, 
            'comment': comment.comment
        })
    
    # print(listing.status)
    if listing.status != 'active': return redirect('auctions:index')
    if request.user.is_authenticated:
        won_listings = request.user.won_listings.all() 
        listing_user= listing.user
        # print(listing_user)
        watchlists = Watchlist.objects.filter(user=request.user)
        active_watchlists_id = []
        
        active_watchlists = []
        for watchlist in watchlists:
            for filter_watchlists in watchlist.listings.filter(status='active'):
                active_watchlists.append(filter_watchlists)
                active_watchlists_id.append(filter_watchlists.id)
        
            
        return render(request, 'auctions/listing.html', {
        "title": listing.title,
        "user_listing": listing.user.username,
        "initialBid": listing.initialBid,
        "image": listing.image,
        "condition": listing.condition,
        "category": listing.category,
        "description": listing.description,
        "listing_id": listing.id,
        "user": user,
        "watchlist_length": len(active_watchlists),
        "user_watchlist_id": active_watchlists_id,
        "current_bid": listing.current_bid,
        "listing_user": listing_user,
        "comments": comments_list,
        "won_listings": won_listings
    })
    return render(request, 'auctions/listing.html', {
        "title": listing.title,
        "user_listing": listing.user.username,
        "initialBid": listing.initialBid,
        "image": listing.image,
        "condition": listing.condition,
        "category": listing.category,
        "description": listing.description,
        "listing_id": listing.id,
        "user": user,
        "current_bid": listing.current_bid,
        "comments": comments_list
    })

def place_a_bid(request, listing_id):
    user= request.user
    
    if request.method == "POST":
        
        user_bid = int(request.POST['new_bid'])
        listing = Listings.objects.get(pk=listing_id)
        if not user_bid:return redirect("auctions:listing", listing_id)
        listing = Listings.objects.get(pk=listing_id)
        watchlists = Watchlist.objects.filter(user=request.user)
        active_watchlists_id = []
        active_watchlists = []
        won_listings = request.user.won_listings.all() # Hacer esto en el template
        for watchlist in watchlists:
            for filter_watchlists in watchlist.listings.filter(status='active'):
                active_watchlists.append(filter_watchlists)
                active_watchlists_id.append(filter_watchlists.id)
        
        # print(listing)
        if user_bid <= listing.initialBid and user_bid <= listing.current_bid: 
            return render(request, 'auctions/listing.html', {
            "title": listing.title,
            "user_listing": listing.user.username,
            "initialBid": listing.initialBid,
            "image": listing.image,
            "condition": listing.condition,
            "category": listing.category,
            "description": listing.description,
            "listing_id": listing.id,
            "user": user,
            "watchlist_length": len(active_watchlists),
            "user_watchlist_id": active_watchlists_id,
            "bid_error_msg": "Your bid must be higher than Current Bid",
            "current_bid": listing.current_bid,
            "won_listings": won_listings
            
        })
        else:
            # user_bider = Bid
            add_bid = Bid(user=user, listing=listing, new_bid=user_bid)
            add_bid.save()
            listing.current_bid = user_bid
            listing.save()
            return redirect("auctions:listing", listing_id)
        
            # print('weeee')
    
    return redirect("auctions:listing", listing_id)


def categories_view(request):
    active_listings = Listings.objects.filter(status='active')
    
    paginator = Paginator(active_listings, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    dict_categories = dict(CATEGORY_CHOICES)
    category_list = []
    
    if request.method == "POST":
        selected_category =  request.POST["category"]
        filtered_category = active_listings.filter(category=selected_category)
        
        for category in filtered_category:
            category_list.append(category)
        
        print(selected_category)
        if not category_list or not selected_category:
            # print(category_list)
            return render(request, 'auctions/categories.html', {
                "dict_categories": dict_categories,
                "listings": page_obj,
                "categories": 'All Categories',
            
            })
            
        if request.user.is_authenticated:
            won_listings = request.user.won_listings.all() # Hacer esto en el template
            watchlists = Watchlist.objects.filter(user=request.user)
            # print(watchlists)
            active_watchlists = []
            for watchlist in watchlists:
                for filter_watchlists in watchlist.listings.filter(status='active'):
                    active_watchlists.append(filter_watchlists)
            if not category_list:
                # print(category_list)
                return render(request, 'auctions/categories.html', {
                    "dict_categories": dict_categories,
                    "listings": page_obj,
                    "categories": 'All Categories',
                    "watchlist_length": len(active_watchlists),
                    "won_listings": won_listings
                })
        
        return render(request, 'auctions/categories.html', {
           "dict_categories": dict_categories,
           "listings": category_list,
           "categories": selected_category,
        })
    # for key, value in dict_categories.items():
    #     category_list.append(key)
        # print(key)
    
    return render(request, 'auctions/categories.html', {
        "dict_categories": dict_categories,
        "listings": page_obj,
        "categories": 'All Categories',
    })


@login_required
def newList(request):
    user = request.user
    watchlists = Watchlist.objects.filter(user=request.user)
    won_listings = request.user.won_listings.all() # Hacer esto en el template
    
    active_watchlists = []
    for watchlist in watchlists:
        for filter_watchlists in watchlist.listings.filter(status='active'):
            active_watchlists.append(filter_watchlists)
    
    
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            
            title = form.cleaned_data['title']
            initialBid = form.cleaned_data['initialBid']
            image = form.cleaned_data['image']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            condition = form.cleaned_data['condition']
            description = form.cleaned_data['description']
            listing = Listings(title=title, initialBid=initialBid, image=image, condition=condition, category=category, description=description, user=user, current_bid=0, status='active')
            listing.save()
            return redirect('auctions:index')
        else: 
            return redirect('auctions:index', {
                "form": form
            })
    return render(request, 'auctions/newList.html', {
        "form": NewListing(),
        "watchlist_length": len(active_watchlists),
        "won_listings": won_listings

    })
 
@login_required
def add_watchinglist(request, listing_id):
    user_request = request.user
    if user_request:
        listing = Listings.objects.get(pk=listing_id)
        watchlist = Watchlist.objects.filter(user=user_request, listings=listing).first() #give NONE if not exist
        
        if not watchlist:
            watchlist = Watchlist.objects.create(user=user_request)
            watchlist.listings.add(listing)
        
        return redirect("auctions:listing", listing_id)

@login_required
def remove_watchinglist(request, listing_id):
    user_request = request.user
    if user_request:
        listing = Listings.objects.get(pk=listing_id)
        watchlist = Watchlist.objects.filter(user=user_request, listings=listing).first() #give NONE if not exist
        print(watchlist)
        watchlist.delete()
        return redirect("auctions:listing", listing_id)


@login_required    
def watchinglists_view(request):
    won_listings = request.user.won_listings.all() # Hacer esto en el template
    watchlists = Watchlist.objects.filter(user=request.user)
    active_watchlist = []
    
    for watchlist in watchlists:
        for filter_watchlists in watchlist.listings.filter(status='active'):
            active_watchlist.append(filter_watchlists)
    return render(request, 'auctions/watchlists.html', {
        "watchlist_length": len(active_watchlist),
        "active_listings": active_watchlist,
        "won_listings": won_listings
    })
    
@login_required     
def close_bid(request, listing_id):
    
    listing = Listings.objects.get(pk=listing_id)
    bids = listing.listing_bids.all()
    max_new_bid = max(bid.new_bid for bid in bids)
        
    won_bider = bids.get(new_bid=max_new_bid)
    listing.won_user=won_bider.user
    listing.status = 'inactive'
    listing.save()
    
    # print(listing)
    return redirect("auctions:listing", listing_id)
    
@login_required
def won_listings(request):
    user = User.objects.get(username=request.user.username)
    won_listings = user.won_listings.all()
    watchlists = Watchlist.objects.filter(user=request.user)
    active_watchlists = []
    
    for watchlist in watchlists:
        for filter_watchlists in watchlist.listings.filter(status='active'):
            active_watchlists.append(filter_watchlists)
    # print(watchlists)
    
    
    return render(request, 'auctions/won_listings.html', {
        "won_listings": won_listings,
        "watchlist_length": len(active_watchlists) 
    })
    

@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != '':
            listing = Listings.objects.get(pk=listing_id)
            # print(listing)
            commenting = Comments.objects.create(user=request.user, comment=comment)
            listing.comments.add(commenting) 
            listing.save()
        return redirect("auctions:listing", listing_id)
    

def error_404_view(request, exception):
    return render(request, 'autcions/404.html', status=404)

