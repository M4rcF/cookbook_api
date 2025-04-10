import json
from sql_alchemy import database

class Recipe(database.Model):
  __tablename__ = 'recipes'

  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String(100), nullable=False)
  origin = database.Column(database.String(100), nullable=True)
  category = database.Column(database.String(100), nullable=True)
  image_url = database.Column(database.String(255), nullable=True)
  instructions = database.Column(database.Text, nullable=True)
  ingredients = database.Column(database.Text, nullable=True)
  public = database.Column(database.Boolean, default=False)
  user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

  reviews = database.relationship('Review', backref='reviews_recipe')

  def __init__(self, name, origin, category, image_url, instructions, ingredients, public, user_id):
    self.name = name
    self.origin = origin
    self.category = category
    self.image_url = image_url
    self.instructions = instructions
    self.ingredients = ingredients
    self.public = public
    self.user_id = user_id

  def to_json(self):
    try:
        ingredients_data = json.loads(self.ingredients) if self.ingredients else []
    except Exception as e:
        ingredients_data = []
    return {
      'id': self.id,
      'name': self.name,
      'origin': self.origin,
      'category': self.category,
      'image_url': self.image_url,
      'instructions': self.instructions,
      'ingredients': ingredients_data,
      'public': self.public,
      'user_id': self.user_id
    }

  def save(self):
    database.session.add(self)
    database.session.commit()

  def delete(self):
    database.session.delete(self)
    database.session.commit()

  @classmethod
  def find_by_id(cls, recipe_id):
    user = cls.query.filter_by(id = recipe_id).first()
    if user:
      return user
    
    return None
  
  @classmethod
  def get_all_by_user(cls, user_id):
    return cls.query.filter_by(user_id=user_id).all()
  
  @classmethod
  def get_all_public(cls):
    return cls.query.filter_by(public=True).all()
