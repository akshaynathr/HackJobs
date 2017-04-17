from flask import Flask, render_template,request,session,redirect,url_for,flash
from models import dbSetUp
import rethinkdb as r

app=Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
dbSetUp()

@app.route('/')
@app.route('/home')
def home():
    connection=r.connect('localhost',28015)
    result=list(r.db('hackjobs').table('post').order_by(r.desc('time')).run(connection))
    connection.close()

    return render_template('index.html',results=result)





@app.route('/post',methods=['GET','POST'])
def postJobs():
    if request.method=='GET':
        return render_template('add.html')
    if request.method=='POST':
        title=request.form['title']
        link=request.form['link']
        details=request.form['text']
        if session.get('id',None):

            userid=session['id']
            connection=r.connect('localhost',28015)
            r.db('hackjobs').table('posts').insert({'userid':userid,'title':title,'time':r.now(),'link':link,'details':details }).run(connection)
            connection.close()
        else:
            return redirect(url_for('login',))





@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        if session.get('id',None):
            return render_template('user.html')
        else:

            return render_template('login.html')
    
              
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        connection=r.connect('localhost',28015)
        count=r.db('hackjobs').table('user').filter((r.row['username']==username) & (r.row['password']==password) ).count().run(connection)
        user=list(r.db('hackjobs').table('user').filter((r.row['username']==username) & (r.row['password']==password) ).run(connection))
        
        connection.close()
        print(count)
        if count==1:
            session['id']=user[0]['id']
            return redirect(url_for('user'))
        else:
            return "No user"

        
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
        user=list(r.db('hackjobs').table('user').filter((r.row['username']==username) & (r.row['password']==password) ).run(connection))
        session['id']=user[0]['id']
        return redirect(url_for('user'))

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


@app.route('/user',methods=['GET','POST'])
def user():
    if request.method=='GET':
        if session.get('id',None):
            connection=r.connect('localhost',28015)
            user=list(r.db('hackjobs').table('user').filter(r.row['id']==session['id']).run(connection))
            return render_template('user.html',name=user[0]['name'])
        else:
            return redirect(url_for('login'))

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    if session.get('id',None):
        session.pop('id',None)
        flash("Successfully logged out.")

        return redirect(url_for('login'))
    else:
        flash("Please login first.")

        return redirect(url_for('login'))
