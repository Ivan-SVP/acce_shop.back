from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.models import Product

User = get_user_model()


class Order(models.Model):
    """Заказ."""
    name = models.CharField('Имя / ФИО', max_length=255)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=15)
    address = models.TextField('Адрес', help_text='Нужен для доставки', null=True, blank=True)
    comment = models.TextField('Комментарий', null=True, blank=True)

    created_at = models.DateTimeField('Создан', auto_now_add=True)
    uuid = models.UUIDField('Технический идентификатор', unique=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='order_items',
                                on_delete=models.PROTECT)

    price = models.DecimalField('Цена', help_text='Цена на момент оформления', decimal_places=0, max_digits=7)
    quantity = models.PositiveIntegerField('Количество', validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.id} - {self.order_id} - {self.product_id}'
