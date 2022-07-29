from flask import Flask, request, render_template, flash, redirect, url_for, session, abort
from markupsafe import escape
from werkzeug.utils import redirect
from admin.admin import admin


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'slkeflkjslk939kjldwks33kd'

app.register_blueprint(admin, url_prefix='/admin')

# lib_list = ['01.png', '01.png', '01.png', '01.png', '01.png', '01.png', '01.png']

@app.route('/')
def home_page():
    return render_template('index.html', title='ГЛАВНАЯ | БИБЛИОТЕКА')

@app.route('/my_lib')
def gallery():
    return render_template('my_lib.html', lib_list=lib_list)

@app.route('/read-full')
def read_full():
    return render_template('book.html')

@app.route('/comment', methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        flash('Сообщение отправлено', category='success')
    return render_template('comment.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Страница не найдена")

@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя: {username}"

@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    # elif request.form['name'] == 'POST' and "admin" and request.form['password'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title="Авторизация")

@app.route('/load_book', methods=["POST", "GET"])
def load_book():
    if request.method == 'POST':
        flash('Книга загружена', category='success')
    return render_template('load_book.html')

@app.route('/base')
def base():
    return render_template('base.html')


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)