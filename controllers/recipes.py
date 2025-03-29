import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models.recipe import Recipe   # Presumindo que o model Recipe esteja definido em models/recipe.py
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
  recipes_args.add_argument('ingredients', type=dict, action="append", required=True, help="The field 'ingredients' cannot be blank")
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
    if recipe_id is None and current_user:
      recipes = Recipe.get_all_public()

      return { 'recipes': [recipe.to_json() for recipe in recipes] }, 200
    
    recipe = Recipe.find_by_id(recipe_id)
    if recipe and recipe.public and current_user:
      return recipe.to_json(), 200
    
    return { 'message': 'Recipe not found' }, 400

  @jwt_required()
  def post(self):
    """
    Cadastrar uma nova receita.
    
    Exemplo de JSON enviado:
    {
      "name": "Bolo de Cenoura",
      "origin": "Brasil",
      "category": "Doce",
      "image_url": "https://receitatodahora.com.br/wp-content/uploads/2017/05/bolo-de-cenoura-perfeito.jpg",
      "instructions": "Misture os ingredientes e asse por 40 minutos...",
      "ingredients": [
        { "text": "cenouras", "measure": "3" },
        { "text": "xícaras de farinha", "measure": "2" }
      ]
    }
    """
    current_user = get_current_user()
    data = recipes_permitted_params()

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
    except Exception as e:
      return { 'message': f'An error occurred trying to create recipe: {str(e)}' }, 500
    
    return recipe.to_json(), 201

  @jwt_required()
  def put(self, recipe_id):
    current_user = get_current_user()
    data = recipes_permitted_params()

    try:
      recipe = Recipe.find_by_id(recipe_id)
      if not recipe:
        return { 'message': 'Recipe not found' }, 400

      if current_user and recipe.user_id == current_user.id:
        # Atualiza os dados da receita
        recipe.name = data['name']
        recipe.origin = data.get('origin')
        recipe.category = data.get('category')
        recipe.image_url = data.get('image_url')
        recipe.instructions = data['instructions']
        # Atualiza os ingredientes convertendo para JSON
        recipe.ingredients = json.dumps(data['ingredients'])
        recipe.save()
        return { "message": "Recipe updated" }, 200

      return { 'message': 'Access denied' }, 403

    except Exception as e:
      return { 'message': f'An error occurred trying to update recipe: {str(e)}' }, 500

  @jwt_required()
  def delete(self, recipe_id):
    current_user = get_current_user()

    try:
      recipe = Recipe.find_by_id(recipe_id)
      if recipe and recipe.user_id == current_user.id:
        recipe.delete()
        return { 'message': 'Recipe deleted' }, 200
      
      return { 'message': 'Recipe not found or access denied' }, 400
    except Exception as e:
      return { 'message': f'An error occurred trying to delete recipe: {str(e)}' }, 500
