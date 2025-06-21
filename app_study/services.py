import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(course, user):
    # Предположим, course.price в USD, например 9.99
    amount_in_cents = int(course.price * 100)
    if amount_in_cents < 50:
        raise ValueError("Сумма должна быть не менее 0.50 USD")

    return stripe.PaymentIntent.create(
        amount=amount_in_cents,
        currency='usd',
        metadata={'user_id': user.id, 'course_id': course.id},
    )

def retrieve_payment_intent(payment_intent_id):
    intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    return intent