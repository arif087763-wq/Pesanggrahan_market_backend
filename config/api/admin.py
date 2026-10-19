from django.contrib import admin
from .models import Category,Producer,Product,ProductImage

class ProductImageInline(admin.TabularInline):
  model = ProductImage
  extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name','is_active','created_at')
  prepopulated_fields = {'slug':('name',)}
  search_fields = ('name',)

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
  list_display = ('business_name', 'whatsapp_number', 'is_active')
  prepopulated_fields = {'slug': ('business_name',)}
  search_fields = ('business_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'producer', 'price', 'publication_status', 'availability_status')
    list_filter = ('publication_status', 'availability_status', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline] # Memasukkan form upload foto ke dalam form produk

# Register your models here.
