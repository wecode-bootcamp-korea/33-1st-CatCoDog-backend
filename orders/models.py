from django.db import models

from core.models import TimeStampedModel

class OrderStatus(models.Model):
    status = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'order_status'

    def __str__(self):
        return self.status

class OrderItemStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'order_item_status'

    def __str__(self):
        return self.status

class Order(TimeStampedModel):
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')
    status        = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, default=1, null=True, related_name='orders')
    shipping_cost = models.PositiveIntegerField()
    address       = models.CharField(max_length=200)

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_status     = models.ForeignKey(OrderItemStatus, on_delete=models.SET_NULL, default=1, null=True, related_name='items')
    product_option  = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE, related_name='items')
    quantity        = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_items'

class Cart(TimeStampedModel):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_option = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE, related_name='carts')
    quantity       = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'