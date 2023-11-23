
import firebase_admin, requests
from firebase_admin import credentials, firestore
from bs4 import BeautifulSoup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template,request
from datetime import datetime

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    X = "作者:陳姵汝 2023-11-23<br>"
    X += "<a href=/mis>資訊導論</a><br>"
    X += "<a href=/today>日期時間</a><br>"
    X += "<a href=/welcome?nick=tcyang>傳送使用者暱稱</a><br>"
    X += "<a href=/about>姵汝網頁</a><br>"
    X += "<a href=/account>表單</a><br>"
    X += "<a href=/read>讀取Firestore資料</a><br><br>"

    X += "<a href=/aboutcpj>我的個人簡介</a><br>"
    X += "<a href=/miss>MIS職業介紹</a><br>"
    X += "<a href=/hobby>興趣何倫碼</a><br>"
    X += "<a href=/slef>自傳履歷</a><br>"
    X += "<a href=/spider>網路爬蟲擷取子青老師課程資料</a><br><br>"
    return X 

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html",datetime = str(now))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")


@app.route("/read")
def read():
    db = firestore.client()
    Result = ""
    collection_ref = db.collection("人選之人─造浪者")
    #docs = collection_ref.where(filter=FieldFilter("name","==", "王淨")).get()
    docs = collection_ref.order_by("birth", direction=firestore.Query.DESCENDING).get()

    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/aboutcpj")
def about1():
    return render_template("aboutcpj.html")

@app.route("/miss")
def about2():
    return render_template("miss.html")

@app.route("/hobby")
def about3():
    return render_template("hobby.html")

@app.route("/slef")
def about4():
    return render_template("slef.html")

@app.route("/spider")
def spider():
    info = ""
    url = "https://www1.pu.edu.tw/~tcyang/course.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    #print(Data.text)
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".team-box")
    

    for x in result:
        info += x.find("h4").text + "<br>"
        info += x.find("p").text + "<br>"
        info += x.find("a").get("href") + "<br>"
        info += "<img src=https://www1.pu.edu.tw/~tcyang/" + x.find("img").get("src") + "></img><br><br>"
    return info

if __name__ == "__main__":
    app.run(debug=True)
""