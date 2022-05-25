from django.db import models

from core.models import TimeStampedModel

class Product(TimeStampedModel):
    name          = models.CharField(max_length=15)
    description   = models.TextField()
    thumbnail_url = models.URLField(max_length=600)
    discount_rate = models.PositiveIntegerField()

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

class Category(models.Model):
    name    = models.CharField(max_length=50, unique=True)
    product = models.ManyToManyField('product', through='productcategory', related_name='category')

    class Meta:
        db_table='categories'

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    product  = models.ForeignKey('product', on_delete=models.CASCADE)
    category = models.ForeignKey('category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_categories'

class ProductImage(models.Model):
    url       = models.URLField(max_length=600)
    product   = models.ForeignKey('product', on_delete=models.CASCADE, related_name='image_url')

    class Meta:
        db_table = 'product_images'

class ProductOption(models.Model):
    product = models.ForeignKey('product', on_delete=models.CASCADE, related_name='options')
    name    = models.CharField(max_length=50)
    price   = models.DecimalField(max_digits=10, decimal_places=2)
    stock   = models.PositiveIntegerField()

    class Meta:
        db_table = 'product_options'

class ProductReview(TimeStampedModel):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('product', on_delete=models.CASCADE, related_name='reviews')
    content = models.CharField(max_length=300)
    rating  = models.PositiveIntegerField()

    class Meta:
        db_table = 'product_reviews'