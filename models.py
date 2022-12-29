from app import db


class User(db.Model):
   id = db.Column(db.Integer,  
                  primary_key=True, 
                  autoincrement=True, 
                  nullable=False, 
                  unique=True)
   username = db.Column(db.String(80), 
                        unique=True, 
                        nullable=False)
   email = db.Column(db.String(120), 
                     unique=True, 
                     nullable=False)
   password = db.Column(db.String(80),
                        unique=False, 
                        nullable=False)
   is_admin = db.Column(db.String(80),
                        unique=False, 
                        nullable=False)


class Product(db.Model):
   id = db.Column(db.Integer,  
                  primary_key=True, 
                  autoincrement=True, 
                  nullable=False, 
                  unique=True)
   p_type = db.Column(db.String(80), 
                        unique=False, 
                        nullable=False)
   p_name = db.Column(db.String(120), 
                     unique=True, 
                     nullable=False)
   p_description = db.Column(db.String(80),
                        unique=False, 
                        nullable=False)
   p_industry = db.Column(db.String(80),
                        unique=False, 
                        nullable=False)
   p_price = db.Column(db.String(80),
                        unique=False, 
                        nullable=False)
   p_filename = db.Column(db.String(80),
                        unique=True, 
                        nullable=False)
   middle_count = db.Column(db.String(80),
                        unique=False, 
                        nullable=False)

class Comment(db.Model):
   id = db.Column(db.Integer,  
                  primary_key=True, 
                  autoincrement=True, 
                  nullable=False, 
                  unique=True)
   product = db.Column(db.String(80), 
                        unique=False, 
                        nullable=False) 
   text = db.Column(db.String(80), 
                        unique=False, 
                        nullable=False)
   username = db.Column(db.String(80), 
                        unique=False, 
                        nullable=False)
   mark = db.Column(db.String(80), 
                        unique=False, 
                        nullable=False)