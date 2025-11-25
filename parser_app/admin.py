from django.contrib import admin
from .models import Listing, Broker

@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'phone', 'mobile', 'profile_url')
    search_fields = ('name', 'company_name', 'profile_url')
    list_per_page = 50

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency_name', 'broker', 'status', 'url')
    list_filter = ('status', 'agency_name', 'broker__company_name')
    search_fields = ('title', 'agency_name', 'url', 'broker__name')
    list_per_page = 50
    actions = ['mark_as_new', 'mark_as_done']
    raw_id_fields = ('broker',)

    @admin.action(description="Сбросить статус на 'Новая ссылка' для повторного парсинга")
    def mark_as_new(self, request, queryset):
        queryset.update(status='New')
        
    @admin.action(description="Сбросить статус на 'Обработано' для парсинга брокеров")
    def mark_as_done(self, request, queryset):
        queryset.update(status='Done')