from flask import Flask, redirect, url_for, render_template, request

app=Flask(__name__)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/page", methods=["POST"])
def main_page():
    name = request.form.get("name", "nothing")
    password = request.form.get("pass", "nothing")

    if password=="password" and name=="user":
        return render_template("mainpage.html", name_pass=name)
    else:
        return "Wrong name/pass", 400

if __name__=="__main__":
    app.run()


