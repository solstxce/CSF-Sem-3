from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Create a SQLite database
db_engine = create_engine('sqlite:///secure_api.db')
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(80))

# Create tables in the database
Base.metadata.create_all(db_engine)

# Sample user data (replace with secure password hashing in production)
users_data = [
    {'username': 'solstxce', 'password': 'solsa'},
    {'username': 'chahaein', 'password': 'password2'},
]

# Insert sample users into the database
Session = sessionmaker(bind=db_engine)
session = Session()
for user in users_data:
    new_user = User(username=user['username'], password=user['password'])
    session.add(new_user)
    session.commit()
session.close()

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = '0b87ff791d47d72b2b680e1c4bb6905dedc6d5ae'

# JWT configuration
def authenticate(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return session.query(User).filter_by(id=user_id).first()

jwt = JWT(app, authenticate, identity)

# Sample task data
tasks = []

class TaskResource(Resource):
    @jwt_required()
    def get(self):
        return {'tasks': tasks}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('task', type=str, required=True)
        args = parser.parse_args()
        tasks.append(args['task'])
        return {'message': 'Task added successfully'}

api.add_resource(TaskResource, '/tasks')

if __name__ == '__main__':
    app.run(debug=True)
