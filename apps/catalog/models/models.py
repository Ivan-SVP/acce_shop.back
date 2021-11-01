from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Supplier(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    markup = models.IntegerField('Наценка %', help_text='Наценка для розницы')
    has_rrp = models.BooleanField('Есть РРЦ', default=False, help_text='Флаг наличия рекомендуемой розничной цены')
    url = models.URLField('Сайт', blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


def get_catalog_image_upload_path(instance, filename):
    return f'catalog/categories/{instance.slug}_{filename}'


class Category(MPTTModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to=get_catalog_image_upload_path, blank=True, null=True)
    available = models.BooleanField('Доступность', default=False, help_text='Доступны покупателям')
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


def get_product_image_image_upload_path(instance, filename):
    return f'catalog/products/{instance.product.category.slug}/{instance.product.slug}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_product_image_image_upload_path)
