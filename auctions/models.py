from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser, models.Model):
    
    def __str__(self):
        return f"{self.id} {self.username} {self.email} {self.last_login} {self.is_active}"
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenting_user")
    comment = models.CharField(max_length=512, blank=True)
    
    def __str__(self):
        return f"Comment by: {self.user.username} Comment: {self.comment}"
    

class Listings(models.Model):

    title = models.CharField(max_length=64)
    initialBid = models.IntegerField()
    image = models.CharField(max_length=512, blank=True)
    category = models.CharField(max_length=64, blank=True)
    condition = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=512, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    current_bid = models.IntegerField(blank=True)
    status =models.CharField(max_length=8)
    won_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="won_listings")
    comments = models.ManyToManyField(Comments, blank=True, related_name="commenting_listing")
    
    def __str__(self):
        return f"id: {self.id} title: {self.title} status:{self.status} comments: {self.comments}  WON_USER: {self.won_user}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    listings = models.ManyToManyField(Listings, related_name="watchlisted_by")
    
    def __str__(self):
        listings_str = ", ".join(str(listing) for listing in self.listings.all())
        return f"user: {self.user} listing: {listings_str}"
        # return f"user: {self.user} "

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_bids")
    new_bid = models.IntegerField()

    def __str__(self):
        return f"Bid by: {self.user}, listing: {self.listing.title} Amount: {self.new_bid}"

