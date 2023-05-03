
from flask import Flask,  request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# create an instance of flask
app = Flask(__name__)
# creating an API object
api = Api(app)
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#sqlalchemy mapper
db = SQLAlchemy(app)

# add a class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    phonenumber=db.Column(db.String(10),unique=True)
    gender = db.Column(db.String(8), nullable=False)
    date=db.Column(db.String(10),nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(16),nullable=False)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} "



# For GET request to http://localhost:5000/
class GetUser(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users :
            user_data = {'Id': user.id, 'FirstName':user.firstname, 'LastName': user.lastname, 'Gender': user.gender,
                        'PhoneNumber': user.phonenumber,'Date': user.date,
                        'UserName': user.username,
                        'Email': user.email,
                        'Password': user.password}
            user_list.append(user_data)
        return {"Users": user_list}, 200

# # For Post request to http://localhost:5000/employee
class AddUser(Resource):
    def post(self):
        if request.is_json:
            user = User(firstname=request.json['FirstName'], lastname=request.json['LastName'],
                       gender=request.json['Gender'], phonenumber=request.json['PhoneNumber']
                       , date=request.json['Date'],
                         username=request.json['UserName']
                         , email=request.json['Email']
                          , password=request.json['Password']
                          )
            db.session.add(user)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'Id': user.id, 'First Name': user.firstname, 'Last Name': user.lastname,
                                          'Gender': user.gender, 'Phone Number': user.phonenumber
                                          , 'Date': user.date
                                          , 'User Name': user.username
                                          , 'Email': user.email
                                          , 'Password': user.password}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400

# # For put request to http://localhost:5000/update/?
class UpdateUser(Resource):
    def put(self, id):
        if request.is_json:
            user = User.query.get(id)
            if user is None:
                return {'error': 'not found'}, 404
            else:
                user.firstname = request.json['FirstName']
                user.lastname = request.json['LastName']
                user.gender = request.json['Gender']
                user.phonenumber = request.json['PhoneNumber']
                user.date = request.json['Date']
                user.username = request.json['UserName']
                user.password = request.json['Password']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

# For delete request to http://localhost:5000/delete/?
class DeleteUser(Resource):
    def delete(self, id):
        user = User.query.get(id)
        if user is None:
            return {'error': 'not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return f'{id} is deleted', 200


api.add_resource(GetUser, '/')
api.add_resource(AddUser, '/add')
api.add_resource(UpdateUser, '/update/<int:id>')
api.add_resource(DeleteUser, '/delete/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)

