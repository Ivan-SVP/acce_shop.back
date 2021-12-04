from django.db import models


class Supplier(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    markup = models.IntegerField('Наценка %', help_text='Наценка для розницы')
    has_rrp = models.BooleanField('Есть РРЦ', default=False, help_text='Флаг наличия рекомендуемой розничной цены')
    url = models.URLField('Сайт', blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
