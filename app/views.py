from flask import Flask, render_template,request,session
from models import dbSetUp
import rethinkdb as r

app=Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

#dbSetUp()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')



@app.route('/post',methods=['GET','POST'])
def postJobs():
    if request.method=='GET':
        return render_template('add.html')
    if request.method=='POST':
        title=request.form['title']
        link=request.form['link']
        details=request.form['details']
        if session['id']:

            userid=session['id']
            connection=r.connect('localhost',28015)
            r.db('hackjobs').table('posts').insert({'userid':userid,'title':title,'time':r.now(),'link':link,'details':details }).run(connection)
            connection.close()
        else:
            return redirect(url_for('login',))





@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        try:
            if session['id']:
                pass
            else:

                return render_template('login.html')
        except :
                return render_template('login.html')
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        connection=r.connect('localhost',28015)
        user=list(r.db('hackjobs').table('user').filter((r.row['username']) & (r.row['password']) ).count().run(connection))
        connection.close()

        
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        try:
            if session['id']:
                pass
            else:

                return render_template('register.html')
        except :
                return render_template('register.html')
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        connection=r.connect('localhost',28015)
        r.db('hackjobs').table('user').insert({'name':name,'username':username,'password':password,'email':email}).run(connection)
        return "Done"

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='GET':
        


        return render_template('add.html')
    elif request.method=='POST':
        title=request.form['title']
        link=request.form['link']
        text=request.form['text']
        connection=r.connect('localhost',28015)
        r.db('hackjobs').table('post').insert({'title':title,'link':link,'text':text}).run(connection)
        return "Done"
