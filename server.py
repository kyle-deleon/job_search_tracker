from flask import Flask, render_template, request, session, flash, redirect
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "keep it secret"

bcrypt = Bcrypt(app)
schema = "job_search_tracker"

@app.route('/')
def log_reg_landing():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("registration.html")

@app.route('/on_register', methods=['POST'])
def on_register():
    is_valid = True

    if len(request.form['em']) < 1:
        is_valid = False
        flash("Please enter an email")
    elif not EMAIL_REGEX.match(request.form['em']):
        is_valid = False
        flash("Please enter a valid email")
    else:
        mysql = connectToMySQL(schema)
        query = 'SELECT * FROM users WHERE email = %(em)s;'
        data = {
            'em':request.form['em']
        }
        user = mysql.query_db(query,data)
        if user:
            is_valid = False
            flash("email already in use")

    if len(request.form['fn']) < 2:
        is_valid=False
        flash("Fist name must be atleast 2 characters long.")
    if len(request.form['ln']) < 2:
        is_valid=False
        flash("last name must be atleast 2 characters long.")
    if len(request.form['pw']) < 8:
        is_valid=False
        flash("password must be atleast 8 characters long.")

    if request.form['pw'] != request.form['cpw']:
        is_valid=False
        flash("Passwords must match")

    if is_valid:
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(fn)s, %(ln)s, %(em)s, %(pw)s, NOW(), NOW())"
        data = {
            "fn": request.form['fn'],
            "ln": request.form['ln'],
            "em": request.form['em'],
            "pw": bcrypt.generate_password_hash(request.form['pw'])
        }
        mysql = connectToMySQL(schema)
        user_id = mysql.query_db(query,data)

        if user_id:
            session['user_id'] = user_id
            session['name'] = request.form['fn']
            return redirect ('/')

    return redirect('/')

@app.route("/on_login", methods=["POST"])
def on_login():
    is_valid = True

    if not EMAIL_REGEX.match(request.form['em']):
        is_valid = False
        flash("email is not valid")

    if is_valid:
        query = "SELECT users.id, users.first_name, users.password FROM users WHERE users.email = %(em)s"
        data = {
            'em': request.form['em']
        } 
        mysql = connectToMySQL(schema)
        result = mysql.query_db(query, data)

        if result:
            if not bcrypt.check_password_hash(result[0]['password'], request.form['pw']):
                flash("incorrect password and/or email")
                return redirect('/')
            else:
                session['user_id'] = result[0]['id']
                session['name'] = result[0]['first_name']
                return redirect('/account')
        else:
            flash("incorrect email and/or password")

    return redirect ('/')

@app.route('/on_logout')  
def on_logout():
    session.clear() 
    return redirect('/')

@app.route('/account')
def account():
    if "user_id" not in session:
        return redirect('/')

    query = "SELECT * FROM jobs where user_id = %(sid)s"
    data = {'sid':session['user_id']}
    mysql = connectToMySQL(schema)
    jobs = mysql.query_db(query, data)

    return render_template('account.html', jobs = jobs)

@app.route('/on_applied', methods=['POST'])
def on_applied():
    is_valid = True

    if len(request.form['company_name']) < 3:
        is_valid = False
        flash("Company Name must be 3 characters")
    if len(request.form['position']) < 6:
        is_valid=False
        flash("Postion must be atleast 6 characters long")
    if len(request.form['platform']) < 6:
        is_valid=False
        flash("Platform must be atleast 6 characters long")
    if len(request.form['link']) < 8:
        is_valid=False
        flash("Please enter Link")
    
    if is_valid:
        query = "INSERT INTO jobs (user_id, company_name, position, platform, company_link, created_at, updated_at) VALUES ( %(sid)s, %(company_name)s, %(position)s, %(platform)s, %(link)s, NOW(), NOW())"
        data = {
            "sid":session['user_id'],
            "company_name": request.form['company_name'],
            "position": request.form['position'],
            "platform": request.form['platform'],
            "link": request.form['link']
        }
        mysql = connectToMySQL(schema)
        mysql.query_db(query,data)
    
    return redirect('/account')

if __name__ == "__main__":
    app.run(debug=True)