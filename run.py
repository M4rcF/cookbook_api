from app import create_app
from app.routes import register_routes
from flask_cors import CORS
from sql_alchemy import database

app = create_app()

with app.app_context():
  from models.user import User
  # Remove todas as tabelas
  # database.drop_all()
  database.create_all()

CORS(app)

register_routes(app)

if __name__ == '__main__':
  app.run(debug=True)
