from django.utils import timezone

from cart.models import Cart
from payment.models import CreatedPayment, UserPaymentDetails
from rentals.models import Rentals
from users.models import CustomUser


def validate_and_create_payment(webhook_data: dict) -> bool:
    """Валидация ответа от Юкассы по ключу idempotence_key,
    а также создание новой аренды в случае успеха"""
    payment_data = webhook_data['object']
    idempotence_key = payment_data['metadata']['idempotence_key']
    created_payment = CreatedPayment.objects.filter(idempotence_key=idempotence_key)
    if not created_payment.exists():
        return False
    payment_status = webhook_data['event']
    if payment_status == 'payment.succeeded':
        user_id = int(payment_data['metadata']['user_id'])
        start_new_rental(user_id)
        create_new_rental_info(payment_data, idempotence_key)
    # обновление статуса оплаты
    update_payment_data = created_payment.update(payment_status=payment_status)
    return True


def start_new_rental(user_id: int) -> None:
    """
    В случае успешной оплаты у пользователя создаются
    объекты аренды, а корзина очищается
    """
    user = CustomUser.objects.filter(id=user_id)
    cart_equipment = Cart.objects.filter(user=user_id)

    for cart_item in cart_equipment:
        rental = Rentals.objects.create(
            equipment=cart_item.equipment,
            user=user[0],
            amount=cart_item.amount,
            date_start=cart_item.date_start,
            date_end=cart_item.date_end
        )

    # Удаление записей из таблицы Cart
    cart_equipment.delete()


def create_new_rental_info(payment_data: dict, idempotence_key: str) -> None:
    """Запись информации об успешном платеже"""
    paid_amount = payment_data['amount']['value']
    payment = UserPaymentDetails.objects.create(
        payment_id=payment_data['id'],
        idempotence_key=idempotence_key,
        date_payment=timezone.now(),
        amount_value=paid_amount,
        amount_currency=payment_data['amount']['currency'],
        income_amount_value=payment_data['income_amount']['value'],
        income_amount_currency=payment_data['income_amount']['currency'],
        description=payment_data['description'])
