from flask_restful import Api
from controllers.recipes import RecipesController
from controllers.my_recipes_controller import MyRecipesController
from controllers.reviews import ReviewsController
from controllers.users import UsersController
from controllers.authentication import SignUpController, LoginController, LogoutController

def register_routes(app):
    api = Api(app)

    api.add_resource(SignUpController, '/api/auth/sign_up')
    api.add_resource(LoginController, '/api/auth/login')
    api.add_resource(LogoutController, '/api/auth/logout')
    api.add_resource(UsersController, '/api/users')
    api.add_resource(RecipesController, '/api/recipes', '/api/recipes/<int:recipe_id>')
    api.add_resource(ReviewsController, '/api/reviews', '/api/reviews/<int:review_id>')
    api.add_resource(MyRecipesController, '/recipes/mine')