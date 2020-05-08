from flask import render_template
from app import app
from app.forms import LoginForm

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

def f1():
   a = [ 1, 2, 3, 4]
   c = sum(a)
   return str(c)

@app.route('/login')
def login():
    form = LoginForm()
    str = calc()
    return render_template('login.html', title='Sign In ' + calc(), form=form)


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
