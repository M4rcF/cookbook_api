from sql_alchemy import database
from datetime import datetime

class Review(database.Model):
  __tablename__ = 'reviews'

  id = database.Column(database.Integer, primary_key=True)
  comment = database.Column(database.Text, nullable=True)
  rating = database.Column(database.Integer, nullable=False)
  recipe_id = database.Column(database.Integer, database.ForeignKey('recipes.id'), nullable=False)
  user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=False)
  created_at = database.Column(database.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = database.Column(database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

  recipe = database.relationship('Recipe', backref='recipe_reviews')
  user = database.relationship('User', backref='user_reviews')

  def __init__(self, comment, rating, recipe_id, user_id):
    self.comment = comment
    self.rating = rating
    self.recipe_id = recipe_id
    self.user_id = user_id

  def to_json(self):
    return {
      'id': self.id,
      'comment': self.comment,
      'rating': self.rating,
      'recipe_id': self.recipe_id,
      'user_id': self.user_id,
      'created_at': self.created_at.strftime("%d/%m/%Y %H:%M:%S") if self.created_at else None,
      'updated_at': self.updated_at.strftime("%d/%m/%Y %H:%M:%S") if self.updated_at else None
    }
  
  def save(self):
    database.session.add(self)
    database.session.commit()

  def delete(self):
    database.session.delete(self)
    database.session.commit()

  @classmethod
  def get_all(cls):
    return cls.query.all()
  
  @classmethod
  def find_by_id(cls, review_id):
    return cls.query.filter_by(id=review_id).first()
  
  @classmethod
  def find_by_recipe_id(cls, recipe_id):
    return cls.query.filter_by(recipe_id=recipe_id).all()
  
    
  @classmethod
  def find_by_user_review(cls, current_user_id, recipe_id):
    return cls.query.filter_by(recipe_id=recipe_id, user_id=current_user_id).all()
  
  
