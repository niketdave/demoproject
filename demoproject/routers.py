from rest_framework import routers

from account.views import UserViewSet, FaqViewSets
# from account.account_views.subadmin_views import SubAdminViewSet
# from account.account_views.carrier_views import CarrierViewSet
# from account.account_views.shipper_views import ShipperViewSet
# from account.account_views.driver_views import DriverViewSet
# from account.account_views.fleet_views import FleetViewSet

# from profilerole.views import (
#     RoleModuleViewSet,
#     RolePermissionViewSet,
#     RoleViewSet,
# #    UserRoleViewSet
# )

router = routers.DefaultRouter()
# -------------------- Account Routers ------------------------#

router.register(r'users', UserViewSet)
router.register(r'faq', FaqViewSets)
# router.register(r'subadmin', SubAdminViewSet)
# router.register(r'carrier', CarrierViewSet)
# router.register(r'shipper', ShipperViewSet)
# router.register(r'driver', DriverViewSet)
# router.register(r'fleet', FleetViewSet)
# -------------------- Profile Role Routers ------------------------#
# router.register(r'role_module', RoleModuleViewSet)
# # router.register(r'role_permissions', RolePermissionViewSet)
# router.register(r'role', RoleViewSet)


