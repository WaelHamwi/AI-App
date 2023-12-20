

# ____________Login configuration________________
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
#TEMPLATE_DIR = os.path.abspath('../templates')
#STATIC_DIR = os.path.abspath('../static')

# app = Flask(__name__) # to make the app run without any
#app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)



class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Prof-Mazen', password='Mazen'))
users.append(User(id=2, username='eng', password='Wael'))
users.append(User(id=3, username='svu', password='online'))
users.append(User(id=4, username='1', password='1'))


app = Flask(__name__,template_folder="templates" , static_folder="assets")
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.route('/')
def man():
    return render_template('login.html')

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/index')
def index():
    

    if not g.user:
        return redirect(url_for('login'))

    return render_template('index.html')

from flask import Flask, render_template, request, send_from_directory
import cv2
import keras
import tensorflow as tf
import numpy as np


model = tf.keras.models.load_model("32x2x0CNN.model")


COUNT = 0
#app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1



@app.route('/login/index', methods=['POST'])
def home():
    global COUNT
    img = request.files['image']
    img.save('static/{}.jpg'.format(COUNT))    
    img_arr = cv2.imread('static/{}.jpg'.format(COUNT), cv2.IMREAD_GRAYSCALE)
    img_arr = cv2.resize(img_arr, (500,500))
    img_arr = img_arr / 255.0
    img_arr = img_arr.reshape(-1,500,500,1)
    prediction = model.predict(img_arr)

    x = round(prediction[0,0], 2)
    preds = np.array([x])
    COUNT += 1
    return render_template('prediction.html', data=preds)


@app.route('/load_img')
def load_img():
    global COUNT
    return send_from_directory('static', "{}.jpg".format(COUNT-1))


if __name__ == '__main__':
    app.run(debug=True)



@app.route('/')
def man():
    return render_template('login.html') 