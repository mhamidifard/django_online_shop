import factory
from products.models import Category, Product, ProductVariant
from accounts.tests.factories import UserFactory

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")
    description = "Category description"

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    seller = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    name = factory.Sequence(lambda n: f"Product {n}")
    slug = factory.Sequence(lambda n: f"product-{n}")
    description = "Product description"
    is_available = True

class ProductVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    price = "99.99"
    stock = 10
    attributes = {}
