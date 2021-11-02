from django.db import models
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel


def get_catalog_image_upload_path(instance, filename):
    return f'catalog/categories/{instance.slug}_{filename}'


class CategoryManager(TreeManager):

    def get_with_products_count(self, qs, cumulative=True):
        from apps.catalog.models import Product

        return self.add_related_count(
            qs,
            Product,
            'category',
            'products__count',
            cumulative=cumulative,
            extra_filters={
                'available': True,
                'supplier_quantity__gt': 0,
            }
        )


class Category(MPTTModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to=get_catalog_image_upload_path, blank=True, null=True)
    available = models.BooleanField('Доступность', default=False, help_text='Доступны покупателям')
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    objects = CategoryManager()

    def __str__(self):
        return self.title
