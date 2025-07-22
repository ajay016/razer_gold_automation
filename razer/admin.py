from django.contrib import admin
from .models import *






@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'url')
    search_fields = ('name', 'code')


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'region', 'status')
    list_filter = ('status', 'region')
    search_fields = ('name', 'email', 'phone')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    filter_horizontal = ('regions',)  # optional for better region selection UI


class ProductScheduleInline(admin.TabularInline):
    model = ProductSchedule
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_scheduled', 'created_at', 'updated_at')
    list_filter = ('status', 'is_scheduled')
    search_fields = ('name',)
    inlines = [ProductVariantInline, ProductScheduleInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'quantity')
    list_filter = ('regions',)
    search_fields = ('name', 'product__name')
    filter_horizontal = ('regions',)


@admin.register(ProductSchedule)
class ProductScheduleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'scheduled_time', 'repeat', 'is_active', 'last_run_at')
    list_filter = ('repeat', 'is_active')
    search_fields = ('product__name',)