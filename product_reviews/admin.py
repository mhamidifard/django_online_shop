from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'user__email')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['product', 'user']
    ordering = ('-created_at',)
