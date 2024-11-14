from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)

    def dictionary(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "user_password": self.user_password,
            "age": self.age
        }


with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = user(
        user_name=data['user_name'],
        user_email=data['user_email'],
        user_password=data['user_password'],
        age=data.get('age')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.dictionary()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = user.query.all()
    return jsonify([user.dictionary() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    result = user.query.get_or_404(user_id)
    return jsonify(result.dictionary())

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    result = user.query.get_or_404(user_id)
    result.user_name = data.get('user_name', result.user_name)
    result.user_email = data.get('user_email', result.user_email)
    result.user_password = data.get('user_password', result.user_password)
    result.age = data.get('age', result.age)
    db.session.commit()
    return jsonify(result.dictionary())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user.query.get_or_404(user_id)
    db.session.delete(result)
    db.session.commit()
    return jsonify({"message": "user deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
