from django.db       import models

from users.models    import User
from products.models import Product
from core.models     import TimeStampModel

class OrderStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = "order_statuses"

class Order(models.Model):
    user                = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status        = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    order_num           = models.IntegerField()
    ordered_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

class OrderItemStatus(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = "order_item_statuses"

class Shipment(models.Model):
    tracking_number = models.CharField(max_length=40)

    class Meta:
        db_table = "shipments"

class OrderItem(models.Model):
    order             = models.ForeignKey('Order', on_delete=models.CASCADE)
    product           = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity          = models.IntegerField()
    order_item_status = models.ForeignKey('OrderItemStatus', on_delete=models.CASCADE)
    shipment          = models.ForeignKey('Shipment', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "orderitems"