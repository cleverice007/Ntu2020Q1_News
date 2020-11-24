from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import pandas as pd
import datetime as dt

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/data.html", methods=["POST", "GET"])
def data():
    data = request.get_json('info')
    userId = data['userId']
    search = data['whattosearch']
    href = data['whattoclick']
   
