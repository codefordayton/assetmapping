from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='info-sign')
    color = models.CharField(max_length=30, default='blue')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Asset(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='assets')
    description = models.TextField()
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    hours = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='assets/', blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, help_text='Comma-separated keywords')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_by = models.CharField(max_length=100, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text='Internal admin notes')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]
