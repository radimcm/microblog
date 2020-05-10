from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np

import io
import random
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

from flask_login import current_user, login_user
from flask_login import login_required
from flask_login import logout_user
from flask import request
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')

@app.route('/index')
@login_required
def index():
    user = {'username': 'Dave'}
    posts = [
        {
            'author': {'username': 'Samuel'},
            'body': 'Roblox is a fantastic game!'
        },
        {
            'author': {'username': 'Emma'},
            'body': 'My way is the tik-tok wherever I go'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/articles')
def articles():
    return render_template('articles.html', title='Articles')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')        
        return redirect(url_for('index'))   
    str = calc()
    return render_template('login.html', title='Sign In', form=form, result = str)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


def onehot(label):
    if label == 0 : return [1, 0, 0, 0]
    if label == 1 : return [0, 1, 0, 0]
    if label == 2 : return [0, 0, 1, 0]
    if label == 3 : return [0, 0, 0, 1]
    return [0, 0, 0, 0]

def calc():
  dataset = [
   [0.25, 0.22, 1.00,  0],
   [0.25, 0.25, 1.00,  0],
   [0.50, 0.23, 1.50,  2],
   [0.25, 0.25, 2.00,  1],
   [0.40, 0.25, 0.90,  1],
   [0.40, 0.25, 1.50,  2],
   [0.60, 0.30, 2.50,  3],
   [0.29, 0.25, 1.16,  1],
   [0.60, 0.40, 0.20,  1]
  ]

  D = np.array(dataset)
  X = D[:,0:3]
  v = [ onehot(dataset[i][3]) for i in range(0,len(dataset))]
  y = np.array(v)
  NN = MLPRegressor(solver='adam',
                   alpha=0.0001,
                   activation='logistic',
                   hidden_layer_sizes=(16, 4),
                   random_state=1,
                   max_iter = 2000,
                   shuffle=True
                   )
  N = 3
  NN.fit(X, y)
  yref = y[0:N]
  yhat = NN.predict(X[0:N])
  return str(yhat[0:2])


@app.route("/matplot-as-image-<int:num_x_points>.png")
def plot_png(num_x_points=50):
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")
 