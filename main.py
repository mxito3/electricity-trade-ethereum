from flask import Flask,render_template,url_for,request,redirect,flash,request,session,make_response
from config.sql import Sql
from pathlib import Path
from config.user import User
from config.ethereum import ethereumUtil
import os
import time
import datetime
import uuid
import _thread
import threading
app=Flask(__name__)
app.secret_key=bytes(str(uuid.uuid4()),'utf-8')
uploadFloader='./static/upload'
app.config['UPLOAD_FLODER']=uploadFloader
sql=Sql("localhost",3306,'root','domore0325','elec')
globalCookie = "ypisthebest"
userOperator =User() 
etherUtil = ethereumUtil()

@app.route('/')
def index():
    sellingDetails = etherUtil.getSellingDetail()
    return render_template('index.html',sellingDetails = sellingDetails)
@app.route('/admin')
def admin():
    if globalCookie == request.cookies.get('session_id'):
        return render_template("admin.html")
    else:
        flash("管理员请先登录")
        return redirect('/login')

@app.route('/login',methods=['Post','GET'])
def signIn():
    if request.method == 'POST':
        form=request.form
        user_name=form.get('user_name')
        user_password=form.get('user_password')
        if  userOperator.existSuchUser(user_name,user_password):
            if user_name == 'admin':
                response=make_response(redirect('/admin'))
                response.set_cookie('session_id',globalCookie)
                return response
            else:
                user = userOperator.getUser(user_name,user_password)
                userInfo = {}
                userInfo["id"] = int(user[0][0])
                userInfo["address"] = user[0][1]
                userInfo["userName"] = user_name
                userInfo["balance"] = etherUtil.getElectricityAmount(userInfo["id"])
                userInfo["coinBalance"] = etherUtil.getCoinBalance(userInfo["addreess"])
                response=make_response(render_template('personal.html',user=userInfo))
                response.set_cookie('session',globalCookie)                
                return response
        else:
            flash("用户名密码不匹配")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/signup',methods=['Post','GET'])
def signUp():
    if request.method == 'POST':
        form=request.form
        user_name=form.get('user_name')
        user_password=form.get('user_password')
        userOperator.createUser(user_name,user_password)
        return redirect("/login")
    else:
        return render_template('signup.html')
        #注册页面

@app.route('/uploadElec',methods=['Post'])
def uploadElec():
    form = request.form 
    userId = form.get('userId')
    amount = form.get('amount')
    if globalCookie == request.cookies.get('session_id'):
        etherUtil.uploadElec(int(userId),int(amount))
        return redirect('/')
    else:
        return "没有权限上传"
if __name__=="__main__":
    app.run(host='0.0.0.0',threaded=True,debug=True,port=8080)


