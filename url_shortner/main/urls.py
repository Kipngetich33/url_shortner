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
    path('<slug:shortcode>',views.error_page),


    # path(r'^s/(?P<shortcode>[-_\w.]+)',views.s, name = 'statistics'),
    # path(r'^l/',views.l, name = 'last'),
    path(r'^a',views.a, name = 'all'), 
    # path(r'^w',views.w, name = 'wrong'), 
    # path(r'^t',views.t, name = 'test'),
    # path(r'^p',views.p, name = 'test2'), 
    # path(r'^i',views.i, name = 'single'), 
]