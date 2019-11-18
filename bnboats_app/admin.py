from django.contrib import admin
from .models import Booking, BoatType, City, State, Invoice, Message, BoatAmenities, UserProfile, Boat, \
    BoatFavorite, CaptainProfile, CaptainLanguages, CaptainExtraActivities, BoatImages, BoatPriceIncludes, \
    BoatFishingSpecies, Review, IBGECityCodes, BoatBlockedDates


# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    search_fields = ['boat__user__username', 'boat__user__first_name', 'boat__city__city', 'boat__title',
                     'customer__username', 'customer__first_name', 'status']
    list_display = ['boat', 'boat_city', 'customer_name', 'status', 'created_on']
    def customer_name(self, obj):
        return obj.customer.first_name + " - " + obj.customer.username
    customer_name.admin_order_field = 'customer__first_name'
    def boat_city(self, obj):
        return obj.boat.city
    boat_city.admin_order_field = 'boat__city'
    pass
admin.site.register(Booking, BookingAdmin)

class BoatAdmin(admin.ModelAdmin):
    search_fields = ['pk', 'user__username', 'user__first_name', 'city__city', 'title']
    list_display = ['pk', 'title', 'city', 'user', 'user_name', 'status', 'created_on', 'last_modified']
    def user_name(self, obj):
        return obj.user.first_name
    user_name.admin_order_field = 'user__first_name'
    pass
admin.site.register(Boat, BoatAdmin)

admin.site.register(BoatType)

admin.site.register(City)

admin.site.register(State)

admin.site.register(Invoice)

admin.site.register(Review)

admin.site.register(Message)

admin.site.register(BoatAmenities)

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__first_name']
    list_display = ['user_name', 'user_email', 'fishing_client', 'fishing_discount', 'mobile_confirmed', 'email_confirmed', 'user_created_on', 'user_last_login']
    def user_name(self, obj):
        return obj.user.first_name
    user_name.admin_order_field = 'user__first_name'
    def user_email(self, obj):
        return obj.user.username
    user_email.admin_order_field = 'user__username'
    def user_created_on(self, obj):
        return obj.user.date_joined
    user_created_on.admin_order_field = 'user__date_joined'
    def user_last_login(self, obj):
        return obj.user.last_login
    user_last_login.admin_order_field = 'user__last_login'
    pass
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(BoatFavorite)

class CaptainAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__first_name']
    list_display = ['user_name', 'user_email', 'is_captaion']
    def user_name(self, obj):
        return obj.user.first_name
    user_name.admin_order_field = 'user__first_name'
    def user_email(self, obj):
        return obj.user.username
    user_email.admin_order_field = 'user__username'
admin.site.register(CaptainProfile, CaptainAdmin)

admin.site.register(CaptainLanguages)

admin.site.register(CaptainExtraActivities)

admin.site.register(BoatImages)

admin.site.register(BoatPriceIncludes)

admin.site.register(BoatFishingSpecies)

admin.site.register(IBGECityCodes)

admin.site.register(BoatBlockedDates)
