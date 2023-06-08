from payment.models import CreatedPayment


def get_payment_status(idempotence_key: str) -> dict:
    """Получение статуса оплаты и удаление объекта хранения статуса в случае успеха"""
    created_payment = CreatedPayment.objects.filter(idempotence_key=idempotence_key)
    if created_payment:
        payment = created_payment.first()
        amount = payment.amount
        payment_status = payment.payment_status
        response_message = {
            "amount": str(amount),
            "status": payment_status
        }
        if payment_status == 'payment.succeeded':
            CreatedPayment.objects.filter(idempotence_key=idempotence_key).delete()
        return response_message
    return {}
