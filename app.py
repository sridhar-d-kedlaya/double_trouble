from flask import Flask, render_template, jsonify, make_response, request, send_from_directory, redirect
from connection import createUser, loginUser, checkAdmin, forgotPassword
from mail import sendMail


app = Flask(__name__)

@app.route("/api/create_user", methods=["POST"])
def create_user():
    # Get form data and send to createUser
    if createUser():
        return redirect("/login")
    else:
        return redirect("/create_user_error")

@app.route("/api/login_user", methods=["POST"])
def login_user():
    # Get form data and send to loginUser
    if loginUser():
        # Set cookie with user_id and user_name
        return redirect("/")
    else:
        return redirect("/loign_user_error")
    return jsonify(access_token=access_token), 200

@app.route("/api/forgot_password", methods=["POST"])
def forgot_password():
    # Send form data to forgotPassword()
    if forgotPassword() and sendMail():
        return redirect("/mail")
    else:
        return redirect("/forgot_password_error")

@app.route("/api/check_admin", methods=["POST"])
def check_admin():
    # Get cookie and get user id
    if checkAdmin(user_id):
        return true
    else:
        return false

@app.route("/", methods=["GET"])
def common():
    if getcookie()=="":
        return redirect("/login")
    else:
        rendered = render_template('common.html')
        resp = make_response(rendered)
        return resp

@app.route("/login", methods=["GET"])
def login():
    rendered = render_template('login.html')
    resp = make_response(rendered)
    return resp

@app.route("/create", methods=["GET"])
def create():
    rendered = render_template('create.html')
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

@app.route("/forgot", methods=["GET"])
def forgot():
    rendered = render_template('forgot.html')
    resp = make_response(rendered)
    return resp

@app.route("/mail", methods=["GET"])
def mail():
    rendered = render_template('mail.html')
    resp = make_response(rendered)
    return resp

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
    rendered = render_template('password_error.html')
    resp = make_response(rendered)
    return resp

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
