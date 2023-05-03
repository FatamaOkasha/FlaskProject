# from flask import Flask, jsonify, request, session
# from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_cors import CORS #pip install -U flask-cors
# from datetime import timedelta
 
# app = Flask(__name__)
 
# app.config['SECRET_KEY'] = 'cairocoders-ednalan'
 
# app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
# CORS(app)
  
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'testingdb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app) 
 
# @app.route('/')
# def home():
#     passhash = generate_password_hash('cairocoders')
#     print(passhash)
#     if 'username' in session:
#         username = session['username']
#         return jsonify({'message' : 'You are already logged in', 'username' : username})
#     else:
#         resp = jsonify({'message' : 'Unauthorized'})
#         resp.status_code = 401
#         return resp
 
# @app.route('/login', methods=['POST'])
# def login():
#     _json = request.json
#     _username = _json['username']
#     _password = _json['password']
#     print(_password)
#     # validate the received values
#     if _username and _password:
#         #check user exists          
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         
#         sql = "SELECT * FROM user WHERE username=%s"
#         sql_where = (_username,)
         
#         cursor.execute(sql, sql_where)
#         row = cursor.fetchone()
#         username = row['username']
#         password = row['password']
#         if row:
#             if check_password_hash(password, _password):
#                 session['username'] = username
#                 cursor.close()
#                 return jsonify({'message' : 'You are logged in successfully'})
#             else:
#                 resp = jsonify({'message' : 'Bad Request - invalid password'})
#                 resp.status_code = 400
#                 return resp
#     else:
#         resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
#         resp.status_code = 400
#         return resp
         
# @app.route('/logout')
# def logout():
#     if 'username' in session:
#         session.pop('username', None)
#     return jsonify({'message' : 'You successfully logged out'})
         
# if __name__ == "__main__":
#     app.run()

from flask import Flask, jsonify, request,make_response
from flask_restful import Resource ,Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api=Api(app)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name=db.Column(db.String(30),nullable=False)
    last_name=db.Column(db.String(30),nullable=False)
    phone_number=db.Column(db.String(10),unique=True)
    gender=db.Column(db.String(8),nullable=False)
    date=db.Column(db.String(10),nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(16),nullable=False)
     
    def __repr__(self):
        return f"{self.first_name} - {self.last_name } - {self.gender } "
    
    #Get Request  to http://localhost::5000/
class GetUser(Resource):
        def get(self):
            users=User.query.all()
            user_list=[]
            for user in users:
                user_data={"Id":user.id ,
                           "FisrtName":user.first_name ,
                           "LastName":user.last_name ,
                           "PhoneNumber":user.phone_number ,
                           "Gender":user.gender ,
                           "Date":user.date ,
                           "UserName":user.username ,
                           "Email":user.email ,
                           "Password":user.password ,
                           }
                user_list.append(user_data)
            return {"Users" : user_list},200
 #Post Request  to http://localhost::5000/
class AddUser(Resource):
        def post (self):
            if request.is_json:
                    user=User(  
                                first_name=request.json['FisrtName'],
                                last_name=request.json['LastName'],
                                phone_number=request.json['PhoneNumber'],
                                gender=request.json['Gender'],
                                date=request.json['Date'],
                                username=request.json['UserName'],
                                email=request.json['Email'],
                                password=request.json['Password']
                    )
                    db.session.add(user)
                    db.session.commit()   
                    # return json response 
                    return  make_response(jsonify({"Id":user.id ,
                           "FisrtName":user.first_name ,
                           "LastName":user.last_name ,
                           "PhoneNumber":user.phone_number ,
                           "Gender":user.gender ,
                           "Date":user.date ,
                           "UserName":user.username ,
                           "Email":user.email ,
                           "Password":user.password }),201)
            else :
                return {'error':'Request must be JSON'} ,408
 #Put Request  to http://localhost::5000/
class UpdateUser(Resource):
        def put (self, id):
            if request.is_json:
                user=User.query.get(id)
                if user is None:
                    return {'error':'not found'}, 404
                else :
                        user.first_name=request.json['FisrtName'],
                        user.last_name=request.json['LastName'],
                        user.phone_number=request.json['PhoneNumber'],
                        user.gender=request.json['Gender'],
                        user.date=request.json['Date'],
                        user.username=request.json['UserName'],
                        user.email=request.json['Email'],
                        user.password=request.json['Password']
                        db.session.commit()
                        return 'Updated',200
            else :
                   return {'error':'Request must be JSON'}, 400
#Delete  Request  to http://localhost::5000/
class DeleteUser(Resource):
        def delete (self, id):
                user=User.query.get(id)
                if user is None:
                    return {'error':'not found'}, 404
                db.session.delete(user)
                db.session.commit()
                return f'{id} is deleted',200
api.add_resource(GetUser,'/')
api.add_resource(AddUser,'/add')
api.add_resource(UpdateUser,'/update/<int:id>')
api.add_resource(DeleteUser,'/delete/<int:id>')
     
                        

# @app.route("/")
# def hello():
#     return "Hello"

if __name__ == "__main__":
    app.run()

