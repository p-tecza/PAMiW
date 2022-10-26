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
        return render_template("index.html", name_pass=name)
    else:
        return "Wrong name/pass", 400


@app.route("/login_form", methods=["GET"])
def login_test():
    return "display_login_form", 200


@app.route("/products_file", methods=["GET"])
def fetch_products():
    f=open("products.txt","r")
    content=f.read()
    return content, 200

@app.route("/simple_text", methods=["GET","POST"])
def test():
    return "<h1>works for me</h1>", 200

@app.route("/index", methods=["POST", "GET"])
def index():

    if request.method=="POST":
        login = request.form["login"]
        password = request.form["pass"]
        return render_template("index.html", username=login, greet="user: ")
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)


