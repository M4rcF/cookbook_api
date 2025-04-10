import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models.recipe import Recipe
from models.user import User

def get_current_user():
  try:
    current_user_email = get_jwt_identity()
    if current_user_email:
      return User.find_by_email(current_user_email)
  except Exception:
    return None

def recipes_permitted_params():
  recipes_args = reqparse.RequestParser()
  recipes_args.add_argument('name', type=str, required=True, help="The field 'name' cannot be blank")
  recipes_args.add_argument('origin', type=str, required=False, help="The field 'origin' is optional")
  recipes_args.add_argument('category', type=str, required=False, help="The field 'category' is optional")
  recipes_args.add_argument('image_url', type=str, required=False, help="The field 'image_url' is optional")
  recipes_args.add_argument('instructions', type=str, required=True, help="The field 'instructions' cannot be blank")
  recipes_args.add_argument('ingredients', type=str, action="append", required=True, help="The field 'ingredients' cannot be blank")
  recipes_args.add_argument('public', type=bool, required=False, default=True, help="The field 'public' is optional")
  return recipes_args.parse_args()

def format_date(date_str):
  if date_str:
    return datetime.strptime(date_str, '%Y-%m-%d').date()
  return None

class RecipesController(Resource):
  @jwt_required()
  def get(self, recipe_id=None):
    current_user = get_current_user()

    if not current_user:
      return {"message": "Unauthorized"}, 401

    if recipe_id is None:
      recipes = Recipe.get_all_public()
      return { 'recipes': [recipe.to_json() for recipe in recipes] }, 200
    
    recipe = Recipe.find_by_id(recipe_id)
    if recipe and (recipe.public or recipe.user_id == current_user.id):
      return recipe.to_json(), 200
  
    return { 'message': 'Recipe not found' }, 400

  @jwt_required()
  def post(self):
    current_user = get_current_user()
    data = recipes_permitted_params()

    if not current_user:
      return {"message": "Unauthorized"}, 401

    try:
      ingredients_json = json.dumps(data['ingredients'])
      recipe = Recipe(
        name=data['name'],
        origin=data.get('origin'),
        category=data.get('category'),
        image_url=data.get('image_url'),
        instructions=data['instructions'],
        ingredients=ingredients_json,
        public=data['public'],
        user_id=current_user.id
      )
      recipe.save()

      return { 'message': 'Recipe created' }, 201
    except Exception as e:
      return { 'message': f'An error occurred trying to create recipe: {str(e)}' }, 500

  @jwt_required()
  def put(self, recipe_id):
    current_user = get_current_user()
    data = recipes_permitted_params()

    if not current_user:
      return {"message": "Unauthorized"}, 401

    try:
      recipe = Recipe.find_by_id(recipe_id)
      if not recipe:
        return { 'message': 'Recipe not found' }, 400

      if recipe.user_id == current_user.id:
        recipe.name = data['name']
        recipe.origin = data.get('origin')
        recipe.category = data.get('category')
        recipe.image_url = data.get('image_url')
        recipe.instructions = data['instructions']
        recipe.ingredients = json.dumps(data['ingredients'])
        recipe.public = data['public']
        recipe.save()

        return { "message": "Recipe updated" }, 200
      
      return {"message": "Access denied."}, 403
    except Exception as e:
      return { 'message': f'An error occurred trying to update recipe: {str(e)}' }, 500

  @jwt_required()
  def delete(self, recipe_id):
    current_user = get_current_user()

    if not current_user:
      return {"message": "Unauthorized"}, 401

    try:
      recipe = Recipe.find_by_id(recipe_id)
      if not recipe:
        return { 'message': 'Recipe not found' }, 400

      if recipe.user_id == current_user.id:
        recipe.delete()
        return { 'message': 'Recipe deleted' }, 200

      return {"message": "Access denied."}, 403
    except Exception as e:
      return { 'message': f'An error occurred trying to delete recipe: {str(e)}' }, 500


class UserRecipesController(Resource):
  @jwt_required()
  def get(self):
    current_user = get_current_user()
    if not current_user:
      return {"message": "Unauthorized"}, 401
    
    recipes = Recipe.get_all_by_user(current_user.id)
    if recipes:
      return { 'recipes': [recipe.to_json() for recipe in recipes] }, 200
  
    return { 'message': 'Recipes not found' }, 400
