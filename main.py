import logging
import os, sys
import sqlite3

from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.security import generate_password_hash, check_password_hash
from FDataBase import FDataBase

from createphone import *
from UserLogin import UserLogin
# from asterisk_ami import *
import flask_sijax
from getscreenyealink import *

# конфигурация
from ldap_search import ad_search_by_objectguid, ad_search_all

DATABASE = '/tmp/voip.db'
DEBUG = True
SECRET_KEY = 'sddf4894rk090ljr84rvn4rlx-x0e9le03cmse9m'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'voip.db')))
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
# login_manager.init_app(app)
login_manager.login_message = "Log in to access closed pages"
login_manager.login_message_category = "success"


menu = [{"name": "Main page", "url": "index"},
        {"name": "Phone book", "url": "phonebook"},
        {"name": "Configuring Yealink", "url": "yealinkconf"},
        {"name": "Yealink DSS", "url": "dssconf"},
        {"name": "Audio Conf", "url": "audioconf"},
        {"name": "About", "url": "about"},
        {"name": "Login", "url": "login"}]

flask_sijax.Sijax(app)

def comet_do_work_handler(obj_response):
    import time
    resp = select_log_ami()
    obj_response.html('#progress', resp)

    # for i in range(6):
    #     width = '%spx' % (i * 80)
    #     obj_response.css('#progress', 'width', width)
    #     obj_response.html('#progress', width)
    #
    #     # Yielding tells Sijax to flush the data to the browser.
    #     # This only works for Streaming functions (Comet or Upload)
    #     # and would not work for normal Sijax functions
    #     yield obj_response
    #
    #     if i != 5:
    #         time.sleep(sleep_time)
    # return resp


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


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
    dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
@app.route("/index")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route("/phonebook", methods=["POST", "GET"])
@login_required
def phonebook():
    # username = request.form.get['username']
    # print(username)

    if request.method == 'POST':
        print(request.form['username'])
        userreq = request.form['username']

        resp = ad_search_by_objectguid(userreq)

        # print(url_for('phonebook'))
        # phonebook1 = ad_search_by_objectGuid(str(39800083))
        # phonebook1 = ad_search_all()
        # phonebook_len = len(ad_search_all())
        # print(phonebook1)
        # resp.status_code = 200
        return resp
    else:


        print(url_for('phonebook'))
        # phonebook1 = ad_search_by_objectGuid(str(39800083))
        phonebook1 = ad_search_all()
        phonebook_len = len(ad_search_all())
        print(phonebook1)


        # photo_encoded = ad_search_all.photo_encoded()
        # for x in ad_search_all.return_list():
        #     print(x)
        # print(ad_search_all)
        return render_template('phonebook.html', menu=menu, return_list=phonebook1, return_list_len=phonebook_len)



@app.route("/user_check", methods=["POST", "GET"])
@login_required
def user_check():

    print(url_for('user_check'))
    # phonebook1 = ad_search_by_objectGuid(str(39800083))
    phonebook1 = ad_search_all()
    phonebook_len = len(ad_search_all())
    print(phonebook1)

    username = request.form['username']
    print(username)
    # validate the received values
    if username and request.method == 'POST':

        # cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # row = cursor.fetchone()
        row = ad_search_by_objectguid('username')
        print(row)

        if row:
            resp = jsonify('Username unavailable')
            resp.status_code = 200
            return render_template('phonebook.html', menu=menu, return_list=phonebook1, return_list_len=phonebook_len, resp=resp)
        else:
            resp = jsonify('Username available')
            resp.status_code = 200
            return render_template('phonebook.html', menu=menu, return_list=phonebook1, return_list_len=phonebook_len, resp=resp)
    else:
        resp = jsonify('Username is required field.')
        resp.status_code = 200
        return render_template('phonebook.html', menu=menu, return_list=phonebook1, return_list_len=phonebook_len, resp=resp)

    # photo_encoded = ad_search_all.photo_encoded()
    # for x in ad_search_all.return_list():
    #     print(x)
    # print(ad_search_all)
    # return render_template('phonebook.html', menu=menu, return_list=phonebook1, return_list_len=phonebook_len)



@app.route("/yealinkconf", methods=["POST", "GET"])
@login_required
def yealinkconf():
    if request.method == 'POST':
        print(request.form)
        getscreen = getscreenyealink(request.form['mac'])
        # ad_search_by_objectGuid(request.form['tabnumber'])
        create_mac(request.form['model'], request.form['mac'], request.form['number'], request.form['tabnumber'])
        # create_mac(model=request.form['model'], mac=request.form['mac'], number=request.form['number'], tabnumber=request.form['tabnumber'])
    # print(url_for('yealinkconf'))
    # create_mac(model=model, mac=mac, number=number, tabnumber=tabnumber)
    log_phone = select_log_phone()
    print(log_phone)
    return render_template('yealinkconf.html', title="Yealink Create Configuration", menu=menu, log_phone=log_phone)


@app.route("/dssconf", methods=["POST", "GET"])
def dssconf():
    if request.method == 'POST':
        print(request.form)
        indexid = request.form['index']
        print("indexid")
        print(indexid)
        text = request.form['text']
        print('text')
        print(text)

        # img = ImmutableMultiDict(indexid)
        # print(request.form.getlist['text'])

        resp = jsonify('Data received')
        resp.status_code = 200
        return resp



        # data = request.get_json(force=True, silent=True)
        # print("Test")
        # print(data)
        # index = data["index"]
        # print(index)

        # read_dss_button = select_dss_phone()
        # # print(request.form)
        # try:
        #     # print(request.form)
        #     return render_template('dssconf.html', title="DSS Button", menu=menu, read_dss_button=read_dss_button)
        #
        # except Exception:
        #     logging.exception('')
        #     return render_template('dssconf.html', title="DSS Button", menu=menu, read_dss_button=read_dss_button)


    else:
        read_dss_button = select_dss_phone()

        print(url_for('dssconf'))
        return render_template('dssconf.html', title="DSS Button", menu=menu, read_dss_button=read_dss_button)


@app.route("/audioconf", methods=["POST", "GET"])
def audioconf():
    if g.sijax.is_sijax_request:
        # resp = select_log_ami()
        # db_select_log_ami = select_log_ami()
        # obj_response.resp('#progress', resp)
        # The request looks like a valid Sijax request
        # Let's register the handlers and tell Sijax to process it
        # g.sijax.register_comet_callback('do_work', resp)
        # print(g.sijax.register_comet_callback('do_work', resp))
        g.sijax.register_comet_callback('do_work', comet_do_work_handler)
        return g.sijax.process_request()

    if request.method == 'POST':
        resp = select_log_ami()
        g.sijax.register_comet_callback('do_work', resp)
        print(g.sijax.register_comet_callback('do_work', resp))
        # g.sijax.register_comet_callback(resp, comet_do_work_handler)
        return g.sijax.process_request()


    # if request.method == 'POST':
    #     print(request.form['username'])
    #     userreq = request.form['username']
    #
    #     resp = select_log_ami()
    #
    #     # print(url_for('phonebook'))
    #     # phonebook1 = ad_search_by_objectGuid(str(39800083))
    #     # phonebook1 = ad_search_all()
    #     # phonebook_len = len(ad_search_all())
    #     # print(phonebook1)
    #     # resp.status_code = 200
    #     return resp
    else:

        print(url_for('audioconf'))
        db_select_log_ami = select_log_ami()
        print(db_select_log_ami)
        return render_template('audioconf.html', title="Audio Conference", menu=menu, db_select_log_ami=db_select_log_ami)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('contact.html', title="TEST", menu=menu)


@app.route("/login", methods=["POST", "GET"])
def login():
    # if 'userLogged' in session:
    #     return redirect(url_for('profile', username=session['userLogged']))
    # elif request.method == 'POST' and request.form['username'] == "test" and request.form['pwd'] == "123":
    #     session['userLogged'] = request.form['username']
    #     return redirect(url_for('profile', username=session['userLogged']))
    #
    # return render_template("login.html", title="User login", menu=menu)

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Invalid username/password", "error")

    return render_template("login.html", menu=menu, title="User login")


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page not found", menu=menu), 404


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out of your account", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Log out of your profile</a>
                <p><a href="{url_for('yealinkconf')}">Yealink Create Configuration</a>
                <p>user info: {current_user.get_email()}"""


@app.route('/background_process')
def background_process():
    try:
        lang = request.args.get('proglang', 0, type=str)
        if ad_search_by_objectguid(lang):
            return jsonify(result=lang)

        # if lang.lower() == 'python':
        #     return jsonify(result='You are wise')
        else:
            return jsonify(result='Try again.')
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    # app.run()
    app.run(host='10.45.3.132')
