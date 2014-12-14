from application import db

lines = db.Table('tags',
    db.Column('line_id', db.Integer, db.ForeignKey('line.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    fb_id = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True)
    rapGodPoints = db.Column(db.Integer, default=0)
    lines = db.relationship('Line', secondary=lines,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, full_name, fb_id, username):
        self.full_name = full_name
        self.username = username
        self.fb_id = fb_id

    def __repr__(self):
        return '<User %r>' % (self.username)


class Rap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    completed = db.Column(db.Boolean, default=False)
    max_length = db.Column(db.Integer)
    progress = db.Column(db.Integer, default=0)

    def __init__(self, title, max_length):
        self.title = title
        self.max_length = max_length

    def __repr__(self):
        return '<Rap %r>' % (self.title)


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line1 = db.Column(db.String(1000))
    line2 = db.Column(db.String(1000))
    isPending = db.Column(db.Boolean, default=True)

    rapID = db.Column(db.Integer)
    lineIndex = db.Column(db.Integer)

    userID = db.Column(db.Integer)

    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

    def __init__(self, line1, line2, lineIndex, rapID, userID):
        self.line1 = line1
        self.line2 = line2
        self.lineIndex = lineIndex
        self.rapID = rapID
        self.userID = userID

    def __repr__(self):
        return '<Lines %r\n\t%r>' % (self.line1, self.line2)

