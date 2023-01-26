from flask import Flask, redirect, url_for, render_template, request, make_response, send_file, session
from bcrypt import checkpw, hashpw, gensalt
from flask_session import Session
from uuid import uuid4
import redis
import json
from pathlib import Path
import os

app=Flask(__name__)
redis_url = "redis://127.0.0.1"
app.config["REDIS_URL"] = redis_url
redis_db=redis.Redis()
redis_user_db=redis.Redis(db=1)
redis_email_db=redis.Redis(db=2)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

authenticated_users={}
name_of_user=""
number_of_entries=0 #TESTOWANIE
previous_no_entries=0 #TESTOWANIE
app.secret_key ="thekey"
UPLOAD_FOLDER="uploaded/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def login_page():
    sid = request.cookies.get("sid")
    if sid in authenticated_users:
        global number_of_entries #TESTOWANIE
        number_of_entries+=1 #TESTOWANIE
        return render_template("index.html",name_pass=name_of_user, number_of_entries=number_of_entries)
    session['basket']=[]
    return render_template("login.html")

@app.route("/page", methods=["POST","GET"])
def main_page():
    name = request.form["name"]
    password = request.form["pass"]
    hashed_password=redis_user_db.get(name)

    if not hashed_password:
        return render_template("login.html", wrongLoginData="user does not exist.")

    if checkpw(password.encode('utf-8'),hashed_password):
        sid = str(uuid4())
        authenticated_users[sid] = name
        global name_of_user
        name_of_user=name
        response = redirect("/", code=302)
        response.set_cookie("sid", sid)
        return response
    else:
        return render_template("login.html", wrongLoginData="wrong password/username.")

@app.route("/logout", methods=["GET"])
def logout():
    response= make_response(request.host)
    response.set_cookie('sid', '', expires=0)
    return response 

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
    db_products=redis_db.keys()
    res=prepare_json(db_products)
    return res


@app.route("/subscribe", methods=["POST"])
def job(): #TESTOWANIE
    data = request.get_json()
    previous_no_entries=data['noVisitors']

    global number_of_entries

    while True:
        if(number_of_entries>int(previous_no_entries)):
            return str(number_of_entries)

@app.route("/register")
def register_user():
    return render_template("register.html")

@app.route("/addnewuser", methods=["POST"])
def add_user():

    login = request.form["name"]
    password = request.form["pass"]
    email=request.form["email"]

    if(redis_user_db.get(login)):
        return render_template("register.html", errorMsg="user with that name already exists.")
    else:
        pass_bytes=password.encode('utf-8')
        hash=hashpw(pass_bytes,gensalt())
        redis_user_db.mset({str(login):hash})
        redis_email_db.mset({str(login):str(email)})
        return redirect("/",code=302)


@app.route("/get_image/<image_name>")
def response_image(image_name):
    path="product-images/"+image_name
    return send_file(path,mimetype="img/gif")

@app.route("/product_page/get_image/<image_name>")
def response_image2(image_name):
    path="product-images/"+image_name
    return send_file(path,mimetype="img/gif")


@app.route("/product_page/<prod_name>", methods=["GET"])
def prod(prod_name):
    return render_template("product.html",product=prod_name)

@app.route("/product_image/<product_name>")
def prod_im(product_name):
    print("BEFORE PROD NAME: "+product_name)
    product_name=product_name.replace("_"," ")
    print("PROD NAME: "+product_name)
    # product_json=redis_db.get(product_name).decode()
    prod = prepare_json([product_name])
    #print("PROD JSON: ",product_json)
    #prods=prepare_json(product_json)
    return prod

@app.route("/addtobasket/<product_name>")
def add_basket(product_name):
    session["basket"].append(product_name)
    print(session["basket"])
    return "ok"

@app.route("/basketpage")
def redbasket():
    return render_template("basket.html")


@app.route("/getproducts")
def getprods():
    return session["basket"]

@app.route("/reset_basket")
def resbas():
    session["basket"]=[]
    return "ok"

@app.route("/buystuff")
def buystuf():
    if len(session["basket"]) < 1:
        return "no items in basket."
    else:
        for prod in session["basket"]:
            prod_name=prod.replace("_"," ")
            prod_json=prepare_json([prod_name])
            prod_json=prod_json[1:len(prod_json)-1]
            normal_json=json.loads(prod_json)
            normal_json["quantity"]=int(normal_json["quantity"])-1
            if normal_json["quantity"] < 0:
                normal_json["quantity"]=1
                return "some of items are sold out, refresh main page."
            to_write_json=json.dumps(normal_json)
            redis_db.mset({prod_name:to_write_json})

        dl=len(session["basket"])
        session["basket"]=[]
        return "you bought "+str(dl)+" items."

@app.route("/redirect_upload")
def redup():
    return render_template("upload.html")

@app.route("/upload_file", methods=["POST"])
def upload_image():
    file=request.files["plik"]

    path=app.config['UPLOAD_FOLDER']
    Path(path).mkdir(parents=True, exist_ok=True)

    save_location=path+"/"+str(file.filename)
    file.save(save_location)
    return redirect("/redirect_upload")

@app.route("/redirect_browse")
def redbrowse():
    return render_template("browse.html")

@app.route("/files")
def show_files():
    path=app.config['UPLOAD_FOLDER']
    files=os.listdir(path)
    return files

@app.route("/file/<filename>")
def fetch_file(filename):
    path=app.config['UPLOAD_FOLDER']+"/"+str(filename)
    return send_file(path)

@app.route("/gotocontact")
def contact():
    return render_template("contact.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True) # threaded = True dla long pollingu




