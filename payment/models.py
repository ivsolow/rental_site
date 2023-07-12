from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class CreatedPayment(models.Model):
    user_id = models.IntegerField()
    idempotence_key = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(default='Created')


class UserPaymentDetails(models.Model):
    user_id = models.IntegerField()
    payment_id = models.CharField(max_length=36)
    idempotence_key = models.CharField(max_length=36)
    date_payment = models.DateTimeField(default=timezone.now)
    amount_value = models.DecimalField(max_digits=10, decimal_places=2)
    amount_currency = models.CharField(max_length=3)
    income_amount_value = models.DecimalField(max_digits=10, decimal_places=2)
    income_amount_currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)

    def __str__(self):
        user = User.objects.get(id=self.user_id)
        return f'payment by {str(self.date_payment)} from {user.email}'
