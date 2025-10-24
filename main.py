import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, redirect, session, abort, g, make_response

from werkzeug.security import generate_password_hash, check_password_hash

from FDataBase import FDataBase

# config
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'afed134eaefdc2f9581821692b30b12cf5e8de92'


app = Flask(__name__)

app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())

@app.route("/add_post", methods=['POST', 'GET'])
def addPost():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавление статьи')

@app.route('/post/<alias>')
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template('login.html', title='Авторизация', menu=dbase.getMenu())


    # if 'userLogged' in session:
    #     return redirect(url_for('profile', username=session['userLogged']))
    # elif request.method == 'POST' and request.form['username'] == 'selfedu' and request.form['psw'] == '123':
    #     session['userLogged'] = request.form['username']
    #     return redirect(url_for('profile', username=session['userLogged']))
    # if request.method == 'POST' and (request.form['username'] != 'selfedu' or request.form['psw'] != '123'):
    #     flash('Неверная пара логин-пароль', category='error')
    #
    # return render_template('login.html', title='Авторизация', menu=dbase.getMenu())


@app.route("/logout")
def logout():
    res = make_response(f"<h1>Вы больше не авторизованы</h1>")
    res.set_cookie('logged', '', 0)
    return res


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегистрированы', category='success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в БД', category='error')
        else:
            flash('Неверно заполнены поля', category='error')

    return render_template('register.html', title='Регистрация', menu=dbase.getMenu())



    # return render_template('register.html', title='Авторизация', menu=dbase.getMenu())


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Профиль пользователя: {username}"


# @app.errorhandler(404)
# def pageNotFound(error):
#     return render_template('page404.html', title='Страница не найдена', menu=dbase.getMenu()), 404

if __name__ == "__main__":
    app.run(debug=DEBUG)
