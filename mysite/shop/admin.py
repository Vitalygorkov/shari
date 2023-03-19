from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Color, Product, Balloon, Photo_product, VideosProducts

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Color)
# admin.site.register(Product)
# admin.site.register(Balloon)
# admin.site.register(Photo_product)
# admin.site.register(VideosProducts)
# Register your models here.

class DescriptionAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Balloon
        fields = '__all__'

class VideosInline(admin.StackedInline):
    model = VideosProducts
    extra = 1

class Photo_productInline(admin.StackedInline):
    model = Photo_product
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="320" height="240"')

    get_image.short_description = "Изображение"

class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        fields = ("id", "name", "price", "sale",)
        skip_unchanged = True
        report_skipped = False

@admin.register(Photo_product)
class Photo_productAdmin(admin.ModelAdmin):
    list_display = ("get_image", "product",)
    list_display_links = ("product",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="320" height="240"')

    get_image.short_description = "Изображение"

@admin.register(Balloon)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    form = DescriptionAdminForm
    prepopulated_fields = {'slug': ('name',), }
    list_display = ("name", "price")
    # list_editable = ("price")
    list_display_links = ("name",)
    # list_filter = ("name")
    # search_fields = ("name")
    inlines = [VideosInline, Photo_productInline,]
    save_on_top = True
    save_as = True

@admin.register(VideosProducts)
class VideosAdmin(admin.ModelAdmin):
    list_display = ("video", "product")