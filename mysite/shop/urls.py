from django.urls import path

from . import views

urlpatterns = [
    path('baloon/', views.baloon, name='baloon'),
    path('cart/', views.cart, name='cart'),
    path('<category_slug>/', views.category, name='category'),
    path('<category_slug>/<product_slug>/', views.show_product, name='product'),
    path('', views.index, name='index'),
]