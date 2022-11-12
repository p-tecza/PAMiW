from time import sleep
from flask import Flask, redirect, url_for, render_template, request, make_response
from bcrypt import checkpw
from uuid import uuid4
import redis
import json

app=Flask(__name__)
redis_db=redis.Redis()

hashed_password=b'$2b$12$L7QA3bW53Ulp0m4jYaF23.4S3UTFUH.tZVXB9IgJXdMd2TdHCN8tO'
authenticated_users={}
name_of_user=""
#Pass135

@app.route("/")
def login_page():
    sid = request.cookies.get("sid")
    if sid in authenticated_users:
        return render_template("index.html",name_pass=name_of_user)
    return render_template("login.html")

@app.route("/page", methods=["POST","GET"])
def main_page():
    name = request.form["name"]
    password = request.form["pass"]

    if checkpw(password.encode('utf-8'),hashed_password) and name=="user":
        sid = str(uuid4())
        authenticated_users[sid] = name
        global name_of_user
        name_of_user=name
        response = redirect("/", code=302)
        response.set_cookie("sid", sid)
        return response
    else:
        return render_template("login.html", wrongLoginData="wrong password/username.")


@app.route("/login_form", methods=["GET"])
def login_test():
    return "display_login_form", 200


@app.route("/logout", methods=["GET"])
def logout():
    #global authenticated_users
    #authenticated_users={}
    response= make_response(request.host)
    response.set_cookie('sid', '', expires=0)
    #print(request.host)
    return response 


""" @app.route("/products_file", methods=["GET"])
def fetch_products():
    #f=open("products.txt","r")
    #content=f.read()
    return 200 """

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


def prepare_json(db): #git

    whole_json="["
    it=0

    for x in db:
        whole_json+=(redis_db.get(x).decode())
        whole_json=whole_json.replace("'",'"')
        if(it!=len(db)-1):
            whole_json+=","
        it+=1

    whole_json+="]"

    return whole_json

@app.route("/fetch_json", methods=["GET"]) #git
def return_json():
    f=open("./srv/products.json","r")
    content=f.read()

    db_products=redis_db.keys()
    
    res=prepare_json(db_products)

    #whole_json="["

    """ for x in db_products:
        whole_json+=(redis_db.get(x).decode())
        whole_json=whole_json.replace("'",'"')
        whole_json+=","

    whole_json+="]"

    print("=======================")
    print(whole_json)
    print("=======================")
    print(json.dumps(whole_json))
    print("=======================") """

    #print(content)
    return res

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)




