# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:36:25 2020

@author: ZuroChang
"""
# 不知道這能不能運行
from __init__ import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.username
