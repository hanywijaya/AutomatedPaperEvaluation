from flask import Flask
import sqlite3
from flask import render_template, url_for, request, redirect, session, jsonify
from controllers.Web import Web
from Database import Database
from Models.Users import Users
from Models.Article import Article
from Models.Mail import Mail
from random import randint
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'private_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

web = Web()
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def reload():
    session['essay'] = ""
    session['score1'] = int(0)
    session['score2'] = int(0)
    session.pop('essayId', None)
    session['essayId'] = None

def send_rp_email(email):
    user = Users()
    tempUser = user.getEmail(email)
    mail = Mail()
    mail.send_reset_password(email,tempUser['randomcode'])

@app.route("/")
def homepage():
    if not session.get("username"):
        return redirect("/login")
    
    reload()
    article = Article()
    data = article.getAll(session['id'])
    return render_template("home.html", heading="Welcome!", articles= data, id=session['id'], username= session['username'], email= session['email'], password= session['pass'], randomcode=session['randomcode'])
    

@app.route("/about")
def about():
    if not session.get("username"):
        return redirect("/login")
    
    reload()
    return render_template("about.html", heading="About APEE", id=session['id'],  username=session['username'], email=session['email'], password=session['pass'], randomcode=session['randomcode'])

@app.route("/register", methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        username  = request.form['username']
        email  =  request.form['email']
        password = request.form['password']

        user = Users()
        randomCode = session['randomcode'] = randint(100000, 999999)
        user_id = user.insert(username, email, password, randomCode)
        session['id'] = user_id

        return redirect(url_for('otp', email=email, randomCode=randomCode))

    return render_template("register.html")

@app.route("/otp")
def otp():
    email = request.args['email']
    randomCode = request.args['randomCode']
    mail = Mail()
    mail.send_verification(email, randomCode)
    return render_template("otp.html")

@app.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username  = request.form['username']
        password = request.form['password']

        user = Users()
        tempUser = user.authenticate(username, password)

        if tempUser and tempUser['DefiniteUser'] == 1:
            # make if tempuser definiteuser not == 1, error message for not verified user
            session['id'] = tempUser['id']
            session['username']  = tempUser['username']
            session['email'] = tempUser['email']
            session['pass'] = tempUser['pass']
            session['randomcode'] = tempUser['randomCode']

            return redirect(url_for('homepage'))
        else:
            # error message for username not found
            print('wrong')

    return render_template("login.html")

@app.route("/essay", methods=('GET', 'POST'))
def essay():
    if not session.get("username"):
        return redirect("/login")
    
    result = web.result()

    essayId = request.args.get('id')

    mdl = SentenceTransformer('all-MiniLM-L6-v2')
    model1 = pickle.load(open("finalized_model_svm_style.model","rb"))
    model2 = pickle.load(open("finalized_model_svm.model","rb"))

    article = Article()

    if essayId :
        essayNow = article.getOne(essayId)
        session['essayId'] = essayId
        session['essay'] = essayNow['content']
        session['score1'] = essayNow['scoreFocusnPurpose']
        session['score2'] = essayNow['ideasnDevelopment']
        # session['desc1'] = article.getDesc1(session['score1'])
        # session['desc2'] = article.getDesc2(session['score2'])
        # print(session['desc1'])
        
    if request.method == 'POST':
        if session['essayId']:
            essay  = request.form['essayInput']
            score1 = model1.predict(np.array([mdl.encode(essay)]))[0]
            score2 = model2.predict(np.array([mdl.encode(essay)]))[0]
            print("score 1: " + str(score1) + " score 2: " + str(score2))

            article.updateEssay(session['essayId'], essay, score1, score2)
            session['essay'] = essay
            session['score1'] = int(score1)
            session['score2'] = int(score2)

            # session['desc1'] = article.getDesc1(int(score1))
            # session['desc2'] = article.getDesc2(int(score2))

            return redirect(url_for('essay', id=essayId))
        else:
            essay  = request.form['essayInput']
            userID = session['id']

            score1 = model1.predict(np.array([mdl.encode(essay)]))[0]
            score2 = model2.predict(np.array([mdl.encode(essay)]))[0]
            print("score 1: " + str(score1) + " score 2: " + str(score2))

            session['essay'] = essay
            session['score1'] = int(score1)
            session['score2'] = int(score2)

            # session['desc1'] = article.getDesc1(int(score1))
            # session['desc2'] = article.getDesc2(int(score2))

            essayId = article.insert(essay, userID, score1, score2)

            return redirect(url_for('essay', id=essayId))
        
    desc1=article.getDesc1(session['score1'])
    desc2=article.getDesc2(session['score2'])

    return render_template("essay.html", heading="Add your Essay!", desc1=desc1, desc2=desc2, id=session['id'], username=session['username'], email=session['email'], password=session['pass'], article=session['essay'], score1=session['score1'], score2=session['score2'], randomcode=session['randomcode'])

@app.route("/printEssay")
def printEssay():
    article = Article()
    data = article.getAll2()
    return render_template("printEssay.html", essays=data)

@app.route('/users')
def users():
    user = Users()
    data = user.getAll()
    return render_template('users.html', users=data)

@app.route('/layout')
def layout():
    return render_template('layout.html', username= session['username'], email= session['email'], password= session['pass'], randomcode=session['randomcode'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/confirm/<token>')
def confirm_email(token):
    print(token)
    user = Users()
    tempUser = user.getCode(token)
    if tempUser:
        user.setDefinite(token)
        session['id'] =  tempUser['id']
        session['username']  = tempUser['username']
        session['email'] = tempUser['email']
        session['pass'] = tempUser['pass']
        session['randomcode'] = tempUser['randomCode']

        return redirect(url_for('homepage'))

@app.route('/fillEmail', methods=('GET', 'POST'))
def fill_email():
    if request.method == 'POST' :
        email = request.form['email']
        send_rp_email(email)
    return render_template("fillEmail.html")

@app.route('/resetPassword/<token>', methods=('GET', 'POST'))
def reset_password(token):
    if request.method == 'POST' :
        password = request.form['password']
        user = Users()
        user.updatePassword(token, password)
        return redirect(url_for('homepage'))
    else:
        return render_template("resetPassword.html", token=token)
if __name__=='__main__':
    app.run(debug=True)
    

