from django.db              import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models           import User
from core.models            import TimeStampModel

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Menu(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "menus"

class MainCategory(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "main_categories"

class Category(models.Model):
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    name          = models.CharField(max_length=45)

    class Meta:
        db_table = "categories"

class CategoryProduct(models.Model): 
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = "categories_products"

class Product(models.Model):
    name          = models.CharField(max_length=50)
    price         = models.DecimalField(max_digits=10, decimal_places=0)
    description   = models.TextField()
    discount_rate = models.DecimalField(max_digits=3, decimal_places=0, validators=PERCENTAGE_VALIDATOR, null=True)

    class Meta:
        db_table = "products"

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    img_url = models.URLField(max_length=500)

    class Meta:
        db_table = "product_images"

class AdditionalProduct(models.Model):
    product            = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='additional_product')
    additional_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product')

    class Meta:
        db_table = "additional_products"

class Seasonal(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name    = models.CharField(max_length=45)

    class Meta:
        db_table = "seasonals"