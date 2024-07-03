#Nikola Kovacevic 2021/0113
from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    """
       Admin view for User model.

       Attributes:
           list_display (tuple): Fields to display in the list view.
           list_filter (tuple): Fields to filter in the list view.
           search_fields (list): Fields to search in the list view.
           ordering (tuple): Default ordering of the fields.
    """
    list_display = (
        'userid', 'username', 'first_name', 'last_name', 'phone', 'city', 'country', 'email', 'membershipstartdate',
        'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')

    list_filter = (
        'first_name', 'last_name', 'city', 'country', 'membershipstartdate', 'last_login', 'is_superuser', 'is_staff',
        'is_active', 'date_joined')

    search_fields = ['userid', 'username', 'first_name', 'last_name', 'phone', 'city', 'country', 'email',
                     'membershipstartdate', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']

    ordering = (
        'userid', 'username', 'first_name', 'last_name', 'phone', 'city', 'country', 'email', 'membershipstartdate',
        'last_login', 'date_joined')


admin.site.register(User, UserAdmin)


class SellerAdmin(admin.ModelAdmin):
    """
        Admin view for Seller model.

        Attributes:
            list_display (tuple): Fields to display in the list view.
            list_filter (tuple): Fields to filter in the list view.
            search_fields (list): Fields to search in the list view.
            ordering (tuple): Default ordering of the fields.
    """
    list_display = ('userid', 'numberOfListings', 'rating')

    list_filter = ('numberOfListings', 'rating')

    search_fields = ['userid', 'numberOfListings', 'rating']

    ordering = ('userid', 'numberOfListings', 'rating')


admin.site.register(Seller, SellerAdmin)


class AdminuserAdmin(admin.ModelAdmin):
    """
        Admin view for Adminuser model.

        Attributes:
            list_display (tuple): Fields to display in the list view.
            list_filter (tuple): Fields to filter in the list view.
            search_fields (list): Fields to search in the list view.
            ordering (tuple): Default ordering of the fields.
    """
    list_display = ('userid',)

    list_filter = ('userid',)

    search_fields = ['userid']

    ordering = ('userid',)


admin.site.register(Adminuser, AdminuserAdmin)


class CustomerAdmin(admin.ModelAdmin):
    """
        Admin view for Customer model.

        Attributes:
            list_display (tuple): Fields to display in the list view.
            list_filter (tuple): Fields to filter in the list view.
            search_fields (list): Fields to search in the list view.
            ordering (tuple): Default ordering of the fields.
    """
    list_display = ('userid', 'rating')

    list_filter = ('rating',)

    search_fields = ['userid', 'rating']

    ordering = ('userid', 'rating')


admin.site.register(Customer, CustomerAdmin)


class ChatAdmin(admin.ModelAdmin):
    """
        Admin view for Chat model.

        Attributes:
            list_display (tuple): Fields to display in the list view.
            list_filter (tuple): Fields to filter in the list view.
            search_fields (list): Fields to search in the list view.
            ordering (tuple): Default ordering of the fields.
    """
    list_display = ('chatid', 'user1', 'user2')

    list_filter = ('user1', 'user2')

    search_fields = ['chatid', 'user1', 'user2']

    ordering = ('chatid', 'user1', 'user2')


admin.site.register(Chat, ChatAdmin)


class ListingAdmin(admin.ModelAdmin):
    """
        Admin view for Listing model.

        Attributes:
            list_display (tuple): Fields to display in the list view.
            list_filter (tuple): Fields to filter in the list view.
            search_fields (list): Fields to search in the list view.
            ordering (tuple): Default ordering of the fields.
    """
    list_display = (
    'listingid', 'price', 'listingname', 'unit', 'quantity', 'description', 'type', 'date_added', 'userid')

    list_filter = ('price', 'listingname', 'unit', 'quantity', 'description', 'type', 'date_added', 'userid')

    search_fields = ['listingid', 'price', 'listingname', 'unit', 'quantity', 'description', 'type', 'date_added',
                     'userid']

    ordering = ('listingid', 'price', 'listingname', 'unit', 'quantity', 'description', 'type', 'date_added', 'userid')


admin.site.register(Listing, ListingAdmin)


class MessageAdmin(admin.ModelAdmin):
    """
        Admin view for Message model.

        Attributes:
            list_display (tuple): Fields to display in the list view.
            list_filter (tuple): Fields to filter in the list view.
            search_fields (list): Fields to search in the list view.
            ordering (tuple): Default ordering of the fields.
    """
    list_display = ('messageid', 'text', 'dateandtime', 'chatid', 'sender')

    list_filter = ('text', 'dateandtime', 'chatid', 'sender')

    search_fields = ['messageid', 'text', 'dateandtime', 'chatid', 'sender']

    ordering = ('messageid', 'text', 'dateandtime', 'chatid', 'sender')


admin.site.register(Message, MessageAdmin)

class ReservationAdmin(admin.ModelAdmin):
    """
        Admin view for Reservation model.

        Attributes:
            list_display (tuple): Fields to display in the list view.
            list_filter (tuple): Fields to filter in the list view.
            search_fields (list): Fields to search in the list view.
            ordering (tuple): Default ordering of the fields.
    """
    list_display = ('listingid', 'userid')

    list_filter = ('listingid', 'userid')

    search_fields = ['listingid', 'userid']

    ordering = ('listingid', 'userid')


admin.site.register(Reservation, ReservationAdmin)
