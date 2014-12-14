Stress Reliever
---

Vent to other Penn students - write your frustrations anonymously to vent.
Help other Penn students by writing comforting things in response.

### Develop

Requirements
---
* Python 2.7 or 2.6
* Sqlite
* pip

Getting started
---


Use the requirements.txt to start dependencies in your virtualenv:

~~~ sh
$ pip install -r requirements.txt
~~~

Start the server:

~~~ sh
$ fab run
~~~

Open the browser; `http://localhost:5000` or with the terminal(OS X):

~~~ sh
$ open http://localhost:5000
~~~

Initialize db
---

Set the db parameters in the default_settings.py or in the production.cfg file and start python interactive shell within the flask environment:

~~~ sh
$ fab shell
>>> db.create_all()
>>> exit()
~~~


Unit testing
---

Add unittests to the manage_tests.py file and then start running the tests:

~~~ sh
$ fab tests
~~~

Production Configuration
---

To activate the production configuration; export the variable:

~~~ sh
$ export PRODUCTION_SETTINGS=/path/to/production.py
~~~

***For Heroku using gunicorn and production settings, do the following:***.

**Heroku Postgresql Database** as primary,
Check [heroku](https://devcenter.heroku.com/articles/heroku-postgresql#establish-primary-db).

~~~ sh
$ heroku config:set PYTHONPATH='fakepath'
$ heroku config:add PRODUCTION_SETTINGS='application/production.py'
~~~

Alembic Migrations
---

~~~ sh
$ alembic revision --autogenerate -m "Added users table"
~~~

Submit
---
1. make a ZIP and send it to s.clara.wu@gmail.com

ToDo
---
* Choose a section 
* [Directions](https://docs.google.com/document/d/1e-FD2u_JIjxvkDdg0RV7lYku2RZ_xVSToW3UmLjNIWg/edit?usp=sharing)

Changelog
---
* Tell us what you did
