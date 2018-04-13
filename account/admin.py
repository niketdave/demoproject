from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission, ContentType
# from ten65.utils import export_as_csv_action



class UserAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return User.objects.filter(user_type='admin')

    def picture_img(self, obj):  # receives the instance as an argument
        try:
            return '<img src="{thumb}" width="50"/>'.format(
                thumb=obj.picture.url,
            )
        except:
            return "No Image"

    picture_img.width = 20
    picture_img.allow_tags = True
    picture_img.short_description = 'Picture'

    list_display = ('id', 'username', 'email',
                    'phone_number', 'user_type', 'last_login', 'is_active', 'is_deleted')
    list_display_link = ('username',)
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_per_page = 10

    # actions = [export_as_csv_action("CSV Export", fields=['email','user_type'])]

class SubAdminAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return SubAdmin.objects.filter(user_type='subadmin')

    list_display = ('id', 'username', 'email',
                    'phone_number', 'user_type', 'last_login', 'is_active', 'is_deleted')
    list_display_link = ('username',)
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_per_page = 10

class ShipperAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Shipper.objects.filter(user_type='shipper')

    list_display = ('id', 'username', 'email',
                    'phone_number', 'user_type', 'last_login', 'is_active', 'is_deleted')
    list_display_link = ('username',)
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_per_page = 10


class CarrierAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Carrier.objects.filter(user_type='carrier')

    list_display = ('id', 'username', 'email',
                    'phone_number', 'user_type', 'last_login', 'is_active', 'is_deleted')
    list_display_link = ('username',)
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_per_page = 10


class PermissionAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,{'fields': ['name','codename']}),

    ]
    list_display = ('name', 'codename')


class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'faq', 'user_type', 'created_at')
    list_display_link = ( 'id', 'faq',)
    search_fields = ['faq']
    list_filter = ('user_type',)
    list_per_page = 10

class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver_name', 'driver_email','driver_licence_number','driver_contact_number','driver_hash_id','created_at')
    list_display_link = ( 'id', 'driver_name',)
    search_fields = ['driver_email']
    list_filter = ('driver_name',)
    list_per_page = 10


class FleetAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrier', 'admin', 'truck', 'trailer', 'truck_hash_id')
    list_display_link = ( 'id', 'truck_hash_id',)
    search_fields = ['truck_hash_id']
    list_per_page = 10

admin.site.register(User, UserAdmin)
# admin.site.register(Shipper, ShipperAdmin)
# admin.site.register(Carrier, CarrierAdmin)
admin.site.register(Faq, FaqAdmin)
# admin.site.register(SubAdmin, SubAdminAdmin)
# admin.site.register(Driver ,DriverAdmin)
# admin.site.register(Fleet ,FleetAdmin)
# admin.site.register(ContentType)
