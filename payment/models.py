from django.db import models
from django.utils import timezone


class CreatedPayment(models.Model):
    user_id = models.IntegerField()
    idempotence_key = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(default='Created')


class UserPaymentDetails(models.Model):
    payment_id = models.CharField(max_length=36)
    idempotence_key = models.CharField(max_length=36)
    date_payment = models.DateTimeField(default=timezone.now)
    amount_value = models.DecimalField(max_digits=10, decimal_places=2)
    amount_currency = models.CharField(max_length=3)
    income_amount_value = models.DecimalField(max_digits=10, decimal_places=2)
    income_amount_currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)


