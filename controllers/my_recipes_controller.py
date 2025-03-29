from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.recipe import Recipe
from models.user import User

def get_current_user():
  try:
    current_user_email = get_jwt_identity()
    if current_user_email:
      return User.find_by_email(current_user_email)
  except Exception:
    return None

class MyRecipesController(Resource):
  @jwt_required()
  def get(self):
    current_user = get_current_user()
    if not current_user:
      return {'message': 'Unauthorized'}, 401

    # Filtra somente as receitas criadas pelo usuário autenticado
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return {'recipes': [recipe.to_json() for recipe in recipes]}, 200
