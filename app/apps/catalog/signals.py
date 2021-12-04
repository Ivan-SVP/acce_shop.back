from django.db.models.signals import pre_save
from django.dispatch import receiver
from uuslug import uuslug

from apps.catalog.models import Supplier, Category, Product


@receiver(pre_save, sender=Supplier)
@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Product)
def generate_slug(sender, instance=None, **kwargs):
    if not instance.slug:
        instance.slug = uuslug(instance.title, instance=instance)
