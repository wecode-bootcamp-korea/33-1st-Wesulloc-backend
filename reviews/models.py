from django.db import models

class Review(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    content     = models.TextField()
    rating      = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    created_at  = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "reviews"
    
class ReviewImage(models.Model):
    review  = models.ForeignKey('Review', on_delete=models.CASCADE)
    img_url = models.URLField(max_length=500)

    class Meta:
        db_table = "review_images"