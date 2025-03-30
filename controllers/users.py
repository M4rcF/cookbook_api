import hmac
from flask_restful import Resource, reqparse
from models.user import User
from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from redis_config import jwt_redis_blocklist, ACCESS_EXPIRES

def get_current_user():
  try:
    current_user_email = get_jwt_identity()
    if current_user_email:
      return User.find_by_email(current_user_email)
  except Exception:
    return None
  
def user_permitted_params():
  user_args = reqparse.RequestParser()
  user_args.add_argument('name', type=str, required=True, help="The field 'name' not can be blank")
  user_args.add_argument('email', type=str, required=True, help="The field 'email' not can be blank")
  user_args.add_argument('password', type=str, required=False, help="The field 'password' not can be blank")

  return user_args.parse_args()

class UsersController(Resource):  
  @jwt_required()
  def put(self, user_id):
    current_user = get_current_user()

    if not current_user:
      return {"message": "Unauthorized"}, 401

    try:
      user = User.find_by_id(user_id)
      updated_user_args = user_permitted_params()

      if current_user.id == user_id:
        user.update(**updated_user_args)
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

        return { "message": "User updated" }, 200

      return {"message": "Access denied."}, 403
    except Exception as e:
      return { 'message': f'An error ocurred trying to update user: {str(e)}' }, 500