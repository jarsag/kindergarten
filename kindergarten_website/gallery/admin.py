from django.contrib import admin
from .models import GalleryCategory, GalleryPhoto

class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 1
    readonly_fields = ('views',)

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'photo_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryPhotoInline]

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at', 'views', 'is_active')
    list_filter = ('category', 'is_active', 'uploaded_at')
    search_fields = ('title', 'description')
    readonly_fields = ('views',)
    date_hierarchy = 'uploaded_at'