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
  user_args.add_argument('email', type=str, required=True, help="The field 'email' not can be blank")

  return user_args.parse_args()

class UsersController(Resource):
  @jwt_required()
  def get(self):
    current_user = get_current_user()

    if current_user and current_user.is_admin:
      users = User.get_all()
      return { 'users': [user.to_json() for user in users] }, 200

    return {'message': 'Unauthorized'}, 401
  
  @jwt_required()
  def put(self, user_id):
    try:
      user = User.find_by_id(user_id)
      current_user = get_current_user()
      updated_user_args = user_permitted_params()

      if current_user and current_user.id == user_id:
        user.update(**updated_user_args)
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

        return { "message": "User updated" }, 200

      return {"message": "Access denied. Only administrators can access."}, 403
    except Exception as e:
      return { 'message': f'An error ocurred trying to update user: {str(e)}' }, 500