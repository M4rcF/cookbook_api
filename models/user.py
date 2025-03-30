from sql_alchemy import database

class User(database.Model):
  __tablename__ = 'users'

  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String(50), unique=True, nullable=False)
  email = database.Column(database.String(20), unique=True, nullable=False)
  password = database.Column(database.String(10), nullable=False)

  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password
  
  def to_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email
    }
  
  def update(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password

    database.session.add(self)
    database.session.commit()

  @classmethod
  def find_by_id(cls, user_id):
    user = cls.query.filter_by(id = user_id).first()
    if user:
      return user
    
    return None

  @classmethod
  def find_by_email(cls, user_email):
    user = cls.query.filter_by(email = user_email).first()
    if user:
      return user
    
    return None

  @classmethod
  def get_all(cls):
    return cls.query.all()
  
  def save(self):
    database.session.add(self)
    database.session.commit()

  def delete(self):
    database.session.delete(self)
    database.session.commit()