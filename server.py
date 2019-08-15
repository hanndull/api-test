from flask import Flask, render_template, redirect, request, jsonify

app = Flask(__name__) #Instanciate a Flask app object

app.secret_key = "Test" #Set the object's secret_key attribute 

@app.route('/')
def confirm_app():

    return "Hello"


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')