We have created a web app using flask, a python web framework.
Additionally, it is being hosted at http://www.rapgenii.com/


application/
  Contains the most relevant code, including our models, views, and controllers, as in an MVC framework.

application/models.py - defines the structure of User, Rap, and Line data
application/manager.py - The Controller in our MVC model.
  Contains almost all of the website's logic.
  Contains code show the home screen, individual raps, individual users,
  add raps and lines, upvote or downvote lines, and the logic behind when to choose the
  best line and which line to choose.

application/__init__.py - sets up everything needed for the website to run.
  Includes adding various flask settings, setting up facebook authentication, and initializing the database

application/quality_control.py - contains the scoring system that we use to rank suggestions
  Determines the rap lines with the best rating using a wilson's score with
  85% certainty. Note that Wilson's score has many benefits over simpler
  scoring methods such as ratio or difference of upvotes and downvotes.

static/
  contains all css and javascript for displaying the frontend.
  Some of this comes from bootstrap, other things we wrote ourselves

templates/ - contains all of the html for our website, including
  base.html - contains the background and outline of our page
  info/     - these all extend the base.html file, and display relevant information, such as
              raps, user profile, etc.

