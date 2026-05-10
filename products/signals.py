from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Category, ProductVariant, ProductImage

@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    cache.delete('categories_root_list')
    cache.delete('products_list')

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete('products_list')
    cache.delete(f'product_detail_{instance.pk}')

@receiver([post_save, post_delete], sender=ProductVariant)
def invalidate_variant_cache(sender, instance, **kwargs):
    cache.delete('products_list')
    cache.delete(f'product_detail_{instance.product_id}')

@receiver([post_save, post_delete], sender=ProductImage)
def invalidate_image_cache(sender, instance, **kwargs):
    cache.delete('products_list')
    cache.delete(f'product_detail_{instance.product_id}')
