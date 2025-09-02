from django.db import models
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_size')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True)
    stock = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock) for {self.product.name} "


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products/main')
    # available
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/extra')
