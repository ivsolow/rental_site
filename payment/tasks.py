from celery import shared_task


@shared_task
def task_send_payment_email(new_rental_detail, total_paid_sum, user_id):

    from services.payment.received_payment_operations import send_email_success_payment  # noqa: E501

    send_email_success_payment(new_rental_detail, total_paid_sum, user_id)

    return "The email has been sent successfully"
