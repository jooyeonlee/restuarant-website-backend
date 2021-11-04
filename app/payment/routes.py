from flask import Blueprint, jsonify, request
import stripe
import os

payment = Blueprint('payment', __name__)

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@payment.route('/pay', methods=['POST'])
def pay():
    try:
        data = request.get_json()
        
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],
            currency='usd'
        )
        return jsonify(client_secret=intent.client_secret)
    except Exception as e:
        return jsonify(error=str(e)), 403