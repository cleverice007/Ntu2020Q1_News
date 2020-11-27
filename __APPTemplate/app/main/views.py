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
import json
import pandas as pd


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
    df=pd.read_json(r'/Users/yanyuming/Desktop/碩士課程/壽險/NLP/News_DailyData/20201017.json')
    info = ['title','source','pubdate' ]
    json_dict=dict(zip(df.link,df[info].values))
    if request.method=='POST':
        userId=request.form["userId"]
        Searching=request.form["searching"]
        URI=request.form['URI']
        file = ('/Users/yanyuming/Desktop/碩士課程/壽險/NLP/__APPTemplate/data.json')
        with open(file, 'r') as f:
            json_data = json.load(f)
        json_data['UserId'].append(userId)
        json_data['Searching'].append(Searching)
        json_data['Other'].append(list(json_dict[URI]))
        json_data['Other'].append(URI)
        #print(json_dict[URI])
        with open(file, 'w') as f:
            json.dump(json_data, f, separators=(',', ':'))
            f.close()

    return render_template('index.html',df=df,info = info , json_dict= json_dict)
