from django.db import models
from django.db.models import OuterRef, ManyToManyField
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager, SQCount
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
                'product_images__isnull': False,
            }
        )

    def add_related_count(
        self,
        queryset,
        rel_model,
        rel_field,
        count_attr,
        cumulative=False,
        extra_filters=None,
    ):
        """Пришлось продублировать метод либы, чтобы добавить distinct для subquery, т.к. count считался неверно."""
        extra_filters = extra_filters if extra_filters is not None else {}

        if cumulative:
            subquery_filters = {
                rel_field + "__tree_id": OuterRef(self.tree_id_attr),
                rel_field + "__lft__gte": OuterRef(self.left_attr),
                rel_field + "__lft__lte": OuterRef(self.right_attr),
            }
        else:
            current_rel_model = rel_model
            for rel_field_part in rel_field.split('__'):
                current_mptt_field = current_rel_model._meta.get_field(rel_field_part)
                current_rel_model = current_mptt_field.related_model
            mptt_field = current_mptt_field

            if isinstance(mptt_field, ManyToManyField):
                field_name = "pk"
            else:
                field_name = mptt_field.remote_field.field_name

            subquery_filters = {
                rel_field: OuterRef(field_name),
            }
        subquery = rel_model.objects.filter(**subquery_filters, **extra_filters).values(
            "pk"
        ).distinct()
        return queryset.annotate(**{count_attr: SQCount(subquery)})


class Category(MPTTModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to=get_catalog_image_upload_path, blank=True, null=True)
    available = models.BooleanField('Доступность', default=False, help_text='Доступны покупателям')
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    objects = CategoryManager()

    def __str__(self):
        return self.title
