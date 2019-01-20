# -*- coding:utf-8 -*-
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time 
import threading

class ethereumUtil(object):
    def __init__(self,coinbase_password,contractAddress,contractAbi):
        self.web3 = Web3(HTTPProvider('http://localhost:8545'))
        self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
        assert self.web3.isConnected(),'connect fail 请打开geth'
        self.ourAddress = self.web3.eth.accounts[0]
        self.ourPassword = coinbase_password
        self.contractAddress = self.web3.toChecksumAddress(contractAddress)
        self.abi=contractAbi
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

class waitingUpload(threading.Thread):
    def __init__(self,Ethereum,hash,index,callback):
        threading.Thread.__init__(self)
        self.hash=hash
        self.index=index
        self.geth=Ethereum
        self.callback=callback
    def run(self): 
        self.geth.watingMined(self.hash,index=self.index,callback=self.callback)

