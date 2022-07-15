from django.urls import path
# from django.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^$',views.h,name = 'home'),
    path('', views.h, name='home'),
]