from django.contrib import admin

from .models import Commodity, Library, Cart, Review

admin.site.register(Commodity)
admin.site.register(Library)
admin.site.register(Cart)
admin.site.register(Review)


