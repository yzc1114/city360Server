# -*- coding: utf-8 -*-
from utils import create_app
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'city360.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
# manager = Manager(app=app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userIdentity = db.Column(db.String(10))
    openid = db.Column(db.String(20))
    avatarUrl = db.Column(db.String(20))
    nickName = db.Column(db.String(20))
    own_projects = db.relationship('User_Owns_Projects', backref='owner', lazy='dynamic')
    in_projects = db.relationship('User_In_Projects', backref='worker', lazy='dynamic')

    def __init__(self, openid, userIdentity, avatarUrl, nickName):
        self.avatarUrl = avatarUrl
        self.userIdentity = userIdentity
        self.openid = openid
        self.nickName = nickName

    def __repr__(self):
        return '<User %r>' % self.avatarUrl


class Project(db.Model):
    #
    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(20))
    creatorOpenid = db.Column(db.String(20))
    projectStatus = db.Column(db.String(20))
    mainProject = db.Column(db.Integer)
    createTimeStamp = db.Column(db.Integer)
    projectCity = db.Column(db.String(20))
    projectStreetBlock = db.Column(db.String(20))
    workersCount = db.Column(db.Integer)
    own_schemes = db.relationship('Project_Owns_Schemes', backref='project',
                                   lazy='dynamic')
    own_messages = db.relationship('Project_Owns_Messages', backref='project', lazy='dynamic')

    def __init__(self,
                 projectName="",
                 creatorOpenid="",
                 projectStatus="",
                 mainProject=False,
                 createTimeStamp="",
                 projectCity="",
                 projectStreetBlock="",
                 workersCount=0):
        self.projectName = projectName
        self.creatorOpenid = creatorOpenid
        self.projectStatus = projectStatus
        self.mainProject = mainProject
        self.createTimeStamp = createTimeStamp
        self.projectCity = projectCity
        self.projectStreetBlock = projectStreetBlock
        self.workersCount = workersCount

    def __repr__(self):
        return '<Project %r>' % self.id


class User_Owns_Projects(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)

    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id


class User_In_Projects(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)

    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id


class Project_Owns_Schemes(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    imageFileName = db.Column(db.String(20), primary_key=True)
    votes = db.Column(db.Integer)
    for_show = db.Column(db.Boolean)

    def __init__(self, project_id, imageFileName, votes=0, for_show=False):
        self.project_id = project_id
        self.imageFileName = imageFileName
        self.votes = votes
        self.for_show = for_show


class Project_Owns_Messages(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    message_content = db.Column(db.Text, primary_key=True)

    def __init__(self, project_id, message_content):
        self.project_id = project_id
        self.message_content = message_content


def db_init():
    db.create_all()

@app.route("/")
def index():
    return "real hello world"


if __name__ == '__main__':
    db_init()
    print(User)
    print("start server")
    app.run(host="0.0.0.0", port=5000)
