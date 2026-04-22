from django.db import models
from django.utils import timezone


class PriceHistory(models.Model):
    symbol = models.CharField(max_length=32, db_index=True)
    price = models.FloatField()
    created_at_utc = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-id"]
