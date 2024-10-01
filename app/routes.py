from flask import jsonify, render_template, request
from app import app
from app.data_service import fetch_stock_data, predict_stock_price

@app.route('/')
def index():
    return render_template('index.html')

# API to fetch stock data from PostgreSQL database
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        stock_data = fetch_stock_data(symbol, start_date, end_date)
        if stock_data:
            return jsonify(stock_data)
        else:
            return jsonify({'error': 'Stock data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to predict stock prices
@app.route('/api/predict/<symbol>', methods=['GET'])
def get_stock_prediction(symbol):
    try:
        prediction = predict_stock_price(symbol)
        if prediction is None:
            return jsonify({'error': 'Prediction could not be generated'}), 404
        return jsonify({
            "predicted_dates": prediction["predicted_dates"],
            "predicted_prices": prediction["predicted_prices"]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
