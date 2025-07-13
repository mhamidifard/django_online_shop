from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_id', 'product_name', 'quantity', 'price', 'variant')
    can_delete = False
    show_change_link = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_status', 'total_amount', 'ordered_at')
    list_filter = ('status', 'payment_status', 'ordered_at')
    search_fields = ('id', 'user__username', 'user__email', 'transaction_id')
    readonly_fields = ('ordered_at',)
    inlines = [OrderItemInline]
    ordering = ('-ordered_at',)
    autocomplete_fields = ['user']

    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'payment_status', 'total_amount')
        }),
        ('Shipping & Payment', {
            'fields': ('shipping_address', 'payment_method', 'transaction_id')
        }),
        ('Additional', {
            'fields': ('notes', 'ordered_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price')
    list_filter = ('order',)
    search_fields = ('order__id', 'product_name', 'product_id')
    readonly_fields = ('order', 'product_id', 'product_name', 'quantity', 'price', 'variant')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'status', 'gateway', 'created_at')
    list_filter = ('status', 'gateway', 'created_at')
    search_fields = ('order__id', 'transaction_id', 'order__user__username')
    readonly_fields = ('created_at', 'updated_at', 'transaction_id', 'gateway_response')
    autocomplete_fields = ['order']
    ordering = ('-created_at',)
