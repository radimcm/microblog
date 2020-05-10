doc: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

// test in PYTHON:
set FLASK_APP=microblog.py
flask run
pip freeze

// deploy on HEROKU
heroku apps:create ub30
heroku config:set FLASK_APP=microblog.py
git push heroku master
//heroku ps:scale web=1
heroku logs -n 200
heroku logs --tail

// add user into database 
from app.models import User
u = User(username='rcmar', email='rcmar@sygic.com')
u.set_password('radim1111')
from app import db
db.session.add(u)
db.session.commit()