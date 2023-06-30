from django.urls import path
from django.views.generic.base import RedirectView
from . import views

# favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)



urlpatterns = [
    # path('baloon/', views.baloon, name='baloon'),
    path('', views.index, name='index'),
    # path('/favicon.ico/', favicon_view),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search, name='search'),
    path('favorites/', views.favorites, name='favorites'),
    path('blog/', views.blog, name='blog'),
    path('post/<slug:post_slug>/', views.post, name="post"),
    path('<category_slug>/', views.category, name='category'),
    path('<category_slug>/<product_slug>/', views.show_product, name='product'),

]