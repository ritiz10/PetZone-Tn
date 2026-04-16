from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    password = data.get('password')

    if not phone or not password:
        return jsonify({"message": "Phone and Password are required"}), 400

    if User.query.filter_by(phone=phone).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(name=name, phone=phone, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account Created! Please Login."}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')

    user = User.query.filter_by(phone=phone, password=password).first()

    if user:
        return jsonify({
            "message": "Login successful",
            "user": {
                "name": user.name,
                "phone": user.phone
            }
        }), 200
    else:
        return jsonify({"message": "Invalid Login!"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
