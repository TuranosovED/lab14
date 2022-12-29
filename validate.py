import re

#проверка пароля и шифрование
def email_cheak(mail):
   if mail.count('@') == 1:
       return True
   return False


def login_cheak(login):
   if len(login) >= 6:
       if login[0] in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
           regex = "^[a-zA-Z0-9_]+$"
           pattern = re.compile(regex)
           if pattern.search(login) is not None:
               return True
   return False


def password_cheak(password):
   cheak1 = False
   cheak2 = False
   cheak3 = False
   cheak4 = False
   if len(password) >= 8:
       for i in password:
           if i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
               cheak1 = True
           if i in 'abcdefghijklmnopqrstuvwxyz':
               cheak2 = True
           if i in '0123456789':
               cheak3 = True
           if i in '_-+*.!%$#@&*^|\/~[]{}':
               cheak4 = True                                                            
       if cheak1 and cheak2 and cheak3 and cheak4:
           return True
   return False

