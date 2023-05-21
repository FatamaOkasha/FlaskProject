from flask import Flask,jsonify,make_response,request
from flask_restful import Resource, Api,reqparse,abort,fields,marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt 
import datetime


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY']='thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parkinsoninfo.db'
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


#Update Arguments 
# Update_user_args=reqparse.RequestParser()
# Update_user_args.add_argument('firstname',type=str,required=True )
# Update_user_args.add_argument('lastname',type=str,required=True )
# Update_user_args.add_argument('phonenumber',type=str,required=True )
# Update_user_args.add_argument('gender',type=str,required=True )
# Update_user_args.add_argument('date',type=str,required=True )
# Update_user_args.add_argument('username',type=str,help="username required",required=True )
# Update_user_args.add_argument('email',type=str,help="email required",required=True )
# Update_user_args.add_argument('password',type=str,required=True )



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
#####################################REGISTERRRRRRRRR###############################################################################
class Register(Resource):
    @marshal_with(user_resource_field)

    def put(self):

        args=register_user_args.parse_args()
        username=args['username']
        password=args['password']
        hashed_password=generate_password_hash(password ,method='sha256')
    
    

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
                  password=hashed_password )
      
        db.session.add(user)
        db.session.commit()
        # message="User Successfully registered."
        abort(400,message="User Successfully registered.")     
         
        # return {'username': user.username,'password': user.password}, 201
        # return user.username,user.password
class Login(Resource): 
      def post (self):
        
        args=login_user_args.parse_args()
        username=args['username']
        password=args['password']
        # print("uuuuuuuuuuuuuuuuuuu",username,password)
        user=User.query.filter_by(username=username).first()
        # print("USERRRRRRRRRRRR:",user.password,password)
    
        if not user :
            return make_response(jsonify({'message ':'Could not verify, Login is required'}), 401)
        if check_password_hash(user.password, password):
            token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            # print("STOOORED",user.password,"   ", password)
            return make_response(jsonify({'token' : token}))
            # return make_response(jsonify({'message':'Succesful login'}))


        else :
             return make_response(jsonify({'message ':'Could not verify, Login is required' }), 401)
        
# class Logout(Resource): 
#     def post (self):


<<<<<<< HEAD
  
=======
<<<<<<< HEAD
  
=======
      
>>>>>>> 42be485 (sixth commit)
>>>>>>> 6718e8b (sixth commit)


# # For GET request to http://localhost:5000/
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

class GetOneUser(Resource):
    def get(self,id):
        # user=User.query.filter_by(id==id).first()
        user = User.query.get(id)
        
        if not user :
            return jsonify({'message':'User not found'})
        
        user_data = {'id': user.id, 'firstname':user.firstname, 'lastname': user.lastname, 'gender': user.gender,
                        'phonenumber': user.phonenumber,'date': user.date,
                        'username': user.username,
                        'email': user.email,
                        'password': user.password
                        }
        return jsonify({'User':user_data})


# # For put request to http://localhost:5000/update/?
class UpdateUser(Resource):
        def put (self, id):
            user=User.query.get(id)
            if user is None:
                return {'error':'User not found'}, 404
            else :
                args=register_user_args.parse_args()
                print(user.f)
                user.firstname=args['firstname'],
                # print("//////////////////////////Update user/////////////////////",user.firstname,args['firstname'])
                user.lastname=args['lastname'],
                user.phonenumber=args['phonenumber'],
                user.gender=args['gender'],
                user.date=args['date'],
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======

>>>>>>> 42be485 (sixth commit)
>>>>>>> 6718e8b (sixth commit)
                user.username=args['username'],
                user.email=args['email'],
                user.password=args['password']
              

                db.session.commit()
                return 'Updated',200
    
    
# # # # For delete request to http://localhost:5000/delete/?
class DeleteUser(Resource):
    def delete (self, id):
        #  user=User.query.filter_by(id==id).first()
        user = User.query.get(id)
        print ("THis is idddddddddddddddddd", id)
        if user is None:
            return {'error': 'not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return f'{id} is deleted', 200

api.add_resource(GetUser, '/')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
# api.add_resource(Logout, '/logout')

api.add_resource(GetOneUser, '/get/<int:id>')
api.add_resource(UpdateUser, '/update/<int:id>')
api.add_resource(DeleteUser,'/delete/<int:id>')
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
## helllllllllllllooooooooooooooooooooooooooooo
>>>>>>> 42be485 (sixth commit)
>>>>>>> 6718e8b (sixth commit)


if __name__ == '__main__':
    app.run(debug=True)
