from application import app
from flask import render_template, jsonify
from application.models import *
from flask import Flask, session, redirect, url_for, escape, request
from flask_oauthlib.client import OAuth, OAuthException
import random
import quality_control
from __init__ import facebook
import urllib2

@app.route('/')
def home():
    unfinRaps = Rap.query.filter(Rap.completed == False).order_by(-Rap.progress).limit(3).all()
    finRaps = Rap.query.filter(Rap.completed == True).limit(3).all()
    user = None
    if 'user_id' in session:
        user = User.query.filter_by(fb_id=session['user_id']).first()
    return render_template("info/home.html", title="Home", user = user, unfinRaps=unfinRaps, finRaps=finRaps)

@app.route('/raps/<int:rapID>')
def show_rap(rapID):
    rap = Rap.query.filter(Rap.id == rapID).first()
    pending_lines = Line.query.filter(Line.rapID == rapID) \
                               .filter(Line.isPending == True).all()
    print pending_lines
    pending_lines = quality_control.sort_lines_by_wilson_score(pending_lines)
    print pending_lines
    already_voted = []
    current_user = None
    if 'user_id' in session:
        current_user = User.query.filter_by(fb_id=str(session['user_id'])).first()
    line_users = []
    for i in pending_lines:
        if (current_user and i in current_user.lines):
            already_voted.append(True)
        else:
            already_voted.append(False)
        user = User.query.filter_by(fb_id=i.userID).first()
        line_users.append(user)
    accepted_line_users = []
    accepted_lines = Line.query.filter(Line.rapID == rapID) \
                               .filter(Line.isPending == False) \
                               .order_by(Line.lineIndex.asc()).all()
    for i in accepted_lines:
        user = User.query.filter_by(fb_id=i.userID).first()
        accepted_line_users.append((user.full_name,user.id, i.upvotes, i.downvotes))
    user = None
    return render_template("info/rap.html", user=current_user, rap=rap,
                           already_voted=already_voted,
                           line_users=line_users, accepted_line_users=accepted_line_users,
                           pending_lines=pending_lines, accepted_lines=accepted_lines)

@app.route('/add_rap', methods=['POST'])
def add_rap():
    try:
        if 'user_id' in session:
            if (not request.form['rap']) or (not request.form['rap_length']):
                return jsonify(success=False)

            r = Rap(request.form['rap'], request.form['rap_length'])
            db.session.add(r)
            db.session.commit()
        return redirect(url_for('home'))
    except:
        return redirect(url_for('home'))

@app.route('/add_line', methods=['POST'])
def add_line():
    index = 1 + 2*len(Line.query.filter(Line.rapID == request.form['rapID'],
                                        Line.isPending == False).all())
    rapID = request.form['rapID']
    try:
        if (not request.form['line1']) or (not request.form['line2']):
            return jsonify(success=False)

        l = Line(request.form['line1'], request.form['line2'],
            index, request.form['rapID'], session['user_id'])
        db.session.add(l)
        db.session.commit()
        return redirect(url_for('show_rap', rapID = rapID))
    except:
        return jsonify(success=False)

# THIS IS THE ROUTE I AM USING FOR THE UPVOTES

@app.route('/line/_upvote', methods=['POST', 'GET'])
def upvote_ajax():
    if request.method == 'POST':
        lineID = request.form['lineID']
        line = Line.query.get(lineID)
        current_user = None
        if 'user_id' in session:
            current_user = User.query.filter_by(fb_id=str(session['user_id'])).first()
            if (current_user and line not in current_user.lines):
                line.upvotes += 1
                current_user.lines.append(line)
                owner = User.query.filter_by(fb_id=line.userID).first()
                owner.rapGodPoints += 1
                db.session.add(current_user)
                db.session.commit()
                total_votes = line.upvotes - line.downvotes
                if total_votes >= 3:
                    select_best_line(line)
                return jsonify({"Success" : True, "Line" : lineID})
            return jsonify({"Success" : False, "Line" : lineID})

        else:
            return jsonify({"Success":False, "Line": lineID})


@app.route('/line/_downvote', methods=['POST', 'GET'])
def downvote_ajax():
    if request.method == 'POST':
        lineID = request.form['lineID']
        line = Line.query.get(lineID)
        current_user = None
        if 'user_id' in session:
            current_user = User.query.filter_by(fb_id=str(session['user_id'])).first()
            if (current_user and line not in current_user.lines):
                line.downvotes += 1
                current_user.lines.append(line)
                db.session.add(current_user)
                db.session.commit()
                total_votes = line.downvotes
                if total_votes >= 5:
                    db.session.delete(line)
                    db.session.commit()
                return jsonify({"Success":True, "Line": lineID})
            return jsonify({"Success":False, "Line": lineID})
        else:
            return jsonify({"Success":False, "Line": lineID})



def accepted_lines(rapID):
    return Line.query.filter(Line.rapID == rapID) \
                     .filter(Line.isPending == True).all()

def pending_lines(rapID):
    return Line.query.filter(Line.rapID == rapID) \
                     .filter(Line.isPending == True).all()

def select_best_line(line):
    rapID = line.rapID
    rap = Rap.query.get(rapID)
    all_pending_lines = pending_lines(rapID)
    best_line, other_lines = quality_control.best_line(all_pending_lines)
    if best_line:
        for line in other_lines:
            db.session.delete(line)
        best_line.isPending = False
        owner = User.query.filter_by(fb_id=best_line.userID).first()
        owner.rapGodPoints += 10
        rap.progress += 2
        db.session.add(best_line)
        db.session.commit()
        # finishes the rap if it reaches the max length
        if rap.progress >= rap.max_length:
            rap.completed = True
            db.session.add(rap)
            db.session.commit()

@app.route('/login')
def login():
    callback = url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True)
    print callback
    return facebook.authorize(callback=callback)

@app.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    session['user_id'] = me.data["id"]
    if not User.query.filter_by(fb_id=str(me.data['id'])).first():
        email = me.data['email']
        u = User(me.data['name'], me.data['id'], email)
        db.session.add(u)
        db.session.commit()
    return redirect(url_for('home'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/user/<int:userID>')
def profile(userID):
    user = User.query.filter_by(id=userID).first()
    lines = Line.query.filter_by(userID=user.fb_id, isPending=False)
    pending = Line.query.filter_by(userID=user.fb_id, isPending=True)
    return render_template("info/profile.html", pending=pending, user=user,
                           lines=lines)

@app.route('/unfinished')
def unfinished():
    raps = Rap.query.filter_by(completed=False).all()
    current_user = None
    if 'user_id' in session:
        current_user = User.query.filter_by(fb_id=str(session['user_id'])).first()
    return render_template("info/unfinished.html", raps=raps, user=current_user)

@app.route("/finished")
def finished():
    raps = Rap.query.filter_by(completed=True).all()
    current_user = None
    if 'user_id' in session:
        current_user = User.query.filter_by(fb_id=session['user_id']).first()
    return render_template("info/finished.html", raps=raps, user=current_user)

@app.route("/about")
def about():
    current_user = None
    if 'user_id' in session:
        current_user = User.query.filter_by(fb_id=str(session['user_id'])).first()
    return render_template("info/about.html", user=current_user)
