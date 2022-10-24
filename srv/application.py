from flask import Flask, redirect, url_for, render_template, request

app=Flask(__name__)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/page", methods=["POST"])
def main_page():
    name = request.form["name"]
    password = request.form["pass"]

    if password=="password" and name=="user":
        return render_template("mainpage.html", name_pass=name)
    else:
        return "Wrong name/pass", 400

@app.route("/simple_text", methods=["GET","POST"])
def test():
    return "<h1>works for me</h1>", 200

@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run()


