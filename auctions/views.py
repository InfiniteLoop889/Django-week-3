from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User
from .models import Category, Listing, WishlistItem, Bid
from .forms import ListingModelForm


'''CRUD+L - Create, Read, Update, Delete + List'''


def listing_list(request):
    listings = Listing.objects.all()

    # print(Listing.objects.first())
    # print(listings[0].bids_count())
    # print(listings[0].highest_bid())
    # print(request.user)
    # print(listings[0].pk)
    # print(listings[0].id)

    context = {"listings": listings}
    return render(request, "auctions/listing_list.html", context)


def listing_detail(request, pk):
    listing = Listing.objects.get(pk=pk)
    max_bid = listing.highest_bid().get("max")
    context = {
        "listing": listing,
        "max_bid": max_bid
    }
    return render(request, "auctions/listing_detail.html", context)


@login_required
def add_to_wishlist(request, item_id):
    item = Listing.objects.get(pk=item_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, listing=item)
    
    if created:
        messages.success(request, "Artikel zur Wunschliste hinzugefügt!")
    else:
        messages.warning(request, "Dieser Artikel befindet sich bereits in Ihrer Wunschliste.")

    print(wishlist_item.objects.first())
    # Redirect zurück zur 'listing_detail' Seite des betreffenden Artikels.
    return redirect('auctions:listing_detail', item_id) 


def place_bid(request, pk):
    listing = Listing.objects.all
    print
    return


@login_required
def listing_create(request):
    if request.method == "POST":
        form = ListingModelForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False) # Fill out form but don't write it to database yet
            listing.created_by = request.user  # Set current user as creator
            listing.save()  # Write all data to database
            return redirect("/")
    else:
        form = ListingModelForm()

    context = {"form": form}
    return render(request, "auctions/listing_create.html", context)


def listing_update(request, pk):
    listing = Listing.objects.get(pk=pk)
    form = ListingModelForm(instance=listing)
    if request.method == "POST":
        form = ListingModelForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        "listing": listing,
        "form": form
    }
    return render(request, "auctions/listing_update.html", context)


def listing_delete(request, pk):
    listing = Listing.objects.get(pk=pk)
    listing.delete()
    return redirect("/")


# Make the categories availablbe on every page
def categories(request):
    return {'categories': Category.objects.all()}


def listing_category(request, category):
    category = Category.objects.get(name=category)
    listings = Listing.objects.all().filter(category=category)
    if listings:
        context = {"category": category, "listings": listings}
        return render(request, "auctions/listing_category.html", context)
    else:
        error = "There are no articles in this category."
        context = {"category": category, "error": error}
        return render(request, "auctions/listing_category.html", context)


@login_required()
def watchlist(request):
    return render(request, "auctions/listing_watchlist.html")


# ------------------------------- Login / User section -------------------------------


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:listing_list"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:listing_list"))


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
        return HttpResponseRedirect(reverse("auctions:listing_list"))
    else:
        return render(request, "auctions/register.html")


# ##################### Error handling #####################
# def listing_category(request, category):
#     category = Category.objects.get(name=category)
#     try:
#         listings = Listing.objects.all().filter(category=category)
#         print(bool(listings))
#         context = {"listings": listings}
#         return render(request, "auctions/listing_category.html", context)
#     except ObjectDoesNotExist:
#         error = "There are no articles in this category."
#         context = {"listing": error}
#         return render(request, "auctions/listing_category.html", context)
