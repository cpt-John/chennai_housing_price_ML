from flask import Flask, request
from model import predict

app = Flask(__name__, static_url_path='',
            static_folder='client',)


@app.route('/<path:path>')
def serve(path):
    return app.send_static_file(path)


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    request_data = request.form
    response = predict(request_data.to_dict())
    return str(response)
