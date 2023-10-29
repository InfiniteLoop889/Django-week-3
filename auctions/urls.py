from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.listing_list, name="listing_list"),
    path("listing/<int:pk>/", views.listing_detail, name="listing_detail"),
    # path("add-listing/", views.listing_create, name="listing_create"),
    path("add_listing/", views.listing_create, name="listing_create"),
    path("listing/<int:pk>/update/", views.listing_update, name="listing_update"),
    path("listing/<int:pk>/delete/", views.listing_delete, name="listing_delete"),
    path("category/<str:category>/", views.listing_category, name="listing_category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("add_to_wishlist/<int:item_id>/", views.add_to_wishlist, name="add_to_wishlist"),
]
