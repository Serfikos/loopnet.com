from django.db import models

class Broker(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Должность")
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Компания")
    address = models.CharField(max_length=512, blank=True, null=True, verbose_name="Адрес")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Телефон")
    mobile = models.CharField(max_length=50, blank=True, null=True, verbose_name="Мобильный")
    bio = models.TextField(blank=True, null=True, verbose_name="Биография")
    specialties = models.TextField(blank=True, null=True, verbose_name="Специализации")
    property_types = models.TextField(blank=True, null=True, verbose_name="Типы недвижимости")
    markets = models.TextField(blank=True, null=True, verbose_name="Рынки")
    education = models.TextField(blank=True, null=True, verbose_name="Образование")
    affiliations = models.TextField(blank=True, null=True, verbose_name="Членство в организациях")
    awards = models.TextField(blank=True, null=True, verbose_name="Награды") # <-- НОВОЕ ПОЛЕ
    profile_url = models.URLField(unique=True, max_length=1024, verbose_name="Ссылка на профиль")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Брокер"
        verbose_name_plural = "Брокеры"
        ordering = ['id']

    def __str__(self):
        return self.name

class Listing(models.Model):
    STATUS_CHOICES = [
        ('New', 'Новая ссылка'),
        ('Done', 'Обработано'),
        ('Error', 'Ошибка'),
        ('Broker Info Done', 'Собрана инф. о брокере'),
    ]

    title = models.CharField(max_length=512, verbose_name="Название")
    url = models.URLField(unique=True, max_length=1024, verbose_name="Ссылка на объявление")
    agency_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Агентство")
    agency_url = models.URLField(max_length=1024, blank=True, null=True, verbose_name="Ссылка на агентство")
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Брокер")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Объявление (LoopNet)"
        verbose_name_plural = "Объявления (LoopNet)"
        ordering = ['id']

    def __str__(self):
        return self.title