from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    account          = models.CharField(max_length=45, unique=True)
    password         = models.CharField(max_length=150)
    name             = models.CharField(max_length=45)
    address          = models.CharField(max_length=100)
    contact          = models.CharField(max_length=45, unique=True)
    birth            = models.DateField()
    email            = models.CharField(max_length=50)
    gender           = models.CharField(max_length=30)
    terms_agreements = models.JSONField()

    class Meta:
        db_table = "users"