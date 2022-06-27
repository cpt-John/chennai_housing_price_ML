from flask import Flask, request
import pandas as pd
from model import predict

app = Flask(__name__, static_url_path='',
            static_folder='client',)


@app.route('/')
def serve():
    return app.send_static_file('index.html')


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    request_data = request.form
    # input_data =\
    # {'AREA': 'Karapakkam', 'INT_SQFT': 1004, 'DATE_SALE': '04-05-2011',
    # 'N_BEDROOM':1.0, 'N_BATHROOM': 1.0, 'N_ROOM': 3, 'SALE_COND': 'AbNormal',
    # 'PARK_FACIL': 'Yes', 'DATE_BUILD': '15-05-1967', 'BUILDTYPE': 'Commercial',
    # 'UTILITY_AVAIL': 'AllPub', 'STREET': 'Paved', 'MZZONE': 'A'}
    input_dict = {k: [float(v)] if v.isnumeric() else [str(v)]
                  for k, v in request_data.to_dict().items()}
    input_df = pd.DataFrame(input_dict)
    response_df = predict(input_df).head(1)
    # {'lower': 7219814.472497235,
    # 'mid': 7679321.769228897,
    # 'upper': 8034817.339012834}
    response = dict(zip(response_df.to_dict('split')[
        'columns'], response_df.to_dict('split')['data'][0]))
    return response
