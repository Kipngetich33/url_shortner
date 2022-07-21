from django.urls import path
# from django.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('details/<slug:shortcode>/',views.url_detail_view),
    path('details/',views.error_page),
    path('error/',views.error_page),
    path('<slug:shortcode>/',views.redirect_short_to_long_url)
]