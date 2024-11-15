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

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    userName = db.Column(db.String(255), nullable=False)
    userEmail = db.Column(db.String(255), nullable=False)
    userPassword = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)

    def dictionary(self):
        return {
            "userId": self.userId,
            "userName": self.userName,
            "userEmail": self.userEmail,
            "userPassword": self.userPassword,
            "age": self.age
        }

with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        userName=data['userName'],
        userEmail=data['userEmail'],
        userPassword=data['userPassword'],
        age=data.get('age')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.dictionary()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.dictionary() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    result = User.query.get_or_404(user_id)
    return jsonify(result.dictionary())

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    result = User.query.get_or_404(user_id)
    result.userName = data.get('userName', result.userName)
    result.userEmail = data.get('userEmail', result.userEmail)
    result.userPassword = data.get('userPassword', result.userPassword)
    result.age = data.get('age', result.age)
    db.session.commit()
    return jsonify(result.dictionary())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = User.query.get_or_404(user_id)
    db.session.delete(result)
    db.session.commit()
    return jsonify({"message": "user deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
