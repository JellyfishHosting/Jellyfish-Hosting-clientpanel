from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from config import oauth_uri, client_id_paypal, client_secret_paypal
from zenora import APIClient
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "live",
    "client_id": client_id_paypal,
    "client_secret": client_secret_paypal
})


testbp = Blueprint('payment', __name__, template_folder="templates")
@testbp.route('/payment', methods=['GET', 'POST'])
def payment():
    if "token" in session:
        item_name = request.form['item_name']
        item_price = request.form['item_price']

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "https://my.jellyfishhosting.xyz/execute",
                "cancel_url": "https://my.jellyfishhosting.xyz/dashboard"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": item_name,
                        "sku": "12345",
                        "price": item_price,
                        "currency": "GBP",
                        "quantity": 1}]},
                "amount": {
                    "total": item_price,
                    "currency": "GBP"},
                "description": f"This is the payment transaction for {item_name}."}]})
    
        if payment.create():
            print('Payment Success!')
            return jsonify({'paymentID': payment.id})
        else:
            print(payment.error)
            return jsonify({'error': 'Payment creation failed'})
    else:
        return redirect(url_for('login.login'))