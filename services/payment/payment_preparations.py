import uuid

from yookassa import Configuration, Payment

from equipment_rental_site import settings
from payment.models import CreatedPayment
from users.models import CustomUser


def get_confirmation_url(user: CustomUser,
                         payment_sum: int,
                         commission: float) -> dict:
    """Receiving payment link from Yookassa"""
    Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    user_id = user.id
    value_with_commission = payment_sum * 1 / (1 - (commission / 100))
    idempotence_key = str(uuid.uuid4())

    return_url = 'https://example.com/'
    description = f'Оплата {round(value_with_commission, 2)} рублей, ' \
                  f'включая комиссию {commission} %'

    payment = Payment.create({
        "amount": {
            "value": value_with_commission,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": 'bank_card'
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "capture": True,
        "description": description,
        "metadata": {
            "user_id": user_id,
            "idempotence_key": idempotence_key
        }
    }, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url
    write_data_of_created_payment(user_id,
                                  idempotence_key,
                                  value_with_commission)

    payment_response = {
        'confirmation_url': confirmation_url,
        'idempotence_key': idempotence_key
    }
    return payment_response


def write_data_of_created_payment(user_id: int,
                                  idempotence_key: str,
                                  value_with_commission: float) -> None:
    """ Write data about the created payment into a new or existing table."""

    create_payment, created = CreatedPayment.objects.get_or_create(
        user_id=user_id,
        idempotence_key=idempotence_key,
        amount=value_with_commission
        )

    if not created:
        create_payment.idempotence_key = idempotence_key
        create_payment.amount = value_with_commission
        create_payment.save()
