from flask import Flask, render_template, redirect, request, jsonify
from adyen_api import ady

app = Flask(__name__) #Instanciate a Flask app object

app.secret_key = "Test" #Set the object's secret_key attribute 

@app.route('/')
def confirm_app():

    return "Hello"

@app.route('/paymentMethods', methods = ['POST'])
def get_avail_methods():
    '''get a list of payment methods available to your shopper''' 
    
    result = ady.checkout.payment_methods({
        'merchantAccount': 'YOUR_MERCHANT_ACCOUNT',
        'countryCode': 'NL',
        'amount': {
                'value': 1000,
                'currency': 'EUR'
        },
        'channel': 'Web',
    })

    return result


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')