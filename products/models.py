from django.db              import models
from users.models           import User, TimeStampModel
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Menu(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "menus"

class Category(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "categories"

class Product(models.Model):
    category      = models.ForeignKey('Category', on_delete=models.CASCADE)
    name          = models.CharField(max_length=50)
    price         = models.DecimalField(max_digits=10, decimal_places=0)
    description   = models.TextField()
    discount_rate = models.DecimalField(max_digits=3, decimal_places=0, validators=PERCENTAGE_VALIDATOR)

    class Meta:
        db_table = "products"

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    img_url = models.URLField()

    class Meta:
        db_table = "productimages"

class AdditionalProduct(models.Model):
    product            = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='additional_product')
    additional_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product')

    class Meta:
        db_table = "additionalproducts"

class Seasonal(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    name    = models.CharField(max_length=50)

    class Meta:
        db_table = "seasonals"

class Review(TimeStampModel):
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = "reviews"
    
class ReviewImage(models.Model):
    review  = models.ForeignKey('Review', on_delete=models.CASCADE)
    img_url = models.URLField()

    class Meta:
        db_table = "reviewimages"

class Cart(models.Model):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=0)
    
    class Meta:
        db_table = "carts"