"""pratilipi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from tastypie.api import Api

from user.api import UserResource
from daily_pass.api import DailyPassResource

v1_api = Api(api_name="v1")
v1_api.register(UserResource())
v1_api.register(DailyPassResource())

urlpatterns = {
    path('admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls))
}
