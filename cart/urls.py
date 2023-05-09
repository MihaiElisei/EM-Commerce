from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add_to_cart/<product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<product_id>/<int:cart_item_id>',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove_cart_item/<product_id>/<int:cart_item_id>',
         views.remove_cart_item, name='remove_cart_item'),
]