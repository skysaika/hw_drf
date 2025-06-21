import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(course, user):
    intent = stripe.PaymentIntent.create(
        amount=int(course.price * 100),  # цена в центах
        currency='usd',
        automatic_payment_methods={'enabled': True},
        metadata={'user_id': user.id, 'course_id': course.id}
    )
    return intent

def retrieve_payment_intent(payment_intent_id):
    intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    return intent