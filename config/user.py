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
    def existSuchUser(self, userName,userPassword):
        self.sql.connect()
        command = 'select password from user where userName = "%s" ' %userName
        result = self.sql.extractSql(command)
        print(result[0][0])
        if result[0][0] == userPassword:
            print("in true")
            return True
        else:
            return False
    def createUser(self,userName,password):
        id = random.randrange(100000000,999999999)
        address = self.ethUtil.createAddress(password)
        self.sql.connect()
        command = 'insert into user (id,userName,password,address) values ("%s","%s","%s","%s")' % (id,userName,password,address)
        self.sql.extractSql(command)
    def getUser(self,userName,password):
        self.sql.connect()
        command = 'select id,address from user where userName = "%s" && password = "%s"'  % (userName,password)
        return self.sql.extractSql(command)


 