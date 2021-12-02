import factory

from apps.catalog.models import Product, Category, Supplier


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: "Category %03d" % n)


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    title = factory.Sequence(lambda n: "Supplier %03d" % n)
    markup = 30


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Sequence(lambda n: "Product %03d" % n)
    shot_description = 'shot_description'
    description = 'description'

    category = factory.SubFactory(CategoryFactory)
    available = True

    supplier = factory.SubFactory(SupplierFactory)
    set_number = factory.Sequence(lambda n: "set_number %03d" % n)
    supplier_quantity = 3
    supplier_price = 1000

    price = 1500
