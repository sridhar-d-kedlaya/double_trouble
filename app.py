from flask import Flask, render_template, make_response, request, redirect
from connection import createUser, loginUser, checkAdmin, forgotPassword
from mail import sendMail
import json
import re

app = Flask(__name__)

@app.route('/api/get_cookie/')
def get_cookie():
    return request.cookies.get('creds')

@app.route("/api/create_user", methods=["POST"])
def create_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    if createUser(username, email, password, firstname, lastname):
        return redirect("/login")
    else:
        return redirect("/create_user_error")

@app.route("/api/login_user", methods=["POST"])
def login_user():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    valid = loginUser(username, password)
    print(valid)
    if valid:
        resp = make_response(redirect("/"))
        resp.set_cookie("creds",json.dumps({"id": valid[2], "username": valid[1]}))
        return resp
    else:
        return redirect("/login_user_error")

@app.route("/api/forgot_password", methods=["POST"])
def forgot_password():
    email = request.form.get("email")
    pattern = "(UPDATE|update|DROP|drop|DELETE|delete|INSERT|insert|INTO|into|\")"
    if re.match(pattern, email):
        redirect("/forgot")
    pattern = ".*@.*(\\.).+"
    if re.match(pattern, email):
        redirect("/forgot")
    password = forgotPassword(email)
    if password[0] and sendMail(password[1]):
        return redirect("/")
    else:
        pattern = "(Integrity)"
        if re.match(pattern, type(password[1]).__name__):
            resp = make_response(redirect("/forgot_password_error"))
            resp.set_cookie("Error",str(password[1]))
            return resp
        else:
            return redirect("/forgot")

@app.route("/api/check_admin", methods=["POST"])
def check_admin():
    cookie = get_cookie()
    if cookie==None:
        return False
    try:
        cookie = json.loads(cookie)
        username = cookie["username"]
        user_id = cookie["id"]
    except:
        return False
    if checkAdmin(username, user_id):
        return True
    else:
        return False

@app.route("/", methods=["GET"])
def common():
    print(get_cookie())
    if get_cookie()==None:
        return redirect("/login")
    else:
        rendered = render_template('index.html')
        resp = make_response(rendered)
        return resp

@app.route("/login", methods=["GET"])
def login():
    rendered = render_template('login.html')
    resp = make_response(rendered)
    return resp

@app.route("/create", methods=["GET"])
def create():
    rendered = render_template('create_user.html')
    resp = make_response(rendered)
    return resp

@app.route("/admin", methods=["GET"])
def protected():
    if check_admin():
        return render_template('admin.html')
    else:
        rendered = render_template('unauthorised.html')
        resp = make_response(rendered)
        return resp

# @app.route("/forgot", methods=["GET"])
# def forgot():
#     rendered = render_template('forgot.html')
#     resp = make_response(rendered)
#     return resp

@app.route("/create_user_error", methods=["GET"])
def create_error():
    rendered = render_template('create_error.html')
    resp = make_response(rendered)
    return resp

@app.route("/login_user_error", methods=["GET"])
def login_error():
    rendered = render_template('login_error.html')
    resp = make_response(rendered)
    return resp

@app.route("/forgot_password_error", methods=["GET"])
def forgot_error():
    rendered = render_template('forgot_password_error.html')
    resp = make_response(rendered)
    return resp

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
