from rest_framework import serializers
from .models import Category, Producer, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'business_name', 'slug', 'description', 'whatsapp_number', 'address', 'is_active']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        # SESUAIKAN DENGAN models.py: nama field-nya adalah 'image'
        fields = ['id', 'image', 'alt_text', 'sort_order']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    producer = ProducerSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    # Field sementara penampung foto dari Flutter saat POST
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'availability_status', 'publication_status', 'is_featured', 
            'category', 'producer', 'images', 'image', 'created_at', 'unit'
        ]

    def create(self, validated_data):
        # Hapus 'image' dari data yang akan di-save ke tabel Product
        validated_data.pop('image', None)
        
        # Lanjutkan proses save standar (sekarang sudah aman tanpa kolom 'image')
        return super().create(validated_data)