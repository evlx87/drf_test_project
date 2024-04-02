import stripe
from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_course_payment(course, price):
    product_stripe = stripe.Product.create(name=course)

    price_stripe = stripe.Price.create(
        currency="usd",
        unit_amount=price,
        recurring={"interval": "month"},
        product=product_stripe.id,
    )

    session_stripe = stripe.checkout.Session.create(
        mode="subscription",
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price_stripe.id,
                "quantity": 1,
            }
        ]
    )

    return session_stripe
