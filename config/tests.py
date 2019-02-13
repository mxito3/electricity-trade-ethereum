# from django.test import TestCase
from ethereum import ethereumUtil
# Create your tests here.
if __name__ == "__main__":
    coinbase_password = "123456"
    sellerId = 33232323
    buyerId = 654321
    buyerAddress = "0x8273fc3E21E561750C8765dd3659bFA7b639b25c"
    buyerPassword = "domore0325" 
    sellerAddress = "0x8273fc3E21E561750C8765dd3659bFA7b639b25c"
    admin = "0x0f4b5adb66461d185b646c6fe04c918a2b0c493b"
    ethUtil = ethereumUtil()

    #set admin
    # ethUtil.setAdmin(admin)

    #upload elec
    ethUtil.uploadElec(sellerId,1000)
    
    #get electricity amount
    print("卖家电量余额%d",ethUtil.getElectricityAmount(sellerId))
    print("买家电量余额%d",ethUtil.getElectricityAmount(buyerId))
    print("买家以太币余额不足%d"%(ethUtil.getEthBalance(buyerAddress)))
    #出售委托
    price = 4
    sellAmount = 77
    # for index in range(5):
    ethUtil.announceSell(sellerId,sellAmount,price,sellerAddress)

    #获取委托的订单
    # print("出售的电量列表%s",ethUtil.getSellingElec(sellerId))

 
    #获取coin balance

    print("买家代币余额%d",ethUtil.getCoinBalance(buyerAddress))
    print("卖家代币余额%d",ethUtil.getCoinBalance(sellerAddress))


    #购买电力
    
    # index = 0 #第一个委托
    # amount = 2 #买两度电
    # ethUtil.buyElectricity(buyerAddress,buyerPassword,buyerId,sellerId,index,amount)