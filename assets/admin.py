from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Asset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'icon']
    prepopulated_fields = {'slug': ('name',)}


class PendingFilter(admin.SimpleListFilter):
    title = 'moderation queue'
    parameter_name = 'queue'

    def lookups(self, request, model_admin):
        return [('pending', 'Needs Review')]

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.filter(status='pending')
        return queryset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'status_badge', 'verified', 'address', 'submitted_at']
    list_filter = [PendingFilter, 'status', 'category', 'verified']
    search_fields = ['name', 'description', 'address']
    list_editable = ['verified']
    readonly_fields = ['submitted_at', 'map_preview']
    fieldsets = [
        ('Asset Info', {'fields': ['name', 'category', 'description', 'tags']}),
        ('Location', {'fields': ['address', 'latitude', 'longitude', 'map_preview']}),
        ('Contact', {'fields': ['phone', 'website', 'hours']}),
        ('Media', {'fields': ['photo']}),
        ('Moderation', {'fields': ['status', 'verified', 'notes', 'submitted_by', 'submitted_at']}),
    ]
    actions = ['approve_assets', 'archive_assets']

    def status_badge(self, obj):
        colors = {'pending': '#f0ad4e', 'active': '#5cb85c', 'archived': '#aaa'}
        color = colors.get(obj.status, '#aaa')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:3px;font-size:11px">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def map_preview(self, obj):
        if obj.latitude and obj.longitude:
            return format_html(
                '<a href="https://www.openstreetmap.org/?mlat={}&mlon={}#map=16/{}/{}" target="_blank">'
                'View on OpenStreetMap</a>',
                obj.latitude, obj.longitude, obj.latitude, obj.longitude
            )
        return '—'
    map_preview.short_description = 'Map'

    def approve_assets(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} asset(s) approved.')
    approve_assets.short_description = 'Approve selected assets'

    def archive_assets(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} asset(s) archived.')
    archive_assets.short_description = 'Archive selected assets'
