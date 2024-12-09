from flask import Flask, render_template, url_for, request,redirect,session
from flask_mail import Mail, Message
import sqlite3 as sql
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'bloodbankprofessional@gmail.com'
app.config['MAIL_PASSWORD'] = 'ujca rqcb fawn gmdx'
app.config['MAIL_DEFAULT_SENDER'] = 'bloodbankprofessional@gmail.com'
mail = Mail(app)

with sql.connect("database.db") as conn:
                    curr = conn.cursor()
                    # curr.execute("CREATE TABLE IF NOT EXISTS blood_acceptors (phone_no TEXT PRIMARY KEY, name TEXT, blood_group TEXT, quantity TEXT, gender TEXT, age TEXT, address TEXT, city TEXT, state TEXT, zip TEXT)")
                    curr.execute("CREATE TABLE IF NOT EXISTS blood_storage (blood_group TEXT PRIMARY KEY, quantity TEXT)")



@app.route('/send-mail/',methods=['POST','GET'])
def send_mail():
    if request.method == "POST":
        try:
            f_user = request.form["f_user"]
            with sql.connect("database.db") as conn:
                    curr = conn.cursor()
                    curr.execute("SELECT * FROM auth WHERE username = ?",(f_user,))
                    f_pass = curr.fetchall()
                    conn.close()
                    if f_pass:
                        row  = f_pass[0]
                        username = row[0]
                        password = row[1]
                        email = row[2]
                        m = f'Password Reminder for Your Blood Bank Account, {username}'
                        b = f'''
                        Dear {username},

                        We received a request to remind you of your password for your Blood Bank account. Your current password is provided below.

                        Your password: {password}

                        Please ensure to keep your password secure and do not share it with anyone. If you did not request this reminder, please contact our support team immediately.

                        Thank you for your attention to this matter.

                        Best regards,

                        Team Blood Bank
                        '''
                        msg = Message(m,
                                      recipients=[email])
                        msg.body = b
                        mail.send(msg)
                        
                        return redirect(url_for('login'))
                    else:
                        return '<h1>Invalid user not found</h1>'
        except:
            err = 'err'
    return redirect(url_for('login'))



user = ""
app.secret_key = 'BloodBank_key'
@app.route("/login")
def login():
    if not ('logged_in' in session and session['logged_in']):
        return render_template('login.html')
    else:
        return redirect(url_for('index'))
@app.route("/")
def index():
     if 'logged_in' in session and session['logged_in']:
        return render_template('index.html',u = session['username'])
     else:
          return redirect(url_for('login'))
@app.route("/signupreg")
def registration():
    return render_template('signup.html')
@app.route("/signup",methods = ['POST','GET'])
def signup():
    if request.method == "POST":
        try:
            r_user = request.form["username"]
            r_pas = request.form["password"]
            r_email = request.form["email"]
            with sql.connect("database.db") as conn:
                curr = conn.cursor()
                curr.execute("INSERT OR REPLACE INTO auth (username,password,email) VALUES(?,?,?)",(r_user,r_pas,r_email))
                conn.commit()
        except:
            conn.rollback()
        conn.close()
    return redirect(url_for('login'))
@app.route("/verify",methods = ['POST','GET'])
def verify():
    if request.method == "POST":
        pas = ""
        try:
            global user
            user = request.form["username"]
            pas = request.form["password"]
            with sql.connect("database.db") as conn:
                curr = conn.cursor()
                curr.execute(
                    "CREATE TABLE IF NOT EXISTS auth (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL,email TEXT NOT NULL)"
                )
                conn.commit()
                curr.execute("SELECT password FROM auth WHERE username = ?",(user,))
                d_pas = curr.fetchall()
                conn.close()
        except:
            print("Error occured")
        try:
            if pas == d_pas[0][0]:
                session['logged_in'] = True
                session['username'] = user
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))
    return redirect(url_for('login'))
 











@app.route("/donate", methods=["POST", "GET"])
def donate():
    if 'logged_in' in session and session['logged_in']:
        # Connect to the SQLite database
        with sql.connect("database.db") as con:
            cur = con.cursor()
        if request.method == "POST":
            try:
                # Extracting form data
                name = request.form["d_name"]
                phone_no = request.form["d_phone"]
                blood_group = request.form["d_blood"]
                quantity = request.form["d_quantity"]
                gender = request.form["d_gender"]
                age = request.form["d_age"]
                address = request.form["d_address"]
                city = request.form["d_city"]
                state = request.form["d_state"]
                zip_code = request.form["d_zip"]
                # Create the blood_donors table if it doesn't exist
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS blood_donors (phone_no TEXT PRIMARY KEY, name TEXT, blood_group TEXT, quantity TEXT, gender TEXT, age TEXT, address TEXT, city TEXT, state TEXT, zip TEXT)"
                )
                con.commit()
                
                # Insert or replace the donor details
                cur.execute(
                    "INSERT OR REPLACE INTO blood_donors (phone_no, name, blood_group, quantity, gender, age, address, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (phone_no, name, blood_group, quantity, gender, age, address, city, state, zip_code)
                )
                con.commit()
            except:
                    con.rollback()
        cur.execute("SELECT * FROM blood_donors")
        rows = cur.fetchall()
        con.close()
        return render_template("donate.html", rows=rows, u = session['username'])
    else:
         return redirect(url_for('login'))


@app.route("/accept", methods=["POST", "GET"])
def accept():
    if 'logged_in' in session and session['logged_in']:
        # Connect to the SQLite database
        with sql.connect("database.db") as con:
            cur = con.cursor()
        if request.method == "POST":
            try:
                # Extracting form data
                name = request.form["a_name"]
                phone_no = request.form["a_phone"]
                blood_group = request.form["a_blood"]
                quantity = request.form["a_quantity"]
                gender = request.form["a_gender"]
                age = request.form["a_age"]
                address = request.form["a_address"]
                city = request.form["a_city"]
                state = request.form["a_state"]
                zip_code = request.form["a_zip"]
                # Create the blood_donors table if it doesn't exist
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS blood_donors (phone_no TEXT PRIMARY KEY, name TEXT, blood_group TEXT, quantity TEXT, gender TEXT, age TEXT, address TEXT, city TEXT, state TEXT, zip TEXT)"
                )
                con.commit()
                
                # Insert or replace the donor details
                cur.execute(
                    "INSERT OR REPLACE INTO blood_acceptors (phone_no, name, blood_group, quantity, gender, age, address, city, state, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (phone_no, name, blood_group, quantity, gender, age, address, city, state, zip_code)
                )
                con.commit()
            except:
                    con.rollback()
        cur.execute("SELECT * FROM blood_acceptors")
        rows = cur.fetchall()
        con.close()
        return render_template("accept.html", rows=rows, u = session['username'])
    else:
         return redirect(url_for('login'))




@app.route('/storage')
def storage():
    if 'logged_in' in session and session['logged_in']:
        con = sql.connect("database.db")
        # con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM blood_storage")
        rows = cur.fetchall()
        con.close()
        return render_template("storage.html",rows=rows, u = session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/collected',methods=['POST','GET'])
def collected():
    if 'logged_in' in session and session['logged_in']:
        # Connect to the SQLite database
        with sql.connect("database.db") as con:
            cur = con.cursor()
        if request.method == "POST":
            try:
                blood_group = request.form['blood_group']
                quantity = request.form['quantity']
                phone = request.form['phone']
                donor_name = request.form['donor']
                print(blood_group,quantity,'joker')
                cur.execute("SELECT * FROM blood_storage WHERE blood_group = ?",(blood_group,))
                con.commit()
                row = cur.fetchall()
                b_g = row[0][0]
                print(blood_group,quantity,phone)
                q = float(row[0][1]) + float(quantity)
                cur.execute("UPDATE blood_storage SET  quantity = ?  WHERE blood_group = ?",(q,b_g))
                con.commit()
                cur.execute("DELETE FROM blood_donors WHERE phone_no = ?",(phone,))
                con.commit()
                print(user)
                cur.execute("SELECT * FROM auth WHERE username = ?",(session['username'],))
                res = cur.fetchall()
                con.commit()
                email = res[0][2]
                m = f'Thank You for Your Precious Blood Donation, {donor_name}'
                b = f'''
                Dear {donor_name},

                We hope this message finds you in good health and high spirits. On behalf of our entire team at the blood bank, we would like to extend our heartfelt gratitude for your recent blood donation.

                Your generous contribution is invaluable and plays a critical role in saving lives. Your selfless act of donating blood is a testament to your kindness and compassion, and it will make a significant difference to those in need of medical care.

                Thank you once again for your precious gift. We deeply appreciate your support and commitment to helping others.

                Warm regards,

                Blood Bank
                '''
                print(email,'hello')
                msg = Message(m, recipients=[email])
                msg.body = b
                mail.send(msg)


            except:
                 err = 'err'
    return redirect(url_for('storage'))


@app.route('/delivered',methods=['POST','GET'])
def delivered():
    if 'logged_in' in session and session['logged_in']:
        # Connect to the SQLite database
        with sql.connect("database.db") as con:
            cur = con.cursor()
        if request.method == "POST":
            try:
                blood_group = request.form['blood_group']
                quantity = request.form['quantity']
                phone = request.form['phone']
                cur.execute("SELECT * FROM blood_storage WHERE blood_group = ?",(blood_group,))
                con.commit()
                row = cur.fetchall()
                b_g = row[0][0]
                q = float(row[0][1]) - float(quantity)
                if q>=0:
                    cur.execute("UPDATE blood_storage SET  quantity = ?  WHERE blood_group = ?",(q,b_g))
                    con.commit()
                    cur.execute("DELETE FROM blood_acceptors WHERE phone_no = ?",(phone,))
                    con.commit()
                else:
                     return redirect(url_for('accept'))
            except:
                 err = 'err'
    return redirect(url_for('storage'))



    
     



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)




kj
