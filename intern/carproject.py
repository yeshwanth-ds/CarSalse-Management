from flask import Flask, render_template,request,redirect,session
import pymysql as db
from flask_mail import Mail,Message
import os


f=os.path.join('static','images')
d=os.path.join('static','images')

cnx = db.connect(
    user='root',
    password='root',
    host='localhost',
    database='carproject',
    charset='utf8'
)

app = Flask(__name__) 

app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "2222carss@gmail.com"
app.config['MAIL_PASSWORD'] = "jegmgjrxwbkobhpw"
mail = Mail(app)

app.config['UPLOAD_FOLDER']=f
app.config['UPLOAD_FOLDER']=d

app.secret_key='super secret key'

@app.route('/')
def mainn():
    myimagee=os.path.join(app.config['UPLOAD_FOLDER'],'supra.jpg')

    return render_template("main.html", img=myimagee)

@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        myimage=os.path.join(app.config['UPLOAD_FOLDER'],'bugatti.jpg')
        return render_template("choose.html",img=myimage)
    else:
      
        return render_template("choose.html")

@app.route('/email')
def em():
    return render_template("email.html")

@app.route("/signin")

def signin():
  myimage=os.path.join(app.config['UPLOAD_FOLDER'],'ford.jpg')

  return render_template("signin.html", img=myimage)
  
@app.route('/signin',methods=['POST'])
def sign():
    u_name=request.form['q']
    p_word=request.form['g']
    e_mail=request.form['d']
    customer = {
        'user_name': u_name,
        'pass_word': p_word,
        'eemail': e_mail
        
    }
    cursor = cnx.cursor()
    insert_query = "INSERT INTO users (userid,password,email) VALUES (%(user_name)s, %(pass_word)s, %(eemail)s)"
    cursor.execute(insert_query, customer)
    cnx.commit()
    cursor.close()

    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        email = request.form['r']
        password_ = request.form['f']
        par = {'email': email, 'password': password_}
     
        cursor = cnx.cursor()
        query = "SELECT * FROM users WHERE email = %(email)s AND password = %(password)s"
        cursor.execute(query, par)
        res = cursor.fetchone()

        if res is not None:
            session['email'] = email
            
            return redirect('/choose')                
        else:
            return redirect('/login')

    myimagee = os.path.join(app.config['UPLOAD_FOLDER'], 'supra.jpg')

    return render_template("main.html", img=myimagee)

@app.route("/carform")
def we():
    if 'email' in session :
        email=session['email']
    
        myimage=os.path.join(app.config['UPLOAD_FOLDER'],'car.jpg')

        return render_template("carform.html", img=myimage,email=email)
    else:
       return  redirect('/')
 
  
@app.route('/carform',methods=['POST'])
def cardetails():
    
    regno=request.form['r']
    Carmodel=request.form['c']
    Ownername=request.form['o']
    Companyname=request.form['cn']
    Kms=request.form['km']
    ownership=request.form['os']
    ownermobileno=request.form['on']
    expectedprice=request.form['ep']
    status=request.form['s']
    posteddate=request.form['d']
    owneremail=session['email']
    
    #storing in dict
    car_data = {
        'regno': regno,
        'Carmodel': Carmodel,
        'Ownername': Ownername,
        'Companyname': Companyname,
        'Kms': Kms,
        'ownership': ownership,
        'ownermobileno': ownermobileno,
        'expectedprice': expectedprice,
        'status': status,
        'posteddate': posteddate,
        'owneremail':owneremail
    }
    cursor = cnx.cursor()
    insert_query = "INSERT INTO carproject (regno, Carmodel, Ownername, Companyname, Kilometers, Ownership, Ownerphoneno, Expectedprice, Status, Posteddate,owneremail) VALUES (%(regno)s, %(Carmodel)s, %(Ownername)s, %(Companyname)s, %(Kms)s, %(ownership)s, %(ownermobileno)s, %(expectedprice)s, %(status)s, %(posteddate)s,%(owneremail)s)"
    cursor.execute(insert_query, car_data)
    cnx.commit()
    cursor.close()

    return redirect('/')

@app.route('/home')
def web():
    a="unsold"
    cursor = cnx.cursor()
    
    query = "select * from carproject where Status=%s"
    cursor.execute(query,a)
    car_data = cursor.fetchall()
    cursor.close()
    car_data_dict = {}
    for row in car_data:
        regno = row[0]
        Carmodel = row[1]
        Ownername = row[2]
        Companyname = row[3]
        Kms = row[4]
        ownership = row[5]
        ownermobileno = row[6]
        expectedprice = row[7]
        status = row[8]
        posteddate = row[9]
        owneremail=row[10]

        car_data_dict[regno] = {
            'Carmodel': Carmodel,
            'Ownername': Ownername,
            'Companyname': Companyname,
            'Kms': Kms,
            'ownership': ownership,
            'ownermobileno': ownermobileno,
            'expectedprice': expectedprice,
            'status': status,
            'posteddate': posteddate,
            'owneremail':owneremail
        }

    myimage=os.path.join(app.config['UPLOAD_FOLDER'],'car.jpg')

    return render_template("home.html", args=car_data_dict,img=myimage)
@app.route('/buy', methods=['GET', 'POST'])
def buyy():
    buyno = None  # Assign a default value to 'buyno'

    if request.method == 'POST':
        buyno = request.form['t']
        cursor = cnx.cursor()
        query = "UPDATE carproject SET Status = 'sold' WHERE regno = %s"
        cursor.execute(query, (buyno,))
        cnx.commit()
        cursor.close()

    a = "unsold"
    cursor = cnx.cursor()
    query = "SELECT * FROM carproject WHERE Status = %s"
    cursor.execute(query, (a,))
    car_data = cursor.fetchall()
    cursor.close()

    car_data_dict = {}
    for row in car_data:
        regno = row[0]
        Carmodel = row[1]
        Ownername = row[2]
        Companyname = row[3]
        Kms = row[4]
        ownership = row[5]
        ownermobileno = row[6]
        expectedprice = row[7]
        status = row[8]
        posteddate = row[9]
        owneremail = row[10]

        car_data_dict[regno] = {
            'Carmodel': Carmodel,
            'Ownername': Ownername,
            'Companyname': Companyname,
            'Kms': Kms,
            'ownership': ownership,
            'ownermobileno': ownermobileno,
            'expectedprice': expectedprice,
            'status': status,
            'posteddate': posteddate,
            'owneremail': owneremail
        }

    e_mail = None  # Assign a default value to 'e_mail'
    if buyno is not None:
        cursor = cnx.cursor()
        query = "SELECT owneremail FROM carproject WHERE regno=%s"
        cursor.execute(query, (buyno,))
        e_mail = cursor.fetchone()
        if e_mail:
            e=e_mail[0]

            msg = Message("CAR SALES",
                        sender="2222carss@gmail.com",
                        recipients=["2222carss@gmail.com",e])
            msg.body = "Your car is sucessfully purchased"
            mail.send(msg)
            cursor.close()
            
            return "email sent"
        else:
            cursor.close()
            return "email not sent"

    myimage = os.path.join(app.config['UPLOAD_FOLDER'], 'buggati.jpg')

    return render_template("buy.html", args=car_data_dict, img=myimage)

@app.route('/search')
def search_form():
    myimage=os.path.join(app.config['UPLOAD_FOLDER'],'car.jpg')

    return render_template('search.html',img=myimage)

@app.route('/search',methods=['POST'])
def ser():

    searchtype=request.form['d']
    search_aa=request.form['y']

    cursor = cnx.cursor()
    query = "SELECT * FROM carproject WHERE {}=%s".format(searchtype)
    cursor.execute(query,search_aa)
    car_data = cursor.fetchall()
    cursor.close()
    myimage=os.path.join(app.config['UPLOAD_FOLDER'],'car.jpg')

    return render_template('searchres.html',args=car_data,img=myimage)

if __name__ == "__main__":
    app.run(debug=True)