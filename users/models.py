from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeStampModel):
    account          = models.CharField(max_length=45, unique=True)
    password         = models.CharField(max_length=150)
    name             = models.CharField(max_length=45)
    address          = models.CharField(max_length=100)
    contact          = models.CharField(max_length=50)
    birth            = models.DateField()
    email            = models.CharField(max_length=100, unique=True)
    gender           = models.CharField(max_length=50)
    terms_agreements = models.JSONField()

    class Meta:
        db_table = "users"
