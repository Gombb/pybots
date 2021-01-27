from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import queries

app = Flask(__name__, template_folder="templates")
bcrypt = Bcrypt(app)
app.secret_key = b'\xe3\r\x8b<\xa1\xc4L2S\x9c\xc4\xbew\x03N\xf0'


@app.route('/')
def index():
    print(session)
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    password_input = request.form.get("inputPassword")
    if bcrypt.check_password_hash(queries.get_password_hash(), password_input):
        session["status"] = "logged in"
    return redirect("/")


if __name__ == '__main__':
    app.run()
