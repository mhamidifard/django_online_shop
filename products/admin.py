from django.contrib import admin
from .models import Category, Product, ProductVariant

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0



class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_available', 'created_at', 'updated_at')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]
    readonly_fields = ('created_at', 'updated_at')


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'stock', 'formatted_attributes')
    list_filter = ('product',)
    search_fields = ('product__name',)
    readonly_fields = ()

    def formatted_attributes(self, obj):
        return str(obj.attributes)
    formatted_attributes.short_description = 'Attributes'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
