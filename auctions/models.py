from unicodedata import name
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    # slug = models.SlugField(max_length=30, unique=True)

    # Change the displayed name in the admin area (default would be "Categories")
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2)
    image_URL = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # bids refers to the related_name="bids" in the Bid model
    def bids_count(self):
        bids = self.bids.all().count()
        return bids

    # return the highest bid from the Bid model
    def highest_bid(self):
        return self.bids.aggregate(max=Max('bid'))


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'listing')


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.user} bid {self.bid} for {self.listing}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=255, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order comments by time (newest first)
        ordering = ["-time"]

    def __str__(self):
        return f"{self.user}: {self.comment}"
