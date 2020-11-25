# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:27:47 2020

@author: ZuroChang
"""


from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask import request
from . import main
from .forms import NameForm
# from .. import db
# from ..models import User

# @main.route('/', methods=['POST'])
# def index():
#     form=NameForm()
#     if form.validate_on_submit():
#         session['name']=form.name.data
#         return redirect(url_for('.index'))
    
#     return(
#         render_template('index.html',form=form,name=session.get('name'))
#     )


@main.route('/', methods=['GET','POST'])
def _index():
    if request.method=='POST':
        userId=request.form["userId"]
        Searching=request.form["searching"]
        URI=request.form['URI']
        
        print(userId)
        print(Searching)
        print(URI)
    
    return (render_template('index.html'))