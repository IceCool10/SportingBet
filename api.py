import hashlib
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import g,Response,request
from flask.ext.mysql import MySQL
import json
import MySQLdb
import random

app = Flask(__name__)
api = Api(app)

@app.before_request
def db_connect():
  g.conn = MySQLdb.connect(host='localhost',
                              user='', #db_user
                              passwd='',#db_pass
                              db='Sporting')
  g.cursor = g.conn.cursor()

class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments

            ALPHABET    =   "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            chars       =   []


            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='Username to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userName = args['username']
            _userPassword = args['password']
            
            if _userName == "":
                return {'Error': "Username cannot be empty"}
            elif _userPassword == "":
                return {'Error': "Password cannot be empty"}
            
            for i in range(25):
                chars.append(random.choice(ALPHABET))
            
            password = hashlib.sha256(_userPassword + ("".join(chars))).hexdigest()

            sql = "INSERT INTO users (username, password, salt)\
                    VALUES ('%s', '%s', '%s')" % (_userName, password, "".join(chars)[::-1])
            g.cursor.execute(sql)
            g.conn.commit()
            resp = Response("User Created", mimetype='application/json')
            return resp
        except Exception as e:
            return {'error': str(e)}

class LoginUser(Resource):
    def post(self):
        try:
            parser  =   reqparse.RequestParser()
            parser.add_argument('username', type=str, help='Username')
            parser.add_argument('password', type=str, help='Password')
            
            args    =   parser.parse_args()
            
            username    =   args["username"]
            password    =   args["password"]

            sql     =   "SELECT password,salt FROM users where username = '%s' LIMIT 1" % (username)

            g.cursor.execute(sql)

            data    =   g.cursor.fetchone()

            if(str(hashlib.sha256(password + str(data[1][::-1])).hexdigest()) == str(data[0])):

                resp    =   Response("Login Successfully", mimetype='application/json')
                return resp
            else:
                resp    =   Response("Invalid Username Or Password", mimetype='application/json')
                return resp

        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/Register')
api.add_resource(LoginUser,  '/Login')

if __name__ == '__main__':
    app.run(debug=True)
    

