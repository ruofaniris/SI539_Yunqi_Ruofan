import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask.ext.mysqldb import MySQL
from flask import Flask, session, redirect, url_for, escape, request
from datetime import timedelta
from flask.ext.mail import Mail, Message
from forms import ContactForm 					# NEW IMPORT LINE


app = Flask(__name__, template_folder='views')
app.secret_key = "super secret key"
mysql = MySQL()
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'
mysql.init_app(app)

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'umsiwebdesign@gmail.com'
app.config["MAIL_PASSWORD"] = '105sstate'
mail.init_app(app)

@app.before_request
def init_session():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')          					#This is the main URL
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/us')
def us():
    return render_template("us.html",name="us",title="Serendipity | About us")

@app.route('/login')
def login():
    return render_template("login.html",name = "login", title ="Serendipity | Log in")

@app.route('/signup')
def signup():
    return render_template("signup.html",name = "signup", title ="Serendipity | Sign up")

@app.route('/profile')
def go_profile():
    form = ContactForm()
    user_here = session['username']
    cur = mysql.connection.cursor()
    # cur.execute('''SELECT Firt_name, Last_name  FROM test2''')
    cur.execute("SELECT * from user_table where Email ='" + user_here + "'")
    user_data = cur.fetchone()
    email = str(user_data[1])
    password = str(user_data[2])
    firstname = str(user_data[3])
    lastname = str(user_data[4])
    age = str(user_data[5])
    gender = str(user_data[6])
    relation = str(user_data[7])
    country = str(user_data[8])
    intro = str(user_data[9])
    Photo_name = str(user_data[10])
    dir_name='/uploads'
    Photo_path = os.path.join(dir_name, Photo_name)
    return render_template("profile.html", form=form, name = "profile", title ="Personal Profile", photo=Photo_path, photome=Photo_path, age=age, gender=gender, country=country, status=relation, intro=intro, firstname=firstname, lastname=lastname)

@app.route('/<userid>', methods=['GET','POST'])
def other(userid):
    form = ContactForm()
    user_here = session['username']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from user_table where ID ='" + userid + "'")
    user_data = cur.fetchone()
    email = str(user_data[1])
    password = str(user_data[2])
    firstname = str(user_data[3])
    lastname = str(user_data[4])
    age = str(user_data[5])
    gender = str(user_data[6])
    relation = str(user_data[7])
    country = str(user_data[8])
    intro = str(user_data[9])
    Photo_name = str(user_data[10])
    dir_name='/uploads'
    Photo_path = os.path.join(dir_name, Photo_name)
    cur.scroll(0,mode='absolute')
    cur.execute("SELECT * from user_table where Email ='" + user_here + "'")
    userme_data = cur.fetchone()
    emailme = str(userme_data[1])
    # password = str(userme_data[2])
    firstnameme = str(userme_data[3])
    # lastname = str(userme_data[4])
    # age = str(userme_data[5])
    # gender = str(userme_data[6])
    # relation = str(userme_data[7])
    # country = str(userme_data[8])
    # intro = str(userme_data[9])
    Photome_name = str(userme_data[10])
    dirme_name='/uploads'
    Photome_path = os.path.join(dirme_name, Photome_name)
    return render_template("profile.html", name = "otherprofile", title ="Other Profile", form=form, photo=Photo_path, photome=Photome_path ,age=age, gender=gender, country=country, status=relation, intro=intro, firstname=firstname, lastname=lastname, email=email, emailme=emailme, firstnameme=firstnameme)

@app.route('/sendemailto<email>from<senderemail>by<sender>', methods=['GET','POST'])
def sendemail(email,senderemail,sender):
    form = ContactForm()
    msg = Message('Message from Serendipity', sender='umsiwebdesign@gmail.com', recipients=[email])
    msg.body="""
        From: %s <%s>
        Subject: %s
        Message: %s
        """ % (sender, senderemail, form.subject.data, form.message.data)
    mail.send(msg)
    # return render_template("index.html", form=form, name = "index", title ="Other Profile")
    return redirect(url_for('encounter'))

@app.route('/encounter')
def encounter():
    user_here = session['username']
    cur = mysql.connection.cursor()

    cur.execute("SELECT * from user_table where Email ='" + user_here + "'")
    userme_data = cur.fetchone()
    emailme = str(userme_data[1])
    # password = str(userme_data[2])
    # firstname = str(userme_data[3])
    # lastname = str(userme_data[4])
    # age = str(userme_data[5])
    # gender = str(userme_data[6])
    # relation = str(userme_data[7])
    # country = str(userme_data[8])
    # intro = str(userme_data[9])
    Photome_name = str(userme_data[10])
    dirme_name='/uploads'
    Photome_path = os.path.join(dirme_name, Photome_name)

    cur.scroll(0,mode='absolute')

    # gender = 'male'
    # cur.execute("Select * from user_table where Gender='" + gender + "'")
    cur.execute("Select * from user_table")
    users = cur.fetchall()
    length = len(users)
    print length
    return render_template("encounter.html", name = "encounter", title ="Encounter", users=users, useramount=length,photome=Photome_path)

@app.route('/postsignup', methods=['POST', 'GET'])
def postsignup():
    email = request.form['signupemail']
    password = request.form['signuppassword']
    firstname = request.form['signupfirstname']
    lastname = request.form['signuplastname']
    age = request.form['signupage']
    gender = request.form['signupgender']
    relation = request.form['signupstatus']
    country = request.form['signupcountry']
    intro = request.form['signupintro']
    Photo = request.files['signupphoto']
    if Photo and allowed_file(Photo.filename):
        Photo_name = Photo.filename
        dir_name='/uploads'
        Photo_path = os.path.join(dir_name, Photo_name)
        Photo.save(os.path.join(app.config['UPLOAD_FOLDER'], Photo_name))
    cur = mysql.connection.cursor()
    cur.execute('''insert into user_table (Email,Password,
                First_name, Last_name, Age, Gender, Relation,
                Country, Intro, Photo_name) VALUES
                ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'''
                % (email, password, firstname, lastname, age, gender,
                  relation, country, intro, Photo_name))
    mysql.connection.commit()
    # cur.close
    return redirect(url_for('login'))

@app.route('/postlogin', methods=['POST', 'GET'])
def postlogin():
    user = request.form['loginemail']
    pwd = request.form['loginpassword']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from user_table where Email='" + user + "' and Password='" + pwd + "'")
    data = cur.fetchone()
    if data is None:
        return render_template("404.html",name="loginfail",errormessage="Your username or password is wrong.")
    else:
        session['username'] = user
        return redirect(url_for('go_profile'))

@app.errorhandler(404)
@app.errorhandler(500)
def notfound(self):
    return render_template("404.html", name="wrongurl",errormessage="Where am I? Scroll down for details"),404

if __name__ == '__main__':	#Start the Development server
    app.run(debug=True)
