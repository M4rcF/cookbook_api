import hmac
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from redis_config import jwt_redis_blocklist, ACCESS_EXPIRES
from flask_restful import Resource, reqparse
from models.user import User

def signup_permitted_params():
  signup_args = reqparse.RequestParser()
  signup_args.add_argument('email', type=str, required=True, help="The field 'email' not can be blank")
  signup_args.add_argument('name', type=str, required=True, help="The field 'name' not can be blank")
  signup_args.add_argument('password', type=str, required=True, help="The field 'password' not can be blank")
  
  return signup_args.parse_args()

def login_permitted_params():
  login_args = reqparse.RequestParser()
  login_args.add_argument('email', type=str, required=True, help="The field 'email' not can be blank")
  login_args.add_argument('password', type=str, required=True, help="The field 'password' not can be blank")
  
  return login_args.parse_args()

class SignUpController(Resource):
  def post(self):
    data = signup_permitted_params()

    user = User(data['name'], data['email'], data['password'])
    user.save()

    return { 'message': 'User created' }, 201
  
class LoginController(Resource):
  def post(self):
    data = login_permitted_params()
    user = User.find_by_email(data['email'])

    if user and hmac.compare_digest(user.password, data['password']):
      token = create_access_token(identity=user.email)
      return { 'token': token, 'user': user.to_json() }, 201
    
    return { 'message': 'email or password incorrect' }, 401
  
class LogoutController(Resource):
  @jwt_required()
  def post(self):
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    return { 'message': 'Logged out successfully' }, 200