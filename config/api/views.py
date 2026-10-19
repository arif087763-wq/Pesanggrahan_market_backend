import uuid
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Category, Producer, Product, ProductImage
from .serializers import CategorySerializer, ProducerSerializer, ProductSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'

# KELAS INI TELAH DIPERBAIKI (Diubah jadi ModelViewSet)
class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.filter(is_active=True)
    serializer_class = ProducerSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly] 

    # Fungsi ini diletakkan dengan benar di dalam ProducerViewSet
    def perform_create(self, serializer):
        # Tangkap nama usaha untuk dijadikan slug unik
        nama_usaha = self.request.data.get('business_name', 'umkm')
        slug_dasar = slugify(nama_usaha) or 'umkm'
        unique_slug = f"{slug_dasar}-{uuid.uuid4().hex[:6]}"
        
        # Simpan ke database dengan slug yang sudah digenerate
        serializer.save(slug=unique_slug, is_active=True)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly] 
    
    # Aktifkan parser agar Django menerima upload berkas multipart/form-data
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Product.objects.all()
            
        return Product.objects.filter(
            publication_status='published',
            category__is_active=True,
            producer__is_active=True
        )
        
    def perform_create(self, serializer):
        # 1. Tangkap ID Kategori, Produsen, dan Unit
        kategori_id = self.request.data.get('category') or self.request.data.get('category_id')
        penjual_id = self.request.data.get('producer') or self.request.data.get('producer_id') or 1
        unit_val = self.request.data.get('unit') or 'item'
        
        # 2. Buat slug unik otomatis menggunakan UUID pendek untuk mencegah bentrok
        nama_produk = self.request.data.get('name', 'produk')
        slug_dasar = slugify(nama_produk) or 'produk'
        unique_slug = f"{slug_dasar}-{uuid.uuid4().hex[:6]}"

        # 3. Simpan data Produk utama
        product = serializer.save(
            slug=unique_slug,
            category_id=kategori_id, 
            producer_id=penjual_id,
            unit=unit_val,
            publication_status='published', # Paksa status menjadi published
        )

        # 4. Tangkap file foto & simpan ke model ProductImage
        image_file = self.request.FILES.get('image')
        if image_file:
            ProductImage.objects.create(
                product=product,
                image=image_file,
                alt_text=product.name,
                sort_order=0
            )