from flask import Flask,jsonify,make_response
from flask_restful import Resource, Api,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_httpauth import HTTPBasicAuth



app = Flask(__name__)
api = Api(app)
# auth=HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

#Register Arguments 
register_user_args=reqparse.RequestParser()
register_user_args.add_argument('firstname',type=str,required=True )
register_user_args.add_argument('lastname',type=str,required=True )
register_user_args.add_argument('phonenumber',type=str,required=True )
register_user_args.add_argument('gender',type=str,required=True )
register_user_args.add_argument('date',type=str,required=True )
register_user_args.add_argument('username',type=str,help="username required",required=True )
register_user_args.add_argument('email',type=str,help="email required",required=True )
register_user_args.add_argument('password',type=str,required=True )

#Login Arguments
login_user_args=reqparse.RequestParser()
login_user_args.add_argument('username',type=str,help="username required",required=True )
login_user_args.add_argument('password',type=str,required=True )


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

        args=register_user_args.parse_args()
        username=args['username']
        password=args['password']

        #  Check for blank requests
        if username is None or password is None:
            abort(400,message="OHHH This is Blank request")

        #Check for existing users
        user=User.query.filter_by(username=username).first()
        if user:
             abort(409, message="User already exists. Please Log in.")
            # return  make_response(jsonify({'message':'User already exists. Please Log in..' }), 409)

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
        message="User Successfully registered."
        abort(400,message="User Successfully registered.")     
         
        # return {'username': user.username,'password': user.password}, 201
        # return user.username,user.password
    
class Login(Resource): 

    def post(self):
        
        args=login_user_args.parse_args()
        username=args['username']
        password=args['password']
        # print(username,password)
        user=User.query.filter_by(username=username).first()
        # if user == None:
        #     return make_response(jsonify({'message': 'Username Is Incorrect'}), 407)
      
        
        # elif password == user.password :
        #     return make_response(jsonify({'response of User_id = ':user.id }), 200)
       
        # else :
        #     return make_response(jsonify({'message ':'Failure of login' }), 408)
        if user and password == user.password:
            return make_response(jsonify({'sussessful of login and id =':user.id }), 200)
        else :
             return make_response(jsonify({'message ':'Failure of login' }), 408)

        
# For GET request to http://localhost:5000/
class GetUser(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users :
            user_data = {'id': user.id, 'firstname':user.firstname, 'lastname': user.lastname, 'gender': user.gender,
                        'phonenumber': user.phonenumber,'date': user.date,
                        'username': user.username,
                        'email': user.email,
                        'password': user.password
                        }
            user_list.append(user_data)
        return {"Users": user_list}, 200
   

    
#Handle Request
api.add_resource(Register, '/register')
api.add_resource(GetUser, '/')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)

