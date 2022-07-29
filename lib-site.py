import sqlite3
import os
from flask import Flask, render_template, request, g, flash, make_response, redirect, url_for
from LDataBase import LDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm

DATABASE = '/tmp/libdb.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5sdoflk;jpoi;elk;s'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'libdb.db')))
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к вашей библиотеке'
login_manager.login_message_category = 'success'

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return  conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = LDataBase(db)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def index():
    return render_template('index.html', menu=dbase.getMenu())

@app.route('/load_book', methods=["POST", "GET"])
def load_book():
    if request.method == 'POST':
        res = dbase.load_book(request.form['book_title'], request.form['book_text'], request.form['url'])
        flash('Книга загружена', category='success')
    else:
        flash('Ошибка загрузки книги', category='error')
    return render_template('load_book.html', menu=dbase.getMenu(), title='Добавление книги')

@app.route('/book/<alias>')
@login_required
def show_book(alias):
    title, text = dbase.get_book(alias)
    if not title:
        abort(404)
    return render_template('book.html', menu=dbase.getMenu(), title=title, text=text)

@app.route("/my_lib")
def my_lib():
    return render_template('my_lib.html', menu=dbase.getMenu(), books=dbase.get_books_all())

@app.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
    return render_template('login.html', menu=dbase.getMenu(), title='Авторизация', form=form)



@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            hash = generate_password_hash(form.psw.data)
            res = dbase.addUser(form.name.data, form.email.data, hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")

    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', category='success')
    return redirect(url_for('login'))

@app.route('/comment', methods=["POST", "GET"])
def comment():
    if request.method == 'POST':
        flash('Сообщение отправлено', category='success')
    return render_template('comment.html')

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", menu=dbase.getMenu(), title="Профиль")

if __name__ == "__main__":
    app.run(debug=True)