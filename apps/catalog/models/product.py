from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.catalog.models import Supplier
from apps.catalog.models.category import Category


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.filter(available=True, supplier_quantity__gt=0)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    available = models.BooleanField('Доступность', default=False, help_text='Доступно для заказа')

    supplier = models.ForeignKey(Supplier, related_name='products', on_delete=models.CASCADE)
    set_number = models.CharField('Артикул поставщика', max_length=255)
    supplier_quantity = models.IntegerField('Количество на складе')
    supplier_price = models.DecimalField('Цена поставщика', decimal_places=2, max_digits=7)

    price = models.DecimalField('Розничная цена', decimal_places=0, max_digits=7)
    discount = models.PositiveSmallIntegerField('Скидка %', default=0, blank=True,
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])

    objects = ProductManager.from_queryset(ProductQuerySet)()

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        if self.discount:
            return self.price - self.price * self.discount/100
        else:
            return self.price

    @property
    def shot_description(self):  # TODO добавить поле
        return 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'

    @property
    def description(self):  # TODO добавить поле
        return 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore' \
               ' et dolore magna aliqua. Ut enim ad minim veniam, quis noexercit ullamco laboris nisi ut aliquip ex' \
               ' ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore' \
               ' eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia' \
               ' deserunt mollit anim id.'

    @property
    def quantity(self):
        return self.supplier_quantity
