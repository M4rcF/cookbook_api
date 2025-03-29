from sql_alchemy import database
from datetime import datetime

class Review(database.Model):
  __tablename__ = 'reviews'  # Nome da tabela em inglês

  id = database.Column(database.Integer, primary_key=True)
  rating = database.Column(database.Integer, nullable=False)
  comment = database.Column(database.Text, nullable=True)
  created_at = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = database.Column(database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
  
  # Chave estrangeira que referencia a receita avaliada
  recipe_id = database.Column(database.Integer, database.ForeignKey('recipes.id'), nullable=False)
  # Chave estrangeira que referencia o usuário que fez a avaliação
  user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)

  def __init__(self, rating, comment, recipe_id, user_id):
    self.rating = rating
    self.comment = comment
    self.recipe_id = recipe_id
    self.user_id = user_id

  def save(self):
    database.session.add(self)
    database.session.commit()