from flask import request, render_template, redirect, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from project import app, db
from project.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/clients')
def clients():
    clients_list = User.query.all()
    return render_template('clients.html', data=clients_list)


@app.route('/login', methods=['POST', 'GET'])
def auth():
    user_name = request.form.get('user_user_name')

    if user_name:
        user = User.query.filter_by(user_user_name=user_name).first()
        if check_password_hash(user.user_user_name, user_name):
            login_user(user)
            # next_page = request.args.get('next')
            render_template('profile.html')
        else:
            flash('Такого имени не найдено')
    else:
        # flash('Неверное имя')
        return render_template('login.html')




@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        user_name = request.form['name']

        user = User(user_name=user_name)

        try:
            db.session.add(user)
            db.session.commit()
            return render_template('okey_reg.html')
        except Exception as e:
            return render_template('sorry.html')
    else:
        return render_template('registration.html')




@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')