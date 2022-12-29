from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///syte.db'
db = SQLAlchemy(app)

app.secret_key = 'd892e4c96c8ce23d201d602462020a'      # session key

from routes import *
from models import User



with app.app_context():
   db.create_all()

if __name__ == '__main__':
   #with app.app_context():
      #admin = User(username = "admin" , email = "admin@gmail.ru" , password = "master_key", is_admin = "True")
      #db.session.add(admin)
      #db.session.commit()
   app.run()

#начало 
#создание аккаунта администратора

#admin_username ="admin"
#admin_mail = "admin@gmail.com"
#admin_password = "strong_password"

#admin = User(username=admin_username,    
        #email=admin_mail,
        #password=admin_password)
#db.session.add(admin)
#db.session.commit()
#конец