from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group, Permission
from .constants import APP_USER_TYPE


class Office(models.Model):
    """
        To store the shipper office addresses
    """
    address = models.TextField()
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=40, null=True, blank=True)
    zip_code = models.CharField(max_length=40, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    contact_person_email = models.EmailField(max_length=255, null=True, blank=True)
    contact_person_phone = models.CharField(max_length=30, null=True, blank=True)
    contact_person_phone_ext = models.CharField(max_length=10, null=True, blank=True)
    contact_fax = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.address



class User(AbstractUser):
    """
        To store the basic details of all user types
    """
    password_reset_token = models.CharField(
        max_length=255, null=True, blank=True)
    password_reset_request = models.BooleanField(default=False)
    user_type = models.CharField(
        choices=APP_USER_TYPE, max_length=20,
        null=True, blank=True, db_index=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    is_one_time_password = models.BooleanField(default=True)
    one_time_password = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    # # carrier
    # full_name = models.CharField(max_length=255, null=True, blank=True)
    # carrier_mode = models.CharField(max_length=255, null=True, blank=True)
    # carrier_scat_num = models.CharField(max_length=255, null=True, blank=True)
    # # Shipper
    # user_offices = models.ManyToManyField(
    #     Office, blank=True)
    # profile_assigned_roles = models.ManyToManyField(
    #     'profilerole.Role', related_name="profile_assigned_roles", blank=True)
    # profile_assigned_permissions = models.ManyToManyField(
    #     'profilerole.RolePermission', related_name="profile_assigned_permissions", blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ['-id']

    # to verify user_type of request.user
    @property
    def is_employee(self):
        return self.user_type == 'employee'

    @property
    def is_shipper(self):
        return self.user_type == 'shipper'

    @property
    def is_carrier(self):
        return self.user_type == 'carrier'

    @property
    def is_driver(self):
        return self.user_type == 'driver'

    @property
    def is_subadmin(self):
        return self.user_type == 'subadmin'

    @property
    def is_admin(self):
        return self.user_type == 'admin'


class Shipper(User):
    class Meta:
        proxy = True

class Carrier(User):
    class Meta:
        proxy = True

class SubAdmin(User):
    class Meta:
        proxy = True


# class Driver(models.Model):
#     """
#         To store the driver data
#     """
#     carrier = models.ForeignKey(
#         User, related_name="carrier_drivers",
#         on_delete=models.CASCADE,
#         limit_choices_to=Q(Q(user_type__in=['carrier']) & Q(is_active=True) & Q(is_deleted=False)))
#     admin = models.ForeignKey(
#         User, related_name="admin_drivers",
#         on_delete=models.CASCADE,
#         limit_choices_to=Q(Q(user_type__in=['admin', 'subadmin']) & Q(is_active=True) & Q(is_deleted=False)), null=True)
#     driver_name = models.CharField(max_length=255)
#     driver_email = models.EmailField(max_length=255, null=True , blank=True)
#     driver_hash_id = models.CharField(max_length=255, null=True, blank=True)
#     driver_licence_number = models.CharField(max_length=255)
#     driver_contact_number = models.CharField(max_length=20, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     active_reason = models.TextField(null=True, blank=True)
#     inactive_reason = models.TextField(null=True, blank=True)
#     # timestamp
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)



# class Fleet(models.Model):
#     """
#         To store the driver data
#     """
#     carrier = models.ForeignKey(
#         User, related_name="carrier_fleets",
#         on_delete=models.CASCADE,
#         limit_choices_to=Q(Q(user_type__in=['carrier']) & Q(is_active=True) & Q(is_deleted=False)))
#     admin = models.ForeignKey(
#         User, related_name="admin_fleets",
#         on_delete=models.CASCADE,
#         limit_choices_to=Q(Q(user_type__in=['admin', 'subadmin']) & Q(is_active=True) & Q(is_deleted=False)), null=True)
#     truck = models.CharField(max_length=255)
#     trailer = models.CharField(max_length=255)
#     truck_hash_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
#     is_active = models.BooleanField(default=True)
#     active_reason = models.TextField(null=True, blank=True)
#     inactive_reason = models.TextField(null=True, blank=True)
#     # timestamp
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)


class Faq(models.Model):
    """
        To store FAQ for the shipper and carrier
    """
    user_type = models.CharField(
        choices=APP_USER_TYPE, max_length=20)
    faq = models.CharField(max_length=255)
    faq_answer = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.faq



