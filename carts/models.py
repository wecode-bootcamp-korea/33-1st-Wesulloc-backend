from django.db import models

from core.models import TimeStampModel

class Cart(TimeStampModel):
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        db_table    = "carts"
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "product"],
                name   = "unique carts"
            )
        ]