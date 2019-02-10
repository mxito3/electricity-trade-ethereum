from config import sql,ethereum
from pathlib import Path
import os
import uuid
import random
uploadFloader='./static/upload'
class User(object):
    """docstring for videoCheck"""

    def __init__(self):
        self.sql=sql.Sql("localhost",3306,'root','domore0325','elec')
        self.ethUtil = ethereum.ethereumUtil()    # def checkExists(self):
    def existSuchUser(self, userName,password):
        self.sql.connect()
        command = 'select password from user where userName="%s" && password="%s" ' %(userName,password)
        result = self.sql.extractSql(command)
        if len(result) == 0:
            return False
        
        if result[0][0] == password:
            # print("in true")
            return True
        else:
            return False

    def createUser(self,userName,password):
        id = uuid.uuid4()
        elecId = random.randrange(100000000,999999999)
        address = self.ethUtil.createAddress(password)
        self.sql.connect()
        command = 'insert into user (id,elecId,userName,password,address) values ("%s","%s","%s","%s","%s")' % (id,elecId,userName,password,address)
        self.sql.extractSql(command)
    def getUser(self,userName,password):
        self.sql.connect()
        command = 'select id,elecId,address,userName from user where userName = "%s" && password = "%s"'  % (userName,password)
        return self.userSerialization(self.sql.extractSql(command))
    
    def getUserById(self,id):
        self.sql.connect()
        command = 'select id,elecId,address,userName from user where id = "%s"'  % (id)
        return self.userSerialization(self.sql.extractSql(command))
    
    def userSerialization(self,rawUser):
        userInfo = {}
        userInfo["id"] = rawUser[0][0]
        userInfo["elecId"] = int(rawUser[0][1])
        userInfo["address"] = rawUser[0][2]
        userInfo["userName"] = rawUser[0][3]
        userInfo["balance"] =  self.ethUtil.getElectricityAmount(userInfo["elecId"])
        userInfo["coinBalance"] = self.ethUtil.getCoinBalance(userInfo["address"])
        return userInfo
    def setSessionId(self,id,sessionId):
        self.sql.connect()
        command = 'insert into sessionId (id,sessionId) values ("%s","%s")' % (id,sessionId)
        self.sql.extractSql(command)

    def getSessionId(self,id):
        self.sql.connect()
        command = 'select  sessionId from sessionId where id="%s"'  % (id)
        result = self.sql.extractSql(command)
        if len(result)==0:
            return ""
        else:
            return result[0][0]
    def getIdByCookie(self,cookie):
        # print("in getIdByCookie")
        self.sql.connect()
        command = 'select id from sessionId where sessionId="%s"'  % (cookie)
        result = self.sql.extractSql(command)
        # print(cookie)
        # print(result)
        if len(result)==0:
            return ""
        else:
            return result[0][0]


 