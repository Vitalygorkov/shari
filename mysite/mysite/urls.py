"""mysite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from shop.models import Balloon, Category, Color, Photo_product

class BalloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balloon
        fields = "__all__"
        #fields = ['name', 'image', 'short_description', 'description', 'price', 'color','category', 'slug', 'availability']
class BalloonViewSet(viewsets.ModelViewSet):
    queryset = Balloon.objects.all()
    serializer_class = BalloonSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

router = routers.DefaultRouter()
router.register(r'balloons', BalloonViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    # path('shop/', include('shop.urls')),
    path('api/', include(router.urls)),
    #path('v1', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", include("shop.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)