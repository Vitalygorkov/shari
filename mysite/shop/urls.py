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
    path('promotions_page/', views.promotions_page, name='promotions_page'),
    path('post/<slug:post_slug>/', views.post, name="post"),
    path('promotions/<slug:promotions_slug>/', views.promotions, name="promotions"),
    path('footer_page/<slug:footer_page_slug>/', views.footer_pages, name="promotions"),
    path('tags/<slug:tag_slug>/', views.tags_view, name="tags_view"),
    path('<category_slug>/', views.category, name='category'),
    path('<category_slug>/<product_slug>/', views.show_product, name='product'),

]