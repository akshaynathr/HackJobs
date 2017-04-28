from flask import Flask, render_template,request,session,redirect,url_for,flash
from models import dbSetUp
import rethinkdb as r
from logging import  *
from logging.handlers import RotatingFileHandler
import os
import json

app=Flask(__name__, static_folder='static')
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
dbSetUp()

SLACK_TOKEN=os.environ['SLACK']
PAGE_LIMIT=30

from slacker_log_handler import SlackerLogHandler
slack_handler = SlackerLogHandler(SLACK_TOKEN, 'post',
                                  stack_trace=True,
                                  username='site-bot')
slack_handler.setFormatter(Formatter('%(message)s'))
file_handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)

file_handler.setLevel(ERROR)
app.logger.addHandler(slack_handler)

@app.route('/test')
def test():
    return render_template('index2.html')



@app.errorhandler(404)
def page_not_found(e):
    #app.logger.info('404 error'+request.url)
    return render_template('404.html'), 404



@app.route('/', defaults={'page': 0})
@app.route('/page/<int:page>')
def home(page):
    connection=r.connect('localhost',28015)
    name=''
    logout=''
    c=r.db('hackjobs').table('post').count().run(connection)
    skip_no=PAGE_LIMIT*page
    result=list(r.db('hackjobs').table('post').order_by(index=r.desc('time')).run(connection))
    if skip_no+30>=c:
        page=None
        
    if session.get('id',None):
        count=r.db('hackjobs').table('user').filter(r.row['id']==session['id']).count().run(connection)
        if count>1:
            user=list(r.db('hackjobs').table('user').filter(r.row['id']==session['id']).run(connection))
        
            name=user[0].get('name','')
            logout='(logout)'
    
    connection.close()
    
    return render_template('index.html',results=result,count=page,name=name,logout=logout)





@app.route('/post',methods=['GET','POST'])
def postJobs():
    if request.method=='GET':
        return redirect(url_for('add'))
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
            return redirect(url_for('user'))
        else:
            

        
            return render_template('login.html')
    
              
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        connection=r.connect('localhost',28015)
        count=r.db('hackjobs').table('user').filter((r.row['username']==username) & (r.row['password']==password) ).count().run(connection)
        user=list(r.db('hackjobs').table('user').filter((r.row['username']==username) & (r.row['password']==password) ).run(connection))
        
        connection.close()
         
        if count==1:
            session['id']=user[0]['id']
            return redirect(url_for('user'))
        else:
            flash("No user found")
            return render_template('login.html')

        
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        try:
            if session.get('id',None):
                return redirect(url_for('user'))
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
        if session.get('id',None):
            return render_template('add.html',logout='logout')
        else:
            return redirect(url_for('login'))
    elif request.method=='POST':
        title=request.form['title']
        link=request.form['link']
        text=request.form['text']
        userid=session['id']
        app.logger.error('New post added:'+title+' Link:'+link+' '+' Text:'+text)
        connection=r.connect('localhost',28015)
        r.db('hackjobs').table('post').insert({'title':title,'link':link,'text':text,'userid':userid,'time':r.now()}).run(connection)
        return redirect(url_for('home'))


@app.route('/user',methods=['GET','POST'])
def user():
    if request.method=='GET':
        if session.get('id',None):
            connection=r.connect('localhost',28015)
            user=list(r.db('hackjobs').table('user').filter(r.row['id']==session['id']).run(connection))
            result=list(r.db('hackjobs').table('post').order_by(index=r.desc('time')).filter(r.row['userid']==session['id']).run(connection))

            return render_template('user.html',name=user[0]['name'],result=result,logout='(logout)')
        else:
            return redirect(url_for('login'))

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    if session.get('id',None):
        session.pop('id',None)
        flash("Successfully logged out.")

        return redirect(url_for('login'))
    else:
        flash("Please login first.")

        return redirect(url_for('login'))

@app.route('/asfadf98fsadfa9090232asdfJSf90' ,methods=['GET','POST'])
def admin():
    if request.method=='GET':
        return render_template('admin.html')
    else:
        title=request.form['delete']
        connection=r.connect('localhost',28015)
        count=r.db('hackjobs').table('post').filter(r.row['title']==title).count().run(connection)
        if count==0:
            flash("No post found")
        else:
            r.db('hackjobs').table('post').filter(r.row['title']==title).delete().run(connection)
            connection.close()
            flash(title+"deleted successfully")
        return render_template('admin.html')



@app.route('/news/<path:path>')
def news(path):
    connection=r.connect('localhost',28015)
    #count=r.db('hackjobs').table('post').get(news_id).count().run(connection)
    results=list(r.db('hackjobs').table('post').filter(r.row['id']==path).run(connection))
    count=len(results)
    name=''
    if session.get('id',None):
        user=list(r.db('hackjobs').table('user').filter(r.row['id']==session['id']).run(connection))
        name=user[0]['name']

    logout='(logout)'
    if count>0:
        #results=list(r.db('hackjobs').table('post').get(path).run(connection))
        #print (results)
        #return json.dumps(results)
        return render_template('news.html',results=results,title=results[0]['title'],name=name,logout=logout)
    else:

        return render_template('news.html',results=[],name=name,logout=logout,title="No news found")


@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)



@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')
