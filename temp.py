from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token,unset_jwt_cookies, jwt_required, get_jwt_identity
import sqlite3
import bcrypt

app = Flask(__name__)
api = Api(app)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'CU7bY6DeI9lUEjDlXyWsfYPsj8XtNtVt6Dt21l4uOjQo9sfeYwkcllJtvlDG1Ep'
jwt = JWTManager(app)

# Initialize SQLite database
conn = sqlite3.connect('secure_api.db')
cursor = conn.cursor()

# Create a user table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

class UserResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(args['password'].encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('secure_api.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (args['username'], hashed_password))
            conn.commit()
            conn.close()
            return {'message': 'User registered successfully'}, 201
        except sqlite3.IntegrityError:
            conn.close()
            return {'message': 'Username already exists'}, 400

class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        conn = sqlite3.connect('secure_api.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (args['username'],))
        user = cursor.fetchone()
        conn.close()
        # print((args['password']))
        if user and bcrypt.checkpw(args['password'].encode('utf-8'), user[2]):
            access_token = create_access_token(identity=args['username'])
            return {'access_token': f"{access_token}"}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

class TaskResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello, {current_user}! You can access this protected route.'}
class LogoutResource(Resource):
    @jwt_required()
    # def post(self):
    #     @api.route("/logout", methods=["POST"])
    def post(self):
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response
class GetRequest(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('username', type=str, required=True)
        parser.add_argument('Authorization', type=str, required=True)
        args = parser.parse_args()

        # conn = sqlite3.connect('secure_api.db')
        # cursor = conn.cursor()

        # # cursor.execute('SELECT * FROM users WHERE username = ?', (args['username'],))
        # # user = cursor.fetchone()
        # conn.close()
        # print((args['password']))
        # if user and bcrypt.checkpw(args['password'].encode('utf-8'), user[2]):
        access_token = args['Authorization']
        if access_token!="":
            return f"curl -X GET -H 'Authorization: Bearer {access_token}' http://127.0.0.1:5000/secure", 200
        else:
            return {'message': 'Invalid credentials'}, 401
api.add_resource(UserResource, '/register')
api.add_resource(AuthResource, '/login')
api.add_resource(TaskResource, '/secure')
api.add_resource(LogoutResource,"/logout")
api.add_resource(GetRequest,"/curl_it")
if __name__ == '__main__':
    app.run(debug=True)
