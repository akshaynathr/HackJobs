from flask import Flask, render_template,request
from models import dbSetUp

app=Flask(__name__)

dbSetUp()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')



@app.route('/add')
def addContent():
    return render_template('add.html')
