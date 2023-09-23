from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

from cart.models import Cart
from payment.models import CreatedPayment, UserPaymentDetails
from payment.tasks import task_send_payment_email
from rentals.models import Rentals
from services.payment.exceptions import InvalidKeyPaymentException
from users.models import CustomUser


def create_new_payment(webhook_data: dict) -> dict:
    """
    Validate the YooKassa response using the idempotence_key
    and initiate a new rental upon successful payment.
    """
    validated_data = validate_webhook_data(webhook_data)

    payment_data = validated_data['payment_data']
    idempotence_key = validated_data['idempotence_key']
    created_payment = validated_data['created_payment']
    payment_status = validated_data['payment_status']

    created_payment.update(payment_status=payment_status)

    if payment_status == 'payment.succeeded':
        cache.delete(settings.RENTALS_CACHE_KEY)
        cache.delete(settings.AVAIL_EQUIPMENT_CACHE_KEY)

        user_id = int(payment_data['metadata']['user_id'])
        new_rental_detail = start_new_rental(user_id)
        total_paid_sum = create_new_rental_info(user_id,
                                                payment_data,
                                                idempotence_key)
        task_send_payment_email.delay(new_rental_detail,
                                      total_paid_sum,
                                      user_id)
        created_payment.delete()
    message = {
        "payment_status": f'{payment_status}'
    }
    return message


def validate_webhook_data(webhook_data: dict) -> dict:
    """Create rental objects for the user
    upon successful payment and clear the user's cart."""
    payment_data = webhook_data.get('object')
    if (not payment_data
            or not isinstance(payment_data, dict)
            or 'metadata' not in payment_data):
        raise ValueError('Invalid payment data')

    idempotence_key = payment_data['metadata'].get('idempotence_key')
    if not idempotence_key:
        raise ValueError('Invalid idempotence key')

    created_payment = (CreatedPayment.objects.
                       filter(idempotence_key=idempotence_key))
    if not created_payment.exists():
        raise InvalidKeyPaymentException()

    payment_status = webhook_data.get('event')
    if not payment_status:
        raise ValueError('Invalid payment status')

    result = {
        'payment_data': payment_data,
        'payment_status': payment_status,
        'created_payment': created_payment,
        'idempotence_key': idempotence_key
    }
    return result


def start_new_rental(user_id: int) -> list:
    """
    Create rental objects for the user
    upon successful payment and clear the user's cart.
    """
    cart_equipment = Cart.objects.filter(user_id=user_id)

    equipment_list = []
    for cart_item in cart_equipment:
        rental = Rentals.objects.create(  # noqa: F841
            equipment=cart_item.equipment,
            user_id=user_id,
            amount=cart_item.amount,
            date_start=cart_item.date_start,
            date_end=cart_item.date_end
        )

        item_summ = float(cart_item.equipment.price * cart_item.amount)

        equipment_data = {
            'equipment': cart_item.equipment.name,
            'amount': cart_item.amount,
            'date_start': str(cart_item.date_start),
            'date_end': str(cart_item.date_end),
            'item_summ': item_summ
        }

        equipment_list.append(equipment_data)

    cart_equipment.delete()
    return equipment_list


def create_new_rental_info(user_id: int,
                           payment_data: dict,
                           idempotence_key: str) -> int:
    """ Write information about a successful payment to the database."""
    paid_amount = payment_data['amount']['value']
    payment = UserPaymentDetails.objects.create(  # noqa: F841
        user_id=user_id,
        payment_id=payment_data['id'],
        idempotence_key=idempotence_key,
        date_payment=timezone.now(),
        amount_value=paid_amount,
        amount_currency=payment_data['amount']['currency'],
        income_amount_value=payment_data['income_amount']['value'],
        income_amount_currency=payment_data['income_amount']['currency'],
        description=payment_data['description'])
    return paid_amount


def send_email_success_payment(new_rental_detail: list,
                               total_paid_sum: int,
                               user_id: int) -> None:
    """Send an email notification for a successful payment."""
    message = (f'Оплата прошла успешно. '
               f'Спасибо, что воспользовались нашим прокатом.\n\n'
               f'Детали заказа: '
               f'\n {get_payment_details_string(new_rental_detail)}\n\n'
               f'Итоговая сумма: {total_paid_sum} рублей')

    user_email = CustomUser.objects.get(id=user_id).email
    subject = 'Payment Confirmation'
    from_email = 'rental_service-noreply@gmail.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def get_payment_details_string(new_rental_detail: list) -> str:
    details_string = ''
    for rental_item in new_rental_detail:
        details_string += (f"Снаряжение: {rental_item['equipment']}\n"
                           f"Количество: {rental_item['amount']}\n"
                           f"Даты проката: "
                           f"{rental_item['date_start']} "
                           f"- {rental_item['date_end']}\n"
                           f"Сумма: {rental_item['item_summ']} рублей\n"
                           f"{'_' * 40}\n")

    return details_string
