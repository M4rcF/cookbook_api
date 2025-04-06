import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.review import Review  # Certifique-se de que o model Review está definido e importado corretamente
from models.user import User

def get_current_user():
  try:
    current_user_email = get_jwt_identity()
    if current_user_email:
      return User.find_by_email(current_user_email)
  except Exception:
    return None

def review_permitted_params():
  parser = reqparse.RequestParser()
  parser.add_argument('rating', type=int, required=True, help="Rating is required")
  parser.add_argument('comment', type=str, required=False, help="Comment is optional")
  parser.add_argument('recipe_id', type=int, required=True, help="Recipe ID is required")
  return parser.parse_args()

class ReviewController(Resource):
  @jwt_required()
  def get(self, recipe_id=None):
    """
    Se review_id for fornecido, retorna a review correspondente; 
    caso contrário, retorna todas as reviews do usuário autenticado.
    """
    current_user = get_current_user()
    if not current_user:
      return {"message": "Unauthorized"}, 401

    if recipe_id:
      review = Review.find_by_recipe_id(recipe_id)
      if review:
        return {"reviews": [review.to_json() for review in reviews]}, 200
      return {"message": "Review not found"}, 404
    else:
      reviews = Review.get_all()
      return {"reviews": [review.to_json() for review in reviews]}, 200

  @jwt_required()
  def post(self):
    """
    Cadastrar uma nova review.
    Exemplo de JSON:
    {
        "rating": 5,
        "comment": "Great recipe!",
        "recipe_id": 1
    }
    """
    current_user = get_current_user()
    if not current_user:
      return {"message": "Unauthorized"}, 401
    
    data = review_permitted_params()
    existing_review =  Review.find_by_user_review(current_user.id, data['recipe_id'])

    if existing_review:
      return { "message": "Review already exists" }, 404

    try:
      review = Review(
        rating=data['rating'],
        comment=data.get('comment'),
        recipe_id=data['recipe_id'],
        user_id=current_user.id
      )
      
      review.save()

      return { 'review': review.to_json(), 'message': 'Review Created' }, 201
    except Exception as e:
      return {"message": f"Error creating review: {str(e)}"}, 500

  @jwt_required()
  def put(self, review_id):
    """
    Atualiza uma review existente.
    Exemplo de JSON:
    {
        "rating": 4,
        "comment": "Updated comment",
        "recipe_id": 1
    }
    Apenas o dono da review ou um admin pode atualizar.
    """
    current_user = get_current_user()
    if not current_user:
      return {"message": "Unauthorized"}, 401

    data = review_permitted_params()
    review = Review.find_by_id(review_id)
    if not review:
      return {"message": "Review not found"}, 404

    if review.user_id != current_user.id:
      return {"message": "Access denied"}, 403

    review.rating = data['rating']
    review.comment = data.get('comment')
    review.recipe_id = data['recipe_id']
    review.save()

    return {"review": review.to_json(), "message": "Review updated"}, 200

  @jwt_required()
  def delete(self, review_id):
    """
    Deleta uma review existente.
    Apenas o dono ou um admin pode deletar.
    """
    current_user = get_current_user()
    if not current_user:
      return {"message": "Unauthorized"}, 401

    review = Review.find_by_id(review_id)
    if not review:
      return {"message": "Review not found"}, 404

    if review.user_id != current_user.id:
      return {"message": "Access denied"}, 403

    review.delete()
    return {"message": "Review deleted"}, 200
