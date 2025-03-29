from sql_alchemy import database

class User(database.Model):
  __tablename__ = 'users'

  id = database.Column(database.Integer, primary_key=True)
  email = database.Column(database.String(20), unique=True, nullable=False)
  password = database.Column(database.String(10), nullable=False)

  def __init__(self, email, password):
    self.email = email
    self.password = password
  
  def to_json(self):
    return {
      'id': self.id,
      'email': self.email
    }
  
  def update(self, email, is_admin, name, cpf, cellphone):
    self.email = email

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
    print('teste1', user_email)
    user = cls.query.filter_by(email = user_email).first()
    print('teste2', user)
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