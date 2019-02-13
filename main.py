from flask import Flask, render_template, url_for, request, redirect, flash, request, session, make_response, jsonify
from config.sql import Sql
from pathlib import Path
from config.user import User
from config.ethereum import ethereumUtil
from ast import literal_eval
import os
import time
import datetime
import uuid
import _thread
import threading
app = Flask(__name__)
app.secret_key = bytes(str(uuid.uuid4()), 'utf-8')
uploadFloader = './static/upload'
app.config['UPLOAD_FLODER'] = uploadFloader
sql = Sql("localhost", 3306, 'root', 'domore0325', 'elec')
globalCookie = "ypisthebest"
userOperator = User()
etherUtil = ethereumUtil()


@app.route('/')
def index():
    sellingDetails = etherUtil.getSellingDetail()    
    return render_template('index.html', sellingDetails=sellingDetails)


@app.route('/personal')
def personal():
    sessionId =request.cookies.get('session_id')
    id = userOperator.getIdByCookie(sessionId)
    if id == "":
        return redirect('/login')
    else:
        user = userOperator.getUserById(id)
        return render_template("personal.html",user=user)
@app.route('/admin')
def admin():
    if globalCookie == request.cookies.get('session_id'):
        return render_template("admin.html")
    else:
        flash("管理员请先登录")
        return redirect('/login')


@app.route('/login', methods=['Post', 'GET'])
def signIn():
    if request.method == 'POST':
        form = request.form
        user_name = form.get('user_name')
        user_password = form.get('user_password')
        if userOperator.existSuchUser(user_name, user_password):
            if user_name == 'admin':
                response = make_response(redirect('/admin'))
                response.set_cookie('session_id', globalCookie)
                return response
            else:
                userInfo = userOperator.getUser(user_name, user_password)
                response = make_response(redirect(url_for('index')))
                userId = userInfo.get('id')
                print("userId %s" % (userId))
                temp = userOperator.getSessionId(userId)
                sessionId = ""
                if temp == "":
                    sessionId = str(uuid.uuid4())
                    userOperator.setSessionId(userId, sessionId)
                else:
                    sessionId = temp
                print("sessionId %s" % (sessionId))
                response.set_cookie('session_id', sessionId)
                return response

        else:
            flash("用户名密码不匹配")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/found/<user>/<sellingDetails>')
def found(user, sellingDetails):
    # print(request.cookies.get('session_id'))
    sellingDetails = literal_eval(sellingDetails)
    user = literal_eval(user)
    return render_template('index.html', user=user, sellingDetails=sellingDetails)


@app.route('/signup', methods=['Post', 'GET'])
def signUp():
    if request.method == 'POST':
        form = request.form
        user_name = form.get('user_name')
        user_password = form.get('user_password')
        userOperator.createUser(user_name, user_password)
        return redirect("/login")
    else:
        return render_template('signup.html')
        # 注册页面


@app.route('/uploadElec', methods=['Post'])
def uploadElec():
    form = request.form
    userId = form.get('userId')
    amount = form.get('amount')
    if globalCookie == request.cookies.get('session_id'):
        etherUtil.uploadElec(int(userId), int(amount))
        return redirect('/')
    else:
        return "没有权限上传"


@app.route('/api/userWhetherLogin', methods=['Post', 'GET'])
def test():
    if globalCookie == request.cookies.get('session_id'):
        return "1"
    else:
        return "0"


@app.route('/api/user/<sessionId>', methods=['GET'])
def getUserInfo(sessionId):
    id = userOperator.getIdByCookie(sessionId)
    userInfo = userOperator.getUserById(id)
    return jsonify(userInfo)


@app.route('/api/elect/transaction', methods=['Post'])
def transact():
    form = request.form
    buyerAddress = form.get('buyerAddress')
    buyerPassword = form.get('buyerPassword')
    buyerId = int(form.get('buyerId'))
    sellerId = int(form.get('sellerId'))
    index = int(form.get('index'))
    amount = int(form.get('amount'))
    print("%s %s %s　%s　%s　%s" %
          (buyerAddress, buyerPassword, buyerId, sellerId, index, amount))
    result = etherUtil.buyElectricity(buyerAddress, buyerPassword,
                             buyerId, sellerId, index, amount)
    # buyerAddress,buyerPassword,buyerId,sellerId,index,amount
    return jsonify(result)

@app.route('/api/elect/announce', methods=['Post'])
def announce():
    form = request.form 
    sellerId = int(form.get("sellerId"))
    sellAmount = int(form.get("sellAmount"))
    price = int(form.get("price"))
    address = form.get('address')
    result = etherUtil.announceSell(sellerId,sellAmount,price,address)
    return jsonify(result)
if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, debug=True, port=8080)
