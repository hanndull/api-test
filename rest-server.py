### http://blog.luisrei.com/articles/flaskrest.html

from flask import Flask, url_for, request, json, Response, jsonify

app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/articles')
def api_articles():
    return 'List of' + url_for('api_articles')


@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid


@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello, ' + request.args['name']
    else:
        return 'Hello, John Doe'


@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PATCH\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE\n"


@app.route('/messages', methods = ['POST'])
def api_message():
    
    if request.headers['Content-Type'] == 'text/plain':
        return 'Text Message: ' + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"         


@app.route('/hello2', methods = ['GET'])
def api_hello2():
    data = {
        'hello': 'world',
        'number': 3
    }
    # js = json.dumps(data)

    # resp = Response(js, status=200, mimetype='application/json')
    resp = jsonify(data)
    resp.status_code = 200

    resp.headers['Link'] = 'http://luisrei.com'

    return resp


@app.route('/payment', methods = ['POST'])
def show_payment_status():

    if request.method == 'POST':
        
        return "ECHO: POST\n" + json.dumps(request.json)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/users/<userid>', methods = ['GET'])
def api_users(userid):
    users = {'1':'john', '2':'steve', '3':'bill'}

    if userid in users:
        return jsonify({userid:users[userid]})
    else: 
        return not_found()


if __name__ == '__main__':
    app.run()
