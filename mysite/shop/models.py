from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import mptt
from PIL import Image as Img
from io import StringIO, BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Category(MPTTModel):
    name = models.CharField("Категория",max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, verbose_name='URL на английском, например "Category"', unique=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def get_absolute_url(self):
        return f'/{self.url}/'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['-tree_id']

    class Meta:
        db_table = "category"
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('tree_id', 'level')

mptt.register(Category, order_insertion_by=['name'])

class Color(models.Model):
    name = models.CharField("Цвет", max_length=50, unique= True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
class Product(models.Model):
    # обработка
    # гнелий( наполнение)
    # Гелий да нет
    # добавить размер в см
    # Ширина ?
    # Высота ?
    # Глубина ?
    # Вес ?
    # Срок гарантии

    name = models.CharField(max_length=150)
    image = models.ImageField('Основное фото', upload_to="photo/", null=True, blank=True)  # фото  https://qna.habr.com/q/218059
    short_description =  models.CharField(max_length=1000, blank=True)
    description = models.TextField('Описание', blank=True)
    price = models.IntegerField('Цена', blank=True, null=True)  # цена
    color = models.ForeignKey(Color, verbose_name="Цвет", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ManyToManyField('Category', blank=True, verbose_name="Категории")
    slug = models.SlugField(max_length=250,unique=True, db_index=True, verbose_name='URL')
    availability = models.BooleanField("Наличие", default=False, blank=True) # Наличие по дефолту нет.
    # whom = TreeForeignKey(Category, on_delete=models.DO_NOTHING, blank=True,null=True,related_name='cat_product')

    def save(self, *args, **kwargs):            #https://overcoder.net/q/136570/%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%80%D0%B0-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-django-%D0%B8-%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D0%B5%D1%80%D0%B5%D0%B4-%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%BE%D0%B9
        if self.image:
            photo = Img.open(BytesIO(self.image.read()))
            # photo = photo.convert('RGB')
            photo.thumbnail((450,450), Img.ANTIALIAS)
            output = BytesIO()
            if photo.mode == "JPEG":
                photo.save(output, format='JPEG', quality=99)
                output.seek(0)
                self.image= InMemoryUploadedFile(output,'ImageField', "%s" %self.image.name, 'image/jpeg', output, None)
            elif photo.mode == "PNG":
                photo.save(output, format='png', quality=99)
                output.seek(0)
                self.image= InMemoryUploadedFile(output,'ImageField', "%s" %self.image.name, 'png', output, None)
            else:
                photo.save(output, format='webp', quality=99)
                output.seek(0)
                self.image= InMemoryUploadedFile(output,'ImageField', "%s" %self.image.name, 'webp', output, None)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.category:
            return f'/{self.category.url}/{self.slug}'
        else:
            return f'/none-cateory/{self.slug}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Balloon(Product):
    size = models.IntegerField("размер см", blank=True,
                                              null=True)  # размер см
    helium = models.BooleanField("Гелий да/нет", default=False, blank=True)  # "Гелий да/нет" по дефолту нет.
    processing = models.BooleanField("Обработка да/нет", default=False, blank=True)  # "Обработка да/нет" по дефолту нет.
    air = models.BooleanField("Воздух да/нет", default=False, blank=True)  # "Воздух да/нет" по дефолту нет.

    class Meta:
        verbose_name = 'Шар'
        verbose_name_plural = 'Шары'

class Photo_product(models.Model):
    image = models.ImageField("Изображение", upload_to="photo/")
    product = models.ForeignKey(Product, verbose_name="", related_name='prodimg', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):            #https://overcoder.net/q/136570/%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%80%D0%B0-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-django-%D0%B8-%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D0%B5%D1%80%D0%B5%D0%B4-%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%BE%D0%B9
        if self.image:
            photo = Img.open(BytesIO(self.image.read()))
            # photo = photo.convert('RGB')
            photo.thumbnail((1280,1280), Img.ANTIALIAS)
            output = BytesIO()
            if photo.mode == "JPEG":
                photo.save(output, format='JPEG', quality=99)
                output.seek(0)
                self.image= InMemoryUploadedFile(output,'ImageField', "%s" %self.image.name, 'image/jpeg', output, None)
            elif photo.mode == "PNG":
                photo.save(output, format='png', quality=99)
                output.seek(0)
                self.image= InMemoryUploadedFile(output,'ImageField', "%s" %self.image.name, 'png', output, None)
            else:
                photo.save(output, format='webp', quality=99)
                output.seek(0)
                self.image= InMemoryUploadedFile(output,'ImageField', "%s" %self.image.name, 'webp', output, None)
        super(Photo_product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

class VideosProducts(models.Model):
    video = models.CharField("Ссылка на видеоролик, например https://www.youtube.com/watch?v=QBkUCVVpyGE убрать всё до знака = и оставить QBkUCVVpyGE ", max_length=100)
    product = models.ForeignKey(Product, verbose_name="Товар", related_name='prodvideos',on_delete= models.CASCADE, null=True)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"