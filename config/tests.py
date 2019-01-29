# from django.test import TestCase
from ethereum import ethereumUtil
# Create your tests here.
if __name__ == "__main__":
    coinbase_password = "123456"
    sellerId = 798457409
    buyerId = 654321
    buyerAddress = "0xdc30f5c10f35807f08d6a82bdb9d3b15ab2a23b8"
    buyerPassword = "123456" 
    sellerAddress = "0xa13def3dfefa8dc8773dc2aaa155d203d5af8493"
    admin = "0xa13def3dfefa8dc8773dc2aaa155d203d5af8493"
    ethUtil = ethereumUtil()

    #set admin
    # ethUtil.setAdmin(admin)

    #upload elec
    ethUtil.uploadElec(sellerId,1000)
    
    #get electricity amount
    print("卖家电量余额%d",ethUtil.getElectricityAmount(sellerId))
    print("买家电量余额%d",ethUtil.getElectricityAmount(buyerId))

    #出售委托
    price = 4
    sellAmount = 54
    for index in range(5):
        ethUtil.announceSell(sellerId,sellAmount,price)


    #获取委托的订单
    print("出售的电量列表%s",ethUtil.getSellingElec(sellerId))

 
    #获取coin balance

    print("买家代币余额%d",ethUtil.getCoinBalance(buyerAddress))
    print("卖家代币余额%d",ethUtil.getCoinBalance(sellerAddress))


    #购买电力
    
    index = 0 #第一个委托
    amount = 2 #买两度电
    # ethUtil.buyElectricity(buyerAddress,buyerPassword,buyerId,sellerId,index,amount)