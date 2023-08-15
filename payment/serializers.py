from rest_framework import serializers

from cart.models import Cart
from payment.models import CreatedPayment


class PaymentSerializer(serializers.ModelSerializer):
    payment_sum = serializers.IntegerField()
    commission = serializers.DecimalField(decimal_places=1, max_digits=4)

    class Meta:
        model = Cart
        fields = ['payment_sum', 'commission', ]


class PaymentStatusSerializer(serializers.ModelSerializer):
    idempotence_key = serializers.CharField()

    class Meta:
        model = CreatedPayment
        fields = ['idempotence_key', ]

