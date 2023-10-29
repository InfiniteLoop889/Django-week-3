from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment, WishlistItem


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ["name", "slug"]
#     prepopulated_fields = {"slug": ("name",)}


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WishlistItem)