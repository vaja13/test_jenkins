from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///microservice_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class prediction_log(db.Model):
    __tablename__ = 'prediction_log'
    id = db.Column(db.Integer, primary_key=True)
    sl = db.Column(db.Float, nullable=False)
    sw = db.Column(db.Float, nullable=False)
    pl = db.Column(db.Float, nullable=False)
    pw = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String(50), nullable=False)


@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()
    new_log = prediction_log(
        sl=data['features'][0],
        sw=data['features'][1],
        pl=data['features'][2],
        pw=data['features'][3],
        prediction=data['prediction']
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"message": "Data logged successfully"}), 201

@app.route('/view_pred', methods=['get'])
def view_pred():
    logs = prediction_log.query.all()
    output = []
    for log in logs:
        log_data = {
            "id": log.id,
            "sepal_length": log.sl,
            "sepal_width": log.sw,
            "petal_length": log.pl,
            "petal_width": log.pw,
            "prediction": log.prediction
        }
        output.append(log_data)
    return jsonify({"logs": output}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5003)