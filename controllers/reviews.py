from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.review import Review  # Presume que o model Review está definido
from models.user import User

def get_current_user():
  """
  Retorna o usuário autenticado com base no token JWT.
  """
  try:
    current_user_email = get_jwt_identity()
    if current_user_email:
      return User.find_by_email(current_user_email)
  except Exception:
    return None

def review_permitted_params():
  """
  Utiliza reqparse para capturar os parâmetros da requisição para review.
  """
  parser = reqparse.RequestParser()
  parser.add_argument('rating', type=int, required=True, help="Rating is required")
  parser.add_argument('comment', type=str, required=False, help="Comment is optional")
  parser.add_argument('recipe_id', type=int, required=True, help="Recipe ID is required")
  return parser.parse_args()

class ReviewsController(Resource):
  @jwt_required()
  def get(self, review_id=None):
    """
    Se review_id for fornecido, retorna a avaliação específica.
    Se não, retorna todas as avaliações do usuário autenticado.
    """
    current_user = get_current_user()
    if review_id:
      review = Review.find_by_id(review_id)
      if review:
          return review.to_json(), 200
      return {'message': 'Review not found'}, 404
    else:
      if current_user:
          reviews = Review.query.filter_by(user_id=current_user.id).all()
          return {'reviews': [review.to_json() for review in reviews]}, 200
      return {'message': 'Unauthorized'}, 401

  @jwt_required()
  def post(self):
    """
    Cria uma nova avaliação (review) para uma receita.
    
    Exemplo de JSON enviado:
    {
        "rating": 5,
        "comment": "Excellent recipe!",
        "recipe_id": 1
    }
    """
    current_user = get_current_user()
    data = review_permitted_params()

    try:
      review = Review(
          rating=data['rating'],
          comment=data.get('comment'),
          recipe_id=data['recipe_id'],
          user_id=current_user.id
      )
      review.save()
      return review.to_json(), 201
    except Exception as e:
      return {'message': f'An error occurred while creating review: {str(e)}'}, 500

  @jwt_required()
  def put(self, review_id):
    """
    Atualiza uma avaliação existente.
    Apenas o autor da avaliação (ou um admin) pode realizar a atualização.
    
    Exemplo de JSON enviado:
    {
        "rating": 4,
        "comment": "Good, but could be improved",
        "recipe_id": 1
    }
    """
    current_user = get_current_user()
    data = review_permitted_params()

    try:
      review = Review.find_by_id(review_id)
      if not review:
        return {'message': 'Review not found'}, 404

      if review.user_id != current_user.id and not current_user.is_admin:
        return {'message': 'Access denied'}, 403

      review.rating = data['rating']
      review.comment = data.get('comment')
      review.recipe_id = data['recipe_id']
      db.session.commit()
      return {'message': 'Review updated'}, 200
    except Exception as e:
      return {'message': f'An error occurred while updating review: {str(e)}'}, 500

  @jwt_required()
  def delete(self, review_id):
    """
    Deleta uma avaliação existente.
    Apenas o autor ou um admin pode realizar a exclusão.
    """
    current_user = get_current_user()

    try:
      review = Review.find_by_id(review_id)
      if not review:
        return {'message': 'Review not found'}, 404

      if review.user_id != current_user.id and not current_user.is_admin:
        return {'message': 'Access denied'}, 403

      db.session.delete(review)
      db.session.commit()
      return {'message': 'Review deleted'}, 200
    except Exception as e:
      return {'message': f'An error occurred while deleting review: {str(e)}'}, 500
