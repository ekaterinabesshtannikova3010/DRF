import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_price(product_id, amount, currency='usd'):
    price = stripe.Price.create(
        unit_amount=amount,
        currency=currency,
        product=product_id,
    )
    return price


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/swagger/',
    )
    return session


def process_payment(product_name, amount):
    product = create_product(product_name)
    price = create_price(product.id, amount * 100)  # Умножаем на 100 для копеек
    session = create_checkout_session(price.id)
    return session.url  # Возвращаем ссылку на оплату


def retrieve_session(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    return session
