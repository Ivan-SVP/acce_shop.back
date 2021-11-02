from django.db import models

from apps.catalog.models import Product


def get_product_image_image_upload_path(instance, filename):
    return f'catalog/products/{instance.product.category.slug}/{instance.product.slug}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_product_image_image_upload_path)
