"""ten65 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .routers import router
# from rest_framework_swagger.views import get_swagger_view
from demoproject.schemas import get_params_swagger_view
from django.contrib.auth import views
from account.views import index as reset_password_index, changePassword as reset_password_view
from account.serializers import UserSerializer as create_view
from demoproject import settings
from account.forms import LoginForm
# import table


admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = 'Dashboard'
admin.site.site_title = settings.ADMIN_SITE_HEADER

schema_view = get_params_swagger_view(title='Demo')
# schema_view = get_swagger_view()
swaggerpatterns = [
    url(r'demo/', schema_view),
]

urlpatterns = [
    # url(r'^table/', include('table.urls')),
    path('admin/', admin.site.urls),
    # url(r'', include('account.urls')),
    # url(r'', include('profilerole.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name="login"),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    path(r'api/', include(router.urls)),
    path(r'api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    path('swagger/', include(swaggerpatterns)),
    # For password change view using token
    url(r'resetpassword/(?P<reset_token>[\w]+)/$',
        reset_password_index, name='index'),
    url(r'resetpassword/(?P<reset_token>[\w]+)/changePassword',
        reset_password_view, name='changePassword'),

]
