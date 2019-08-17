### Adyen API Endpoint ref: https://docs.adyen.com/api-reference/payments-api
### Note -- these requests need authentication each time. 

from flask import Flask, jsonify
import requests
import json
from adyen_api import USER, PW


app = Flask(__name__) #Instanciate a Flask app object
app.secret_key = "Test" #Set the object's secret_key attribute 


@app.route('/')
def confirm_app():


    data = { 
         "amount": {
           "currency": "USD",
           "value": 100
         },
         "paymentMethod":{
           "type":"scheme",
           "expiryYear":"2020",
           "expiryMonth":"10",
           "cvc":"737",
           "number":"4000020000000000",
           "holderName":"Hannah Johnson"
         },
         "merchantOrderReference": "Hannah Johnson",
         "reference":"HannahJohnson",
         "merchantAccount":"SFTestAccount"
        }

    data = jsonify(data)

    print (">>>>>>>> DATA", data)

    return data


@app.route('/authorize', methods=['GET', 'POST'])
def authorize_payment():

    api_endpoint = 'https://pal-test.adyen.com/pal/servlet/Payment/v46/authorise'
    
    data = { 
         "amount": {
           "currency": "USD",
           "value": 100
         },
         "card":{
           "expiryYear":"2020",
           "expiryMonth":"10",
           "cvc":"737",
           "number":"4000020000000000",
           "holderName":"Hannah Johnson"
         },
         "merchantOrderReference": "Hannah Johnson",
         "reference":"HannahJohnson",
         "merchantAccount":"SFTestAccount"
        }
        # "additionalData":{
        #   "merchantReference":"Hannah Johnson"
        # },
    data = jsonify(data)

    result = requests.post(api_endpoint, data, auth=(f'{USER}',f'{PW}'))
    print (">>>>>>>> RESULT", result)


    return jsonify(result)


@app.route('/capture', methods = ['GET', 'POST'])
def capture_funds():
    
    api_endpoint = 'https://pal-test.adyen.com/pal/servlet/Payment/v46/capture'

    data = ({  
       "merchantAccount":"SFTestAccount",
       "modificationAmount":{  
          "value":50,
          "currency":"USD"
       },
       "merchantOrderReference": "Hannah Johnson",
       "reference":"HannahJohnson", 
       "originalReference":"[TO FILL IN]" #returned in authorisation response
    })

    result = requests.post(url = api_endpoint, data = data, auth=(f'{USER}',f'{PW}'))

    return result 
    # Expected result like:
    #{"pspReference":"8825408195409505","response":"[capture-received]"}  


@app.route('/refund', methods = ['GET', 'POST'])
def refund_funds():

    api_endpoint = 'https://pal-test.adyen.com/pal/servlet/Payment/v46/refund'

    data = ({
       "merchantAccount":"SFTestAccount",
       "modificationAmount":{  
          "value":50,
          "currency":"USD"
       },
       "originalReference":"[TO FILL IN]",
       "reference":"HannahJohnson",    
    })

    result = requests.post(url = api_endpoint, data = data, auth=(f'{USER}',f'{PW}'))

    return result 

    #Reasoning for refunding only $50: 
    #Refunds a payment that has previously been captured, returning a unique reference for this request. Refunding can be done on the full captured amount or a partial amount. Multiple (partial) refunds will be accepted as long as their sum doesn't exceed the captured amount. Payments which have been authorised, but not captured, cannot be refunded, use the /cancel method instead.
    #https://docs.adyen.com/api-explorer/#/Payment/v46/refund


@app.route('/cancel', methods = ['GET', 'POST'])
def cancel_funds():

    api_endpoint = 'https://pal-test.adyen.com/pal/servlet/Payment/v46/cancel'
    
    data = ({
        "merchantAccount" : "SFTestAccount",
        "originalReference" : "[TO FILL IN]",
        "reference" : "HannahJohnson"
    })

    result = requests.post(url = api_endpoint, data = data, auth=(f'{USER}',f'{PW}'))

    #Reasoning for cancellation of remaining $50:
    #If you have authorised a payment but do not wish to capture it, for example because an item is out of stock, you need to cancel the authorisation. If the payment has already been captured, you need to refund it instead.
    #https://docs.adyen.com/development-resources/payment-modifications/cancel


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')