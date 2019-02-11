# -*- coding:utf-8 -*-
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time 
import threading

class ethereumUtil(object):
    def __init__(self):
        self.web3 = Web3(HTTPProvider('http://localhost:8545'))
        self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
        assert self.web3.isConnected(),'connect fail 请打开geth'
        self.ourAddress = self.web3.eth.accounts[0]
        self.ourPassword = "123456"
        self.contractAddress = self.web3.toChecksumAddress("0xae2eef917384db30f1e186eb9fa8fb27f50691fe")
        self.abi = '[{"constant":false,"inputs":[{"name":"userName","type":"uint256"}],"name":"addUser","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"userId","type":"uint256"},{"name":"value","type":"uint256"},{"name":"price","type":"uint256"}],"name":"announceSell","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"},{"name":"_extraData","type":"bytes"}],"name":"approveAndCall","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"user","type":"address"},{"name":"amount","type":"uint256"}],"name":"award","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_value","type":"uint256"}],"name":"burn","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_value","type":"uint256"}],"name":"burnFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"buy","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"buyserId","type":"uint256"},{"name":"sellerId","type":"uint256"},{"name":"index","type":"uint256"},{"name":"value","type":"uint256"}],"name":"buyElec","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"},{"name":"freeze","type":"bool"}],"name":"freezeAccount","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"},{"name":"lockAmount","type":"uint256"},{"name":"lockPeriod","type":"uint256"}],"name":"lockToken","outputs":[{"name":"res","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"},{"name":"mintedAmount","type":"uint256"}],"name":"mintToken","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"target","type":"address"},{"name":"amount","type":"uint256"}],"name":"ownerUnlock","outputs":[{"name":"res","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"violator","type":"address"},{"name":"victim","type":"address"},{"name":"amount","type":"uint256"}],"name":"punish","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"sell","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"admin","type":"address"}],"name":"setAdmin","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newSellPrice","type":"uint256"},{"name":"newBuyPrice","type":"uint256"}],"name":"setPrices","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"uint256"},{"name":"_to","type":"uint256"},{"name":"_value","type":"uint256"}],"name":"transferElec","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"to","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"Award","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"target","type":"address"},{"indexed":false,"name":"frozen","type":"bool"}],"name":"FrozenFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"from","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"OwnerUnlock","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"target","type":"address"},{"indexed":false,"name":"amount","type":"uint256"},{"indexed":false,"name":"lockPeriod","type":"uint256"}],"name":"LockToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"violator","type":"address"},{"indexed":false,"name":"victim","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"Punish","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"uint256"},{"indexed":true,"name":"to","type":"uint256"},{"indexed":false,"name":"value","type":"uint256"}],"name":"TransferElec","type":"event"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_recivers","type":"address[]"},{"name":"_values","type":"uint256[]"}],"name":"transferMultiAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"initialSupply","type":"uint256"},{"name":"tokenName","type":"string"},{"name":"tokenSymbol","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"name":"userId","type":"uint256"},{"name":"amount","type":"uint256"}],"name":"uploadElec","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"announceCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"balance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"buyPrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"frozenAccount","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getSellingOwner","outputs":[{"name":"res","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isAdmin","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"isUser","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"lockedAmount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"name":"sellingElec","outputs":[{"name":"value","type":"uint256"},{"name":"price","type":"uint256"},{"name":"payAddress","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"sellingsOwner","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"sellPrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
        
        self.contract=self.getContract()
        
    def getContract(self):
        contract = self.web3.eth.contract(address=self.contractAddress, abi=self.abi)
        return contract

    def setAdmin(self,rawAddress):
        address = self.web3.toChecksumAddress(rawAddress)
        unlockResult = self.web3.personal.unlockAccount(self.ourAddress, self.ourPassword)
        if (unlockResult):
            hash = self.contract.functions.setAdmin(address).transact({'from': self.ourAddress})
            if (hash):
                print("设置管理员 "+rawAddress+" 交易发起成功hash值是" + self.web3.toHex(hash))
                self.web3.personal.lockAccount(self.ourAddress)
    def uploadElec(self,userId,amount):
        unlockResult = self.web3.personal.unlockAccount(self.ourAddress, self.ourPassword)
        if (unlockResult):
            hash = self.contract.functions.uploadElec(userId,amount).transact({'from': self.ourAddress})
            if (hash):
                print("上传电力信息交易发起成功hash值是" + self.web3.toHex(hash))
                self.web3.personal.lockAccount(self.ourAddress)
    
    def announceSell(self,userId,value,price):
        if (value > self.getElectricityAmount(userId)):
            print("委托数量大于账户余额")
            return
        unlockResult = self.web3.personal.unlockAccount(self.ourAddress, self.ourPassword)
        if (unlockResult):
            hash = self.contract.functions.announceSell(userId,value,price).transact({'from': self.ourAddress})
            if (hash):
                print("卖家委托交易发起成功hash值是" + self.web3.toHex(hash))
                self.web3.personal.lockAccount(self.ourAddress)

    def buyElectricity(self,rawBuyerAddress,buyerPassword,buyerId,sellerId,index,amount):
        buyerAddress = self.web3.toChecksumAddress(rawBuyerAddress)
        if (amount > self.getSellingElec(sellerId)[index][0] or self.getCoinBalance(buyerAddress) < self.getSellingElec(sellerId)[index][1]*amount):
            print("币余额不足或欲购买数量超出出售数量")
            return
        unlockResult = self.web3.personal.unlockAccount(buyerAddress, buyerPassword)
        if (unlockResult):
            hash = self.contract.functions.buyElec(buyerId,sellerId,index,amount).transact({'from': buyerAddress})
            if (hash):
                print("购买交易发起成功hash值是" + self.web3.toHex(hash))
                self.web3.personal.lockAccount(self.ourAddress)
        else:
            print("解锁失败")
    def getAnnounceLength(self,userId):
        return self.contract.functions.announceCount(userId).call()
    
    
    def getSellingElec(self,userId):
        length = self.getAnnounceLength(userId)
        sellingElec = []
        for index in range(length):
            sellingElec.append(self.contract.functions.sellingElec(userId,index).call())
        return sellingElec    

    def getElectricityAmount(self,userId):
        return self.contract.functions.balance(userId).call()
    def getCoinBalance(self,rawAddress):
        address = self.web3.toChecksumAddress(rawAddress)
        return self.contract.functions.balanceOf(address).call()    
    def createAddress(self,password):
        return self.web3.personal.newAccount(password)
    def getUsers(self,index):
        return self.contract.functions.sellingsOwner(index).call()
    def getUsersAmount(self):
        return self.contract.functions.getSellingOwner().call()

    def getSellingDetail(self):
        #获得每个用户的id
        userIds = []
        sellingDetail = {}
        for index in range(self.getUsersAmount()):
            userIds.append(self.getUsers(index))
        #根据id获得委托订单
        for index in  range(len(userIds)):
            userId=userIds[index]
            sellingDetail[userId]=self.getSellingElec(userId)
        return sellingDetail


class waitingUpload(threading.Thread):
    def __init__(self,Ethereum,hash,index,callback):
        threading.Thread.__init__(self)
        self.hash=hash
        self.index=index
        self.geth=Ethereum
        self.callback=callback
    def run(self): 
        self.geth.watingMined(self.hash,index=self.index,callback=self.callback)
