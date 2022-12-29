from app import app, db
from flask import render_template, request, redirect, url_for, session
from models import User, Product, Comment
from validate import email_cheak, login_cheak, password_cheak
import os





@app.route('/register', methods=['GET', 'POST'])
def register():
   result = 'Пользователь не создан'
   if request.method == 'POST':
       username = request.form.get('username')
       email = request.form.get('email')
       password = request.form.get('password')
       confirm_password = request.form.get('confirm_password')

       if not login_cheak(username):
           result = 'Некорректный логин'
       elif not email_cheak(email):
           result = 'Некорректный email'
       elif not password_cheak(password):
           result = 'Некорректный пароль'
       elif password != confirm_password:
           result = 'Пароли не совпадают'
       else:
           user = User(
               username=username,
               email=email,
               password=password,
               is_admin = 'False')
           user_test = User.query.filter_by(username=user.username).first()
           if user_test is None:
               db.session.add(user)
               db.session.commit()
               result = 'Пользователь создан'
           else:
               result = 'Такой логин занят'
   return render_template('/register.html', result=result)






@app.route('/login', methods=['GET', 'POST'])
def login():
   result = 'Введите логин и пароль'
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       user_test = User.query.filter_by(username=username).first()
       if user_test is None:
           result = 'Пользователь не существует'
       elif user_test.password != password:
           result = 'Неверный пароль'
       else:
           result = 'Пользователь вошел'
           if 'user_status' in session:                           #### start
                if (user_test.is_admin == "False"):
                    session['user_status'] = 'authorized'   
                    session['username'] = username
                    print(session['user_status'])                 
                    session.modified = True
                elif (user_test.is_admin == "True"):
                    session['user_status'] = 'admin' 
                    session['username'] = username  
                    print(session['user_status'])                 
                    session.modified = True                       #### end
   if result == 'Пользователь вошел':
       return redirect(url_for('confirm'))
   return render_template('/login.html', result=result)





@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
   return render_template('/confirm.html')





@app.route('/add_product',methods=['GET', 'POST'])
def add_product():
    if(session['user_status'] == 'admin'):
        if request.method == 'POST' :
            p_type = request.form.get("product_type")
            p_name = request.form.get("product_name")
            p_description = request.form.get("description")
            p_industry = request.form.get("industry")
            p_price = request.form.get("price")
            f = request.files["file"]
            print(f.filename)
            product = Product(p_type = p_type,p_name = p_name,p_description = p_description,p_industry = p_industry,p_price = p_price,p_filename = f.filename, middle_count = 0)
            #product_test = Product.query.filter_by(p_name=Product.p_name).first()
            #if product_test is None:
            f.save("static/" + f.filename)            #Tab
            db.session.add(product)                 #Tab
            db.session.commit()                     #Tab
    else: 
        return redirect(url_for('login'))
    return render_template('/add_product.html')




@app.route('/',methods=['GET', 'POST'])
def base():
    if not('user_status' in session): 
        session['user_status'] = 'unauthorized'
        session['username'] =  'unauthorized'
        session.modified = True #показываем фласку, что внесли изменения в сессиию
    return render_template('/base.html',user_status = session['user_status'])


@app.route('/cards',methods=['GET', 'POST'])
def Cards_list():
    if session['user_status'] == "admin":
        admin = True
    else:
        admin = False
    with app.app_context():
        res = db.engine.execute('SELECT * FROM product')
    if request.method == 'POST':
        req = request.form.get('filter')
        filtr, msg = req.split('/')
        msg = msg.lower()
        if filtr == "no_filter":
            pass
        elif filtr == 'p_price':
            with app.app_context():
                res = db.engine.execute(f'SELECT * FROM product order by {filtr}')
                return (render_template("cards.html", trashs=res, msg=msg,admin = admin))

        else:
            try:
                with app.app_context():
                    res = db.engine.execute(f'SELECT * FROM product order by {filtr}')
                    return(render_template("cards.html", trashs=res, msg=msg,admin = admin))
            except Exception: pass

    with app.app_context():
        res = db.engine.execute('SELECT * FROM product')
    return render_template("cards.html", trashs=res,admin = admin)


@app.route('/cards/<int:id>',methods=['GET', 'POST'])
def Products(id):
    mark_sum = 0
    with app.app_context():
        res = db.engine.execute(f'SELECT * FROM product WHERE id = {id}')
        for i in res:
            l = {}
            p = 0
            for a in i:
                l[p] = a
                p+=1
    if(session['user_status'] == 'authorized' or session['user_status'] == 'admin'):
        if request.method == 'POST' :
            product = id
            text = request.form.get("comment")
            mark = request.form.get("mark")
            db.session.add(Comment(product = product, text = text,username = session['username'],mark = mark))                 
            db.session.commit()                    
    else: 
        return redirect(url_for('login'))
    users_count = db.session.execute(f'SELECT COUNT(*) as count FROM comment WHERE product = {id}')       ####
    mark_count = db.engine.execute(f'SELECT * FROM comment WHERE product = {id}')
    for i in users_count:
        l_s = {}
        p = 0
        for a in i:
            l_s[p] = a
            p+=1

    for i in mark_count:
        l_c = {}
        p = 0
        for a in i:
            l_c[p] = a
            p+=1
        mark_sum += int(l_c[4])
    if(l_s[0] != 0):
        sr = mark_sum / l_s[0]
        sr = round(sr,2)
        print(sr)
        db.session.execute(f'UPDATE product SET middle_count = "{sr}" WHERE id = {id}')
        db.session.commit()
    res = db.engine.execute(f'SELECT * FROM comment WHERE product = {id}')
    return render_template('product.html', p_id = id,p_name = l[2],p_description = l[3],p_industry = l[4],p_price = l[5],p_filename = l[6],trashs = res)




@app.route('/cards/Edit/<int:id>',methods=['GET', 'POST'])
def Edit(id):
    res_f = db.engine.execute(f'SELECT * FROM product WHERE id = {id}')
    for i in res_f:
        l_f = {}
        p = 0
        for a in i:
            l_f[p] = a
            p+=1
    if(session['user_status'] == 'admin'):
        if request.method == 'POST' :
            p_type = request.form.get("product_type")
            p_name = request.form.get("product_name")
            p_description = request.form.get("description")
            p_industry = request.form.get("industry")
            p_price = request.form.get("price")
            f = request.files["file"]
            if p_type != "": 
                db.session.execute(f'UPDATE product SET p_type = "{p_type}" WHERE id = {id}')
                db.session.commit()
            if p_name != "": 
                db.session.execute(f'UPDATE product SET p_name = "{p_name}" WHERE id = {id}')
                db.session.commit()
            if p_description != "": 
                db.session.execute(f'UPDATE product SET p_description = "{p_description}" WHERE id = {id}')
                db.session.commit()
            if p_industry != "":
                 db.session.execute(f'UPDATE product SET p_industry = "{p_industry}" WHERE id = {id}')
                 db.session.commit()
            if p_price != "":
                 db.session.execute(f'UPDATE product SET p_price = "{p_price}" WHERE id = {id}')
                 db.session.commit()
            if f.filename != "": 
                db.session.execute(f'UPDATE product SET p_filename = "{f.filename}" WHERE id = {id}')
                db.session.commit()
                os.remove("static/" + l_f[6])
                f.save("static/" + f.filename)
            
            #print(f.filename)
            #product = Product(p_type = p_type,p_name = p_name,p_description = p_description,p_industry = p_industry,p_price = p_price,p_filename = f.filename)
            #f.save("png/" + f.filename)             #Tab
            #db.session.add(product)                 #Tab
            #db.session.commit()                     #Tab
    else: 
        return redirect(url_for('login'))
    res = db.engine.execute(f'SELECT * FROM product WHERE id = {id}')
    for i in res:
        l = {}
        p = 0
        for a in i:
            l[p] = a
            p+=1
    return render_template('edit.html', p_id = l[0],p_type = l[1], p_name = l[2],p_description = l[3], p_industry = l[4],p_price =l[5] )

@app.route('/cards/delete/<int:id>',methods=['GET', 'POST'])
def delete(id):
    res = db.engine.execute(f'SELECT * FROM product WHERE id = {id}')
    for i in res:
        l = {}
        p = 0
        for a in i:
            l[p] = a
            p+=1
    os.remove("static/" + l[6])
    db.engine.execute(f'DELETE FROM product WHERE id = {id}')
    db.engine.execute(f'DELETE FROM comment WHERE product = {id}')
    db.session.commit()
    return redirect(url_for('Cards_list'))