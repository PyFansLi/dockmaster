# -*- coding:UTF-8 -*-
from app import db

class User(db.Model):
    __tatlename__ = 'user'
    #id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), primary_key=True, unique = True)  
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime)
    engines = db.relationship('Engine', backref = "user", lazy = "dynamic")

    def __repr__(self):
        return '<User %r>' % (self.username)

class Engine(db.Model):
    __tatlename__ = 'engine'
    uuid = db.Column(db.String(80), primary_key=True, unique = True)
    hostname = db.Column(db.String(80))
    host = db.Column(db.String(80))
    port = db.Column(db.String(80))
    status = db.Column(db.String(20))
    user_name = db.Column(db.String(80), db.ForeignKey('user.username'))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Engine %r_%r>' % (self.user_name, self.host)


