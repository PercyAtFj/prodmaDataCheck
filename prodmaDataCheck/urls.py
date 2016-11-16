"""prodmaDataCheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from diffQuery import views as diffQuery_view

urlpatterns = [
    url(r'^$', diffQuery_view.home),
    url(r'^index/queryDiff', diffQuery_view.queryDiffRecords),
    url(r'^index/$', diffQuery_view.index),
    url(r'^admin/', admin.site.urls),
    url(r'^export/', diffQuery_view.export),
    url(r'^fund/(\w+)/$', diffQuery_view.queryFun),
    url(r'^fund/$', diffQuery_view.fund),
]
