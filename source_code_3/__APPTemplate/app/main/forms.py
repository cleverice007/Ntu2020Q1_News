# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:39:20 2020

@author: ZuroChang
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name=StringField('What is your name?',validators=[DataRequired()])
    submit=SubmitField('Submit')

