# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:27:47 2020

@author: ZuroChang
"""


from datetime import datetime
from flask import jsonify, Response
from flask import render_template, session, redirect, url_for
from flask import request
from . import main
from .forms import NameForm
import json
import pandas as pd
import os, sys
from itertools import tee
from pprint import pprint
from collections import defaultdict
current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(os.path.dirname(current_dir_path))
data_path = os.path.join(os.path.dirname(project_path), 'News_DailyData_AdjustedSource')
sys.path.append(os.path.dirname(project_path))
import Algorithm
#讀所有新聞
#path = '/Users/yanyuming/Desktop/碩士課程/壽險/NLP/News_DailyData'

dirs = os.listdir(data_path)
data = {}
for i in dirs:
  data[i] = pd.read_json(os.path.join(data_path, i))

#讀新聞檔案
'''
dirs = os.listdir('/Users/yanyuming/Desktop/碩士課程/壽險/NLP/News_DailyData')
data = {}
for i in dirs:
  data[i] = pd.read_json(os.path.join('/Users/yanyuming/Desktop/碩士課程/壽險/NLP/News_DailyData', i))
'''
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

@main.route('/get_default_news', methods=['GET'])
def _get_default_news():
  default_date = '20180530.json'
  default_news_data = data[default_date]
  default_news = {}
  for _, row in default_news_data.iterrows():
    if row['source'] not in default_news:
      default_news[row['source']] = list()
    default_news[row['source']].append([row['title'], row['link'], '20180530'])

  # results = [[source1, source2, source1_news, source2_news], [source3, source4....]]
  results = process_rtn_data(default_news)

  return render_template('news.html', r=results, news=default_news)

def process_rtn_data(rtn_data):
  rtn_data = {k: v for k, v in sorted(rtn_data.items(), key=lambda item: item[0])}
  results = []
  keys = list(rtn_data.keys())
  len_keys = len(keys)

  for i in range(0, len_keys, 2):
    if i + 1 < len_keys:
      source1 = keys[i]
      source2 = keys[i+1]
      tmp = [source1, source2]
    else:
      tmp = [keys[i], '']
    results.append(tmp)

  return results

@main.route('/', methods=['GET'])
def _index():
  return render_template('index.html')

def get_news_by_topics(topics):
  subtopics_data = {subtopic: defaultdict(list) for subtopic in topics[1:]}
  rtn_data = {topics[0]: subtopics_data}

  title = topics[0].lower()
  for date, df in data.items():
    for _, row in df.iterrows():
      news_title = row['title']
      if news_title:
        news_title = news_title.lower()
      else:
        news_title = ''

      if title in news_title:
        if topics[1].lower() in news_title:
          rtn_data[topics[0]][topics[1]][row['source']].append((row['title'], row['link']))
        if topics[2].lower() in news_title:
          rtn_data[topics[0]][topics[2]][row['source']].append((row['title'], row['link']))
        if topics[3].lower() in news_title:
          rtn_data[topics[0]][topics[3]][row['source']].append((row['title'], row['link']))

  return rtn_data

def get_news_by_date_and_title(date, title):
  title = title.lower()
  date_data = get_news_by_date(date)

  rtn_data = {}
  for source, news in date_data.items():
    for row in news:
      row_title = row[0].lower()
      if title in row_title:
        if source not in rtn_data:
          rtn_data[source] = list()
        rtn_data[source].append(row)

  return rtn_data

def get_news_by_date(date):
  rtn_data = {}
  date += '.json'
  if date not in data:
    return rtn_data

  date_data = data[date]
  for _, row in date_data.iterrows():
    if row['source'] not in rtn_data:
      rtn_data[row['source']] = list()
    rtn_data[row['source']].append((row['title'], row['link'], date[:8]))

  return rtn_data

def get_news_by_title(title):
  title = title.lower()
  rtn_data = {}
  for date, df in data.items():
    for _, row in df.iterrows():
      news_title = row['title']
      if news_title:
        news_title = news_title.lower()
      else:
        news_title = ''
      if title in news_title:
        if row['source'] not in rtn_data:
          rtn_data[row['source']] = list()
        rtn_data[row['source']].append((row['title'], row['link'], date[:8]))

  return rtn_data


@main.route('/get_default_recomm_news', methods=['GET'])
def _get_default_recomm_news():
  return "There is no recommendatory news"

@main.route('/get_recommend_news', methods=['GET'])
def _get_recommend_news():
  # if < 20:
  try:
    user = request.args.get('user')
    date = request.args.get('date')
    title = request.args.get('title')
  except:
    return "There is no recommendatory news"

  searched_data_path = os.path.join(project_path, 'data.json')
  with open(searched_data_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

  user_id_cnt = json_data['UserId']
  cnt = 0
  for user_id in user_id_cnt:
    if user_id == user:
      cnt += 1

  if cnt >= 10:
    topics = find_recommened_news()
    rtn_data = get_news_by_topics(topics)

    row_info = {topic: process_rtn_data(sub_data) for topic, sub_data in rtn_data[topics[0]].items()}
    return render_template('recommend_news.html', main_topic=topics[0],
                         subtopics=topics[1:],
                         r=row_info,
                         news={topic: subtopic_news for topic, subtopic_news in rtn_data[topics[0]].items()})
  else:
    return "There is no recommendatory news"

def find_recommened_news():
  topics = Algorithm.get_topics()
  return topics

def get_news(date, title):
  rtn_data = {}
  if date and title:
      rtn_data = get_news_by_date_and_title(date, title)
  elif date:
      rtn_data = get_news_by_date(date)
  elif title:
      rtn_data = get_news_by_title(title)

  return render_template('news.html', r=process_rtn_data(rtn_data), news=rtn_data)

@main.route('/get_news', methods=['GET'])
def _get_news():
  date = request.args.get('date')
  title = request.args.get('title')

  return get_news(date, title)

@main.route('/save_records', methods=['POST'])
def _save_records():
  user_id = request.form['userId']
  searching = request.form['searching']
  URI = request.form['URI']
  date = request.form['date']

  #if not date or not URI or not searching or not user_id:
#    return jsonify(success=True)

 # print(f"UserID: {user_id}, Searching: {searching}, Date: {date}")
  #print(f"URI: {URI}")

  df = data[date + '.json']
  info = ['title','source','pubdate']
  json_dict = dict(zip(df.link, df[info].values))

  searched_data_path = os.path.join(project_path, 'data.json')
  with open(searched_data_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

  '''
  # write into files
  with open('/Users/yanyuming/Desktop/碩士課程/source-codes/__APPTemplate/data.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
  '''
  print(user_id, searching, URI)
  json_data['UserId'].append(user_id)
  json_data['Searching'].append(searching)
  #if URI in json_dict:
  json_data['Other'].append(list(json_dict[URI]))
  json_data['Other'].append(URI)
  #print(json_dict[URI])

  with open(searched_data_path, 'w') as f:
    json.dump(json_data, f, separators=(',', ':'))

  '''
  with open('/Users/yanyuming/Desktop/碩士課程/source-codes/__APPTemplate/data.json', 'w') as f:
    json.dump(json_data, f, separators=(',', ':'))
  '''

  return jsonify(success=True)
