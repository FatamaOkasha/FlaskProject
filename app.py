
from flask import Flask
from flask_restful import Resource, Api,reqparse,abort, fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db=SQLAlchemy(app)

user_args=reqparse.RequestParser()
user_args.add_argument('firstname',type=str,required=True )
user_args.add_argument('lastname',type=str,required=True )
user_args.add_argument('phonenumber',type=str,required=True )
user_args.add_argument('gender',type=str,required=True )
user_args.add_argument('date',type=str,required=True )
user_args.add_argument('username',type=str,help="username required",required=True )
user_args.add_argument('email',type=str,help="email required",required=True )
user_args.add_argument('password',type=str,required=True )

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

user_resource_field = {
    "id":fields.Integer,
    "firstname":fields.String,
    "lastname":fields.String,
    "phonenumber":fields.String,
    "gender":fields.String,
    "date":fields.String,
    "username":fields.String,
    "email":fields.String,
    "password":fields.String

}

# db.create_all()
class Register(Resource):
    @marshal_with(user_resource_field)
    def put(self):
        args=user_args.parse_args()
        #check username already taken or not 
        username=args['username']
        user=User.query.filter_by(username=username).first()
        if user:
            abort(409, message="User already registered with username")
        user=User(
                  firstname=args['firstname'],
                  lastname=args['lastname'],
                  phonenumber=args['phonenumber'],
                  gender=args['gender'],
                  date=args['date'],
                  username=args['username'],
                  email=args['email'],
                  password=args['password'] )
        db.session.add(user)
        db.session.commit()
        return  user
    
#Handle Request
api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(debug=True)