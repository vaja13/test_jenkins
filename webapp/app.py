from flask import Flask, request, render_template
import pickle
import numpy as np
from waitress import serve
import requests

app = Flask(__name__)
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

DATABASE_URI = "http://composedbapp:5003"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    features = [np.array(features)]
    
    prediction = model.predict(features)
    
    iris_classes = ['setosa', 'versicolor', 'virginica']
    output = iris_classes[prediction[0]]
    
    r = requests.post(f"{DATABASE_URI}/send_data", json={"features": features[0].tolist(), "prediction": output})

    return render_template('index.html', 
                         prediction_text=f'The flower is predicted to be: {output}')

@app.route('/view_pred', methods=['GET'])
def view_pred():
    try:
        r = requests.get(f"{DATABASE_URI}/view_pred")
        if r.status_code != 200:
            return render_template('view.html', 
                                error=f"Database service returned status code: {r.status_code}")
        
        try:
            data = r.json()
            return render_template('view.html', logs=data.get('logs', []))
        except ValueError:  # includes JSONDecodeError
            return render_template('view.html', 
                                error="Invalid response from database service")
            
    except requests.ConnectionError:
        return render_template('view.html', 
                            error="Could not connect to database service. Is it running?")

if __name__ == '__main__':
    # app.run(host="0.0.0.0",port = 5050,debug = True)
    serve(app, host="0.0.0.0", port=5001)