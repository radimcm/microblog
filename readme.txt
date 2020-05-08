doc: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

test in PYTHON
set FLASK_APP=microblog.py
flask run


deploy on HEROKU

mozno:
  heroku config:set PYTHON_NO_SQLITE3=true
  git commit --allow-empty -m "test-new-python-runtime"
git push heroku master
heroku config:set FLASK_APP=microblog.py
heroku ps:scale web=1
heroku logs -n 200
heroku logs --tail
