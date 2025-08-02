from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('add-to-cart/<int:event_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:event_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:event_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
]