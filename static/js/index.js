
$(document).ready(function($) {
    let buttonId,sellerId,amount ,price ,sellerAddress;
    $(".btn").click(function(){
        buttonId = $(this).attr("id");
        sellerId = $("#"+buttonId+1).attr("value");
        amount = $("#"+buttonId+2).attr("value");
        price = $("#"+buttonId+3).attr("value");
        sellerAddress = $("#"+buttonId+4).attr("value");
        console.log(buttonId);
        $(".mask").show();
        $(".bomb_box").show();
    })

    $('#buyButton').click(function (e) { 
        e.preventDefault();
        let cookie = $.cookie("session_id");
        // console.log(sellerId+"  "+amount+"  "+price+"  "+sellerAddress);
        if (cookie == undefined)
        {
            location.href = '/login';
        }
        else //有cookie，，获得用户信息
        {
            //输入量是不是大于卖家委托的
            let buyAmount = $("#buyAmount").val();
            // console.log(buyAmount);
            if(buyAmount>amount)
            {
                console.log("购买量超出卖家出售的总额"+amount);
            }
            else
            {
                //请求当前登录用户的数据
                url = "/api/user/"+cookie;
                $.get(url,function(data,status,xhr){
                    if(status == "success")
                    {
                        // $(".mask").hide();
                        // $(".bomb_box").hide();
                        //隐藏登录注册　显示用户信息
                        $('#userInfo').show();
                        $('#login').hide();
                        //发起交易        
                        console.log(data);
                        buyerAddress=data.address;
                        buyerPassword="domore0325";
                        buyerId=data.elecId;
                        let index=buttonId.split("-")[1]-1
                        let amount=buyAmount;
                        let buyInfo = {};
                        buyInfo.buyerAddress = buyerAddress;
                        buyInfo.buyerPassword= buyerPassword;
                        buyInfo.buyerId = buyerId;
                        buyInfo.sellerId =sellerId;
                        buyInfo.index=index;
                        buyInfo.amount=amount;
                        // let buyInfoJson = JSON.parse(buyInfo)
                        console.log(JSON.stringify(buyInfo))
                        let buyUrl = "/api/elect/transaction";
                        $.post(buyUrl,buyInfo,function(data,status,xhr){
                            if(status == "success")
                            {
                                $(".mask").hide();
                                $(".bomb_box").hide();
                                alert("购买交易成功发起,待成功后查看余额")
                                console.log("in post success"+data);
                            }
                            else
                            {
                                console.log("出错了");
                            }
                        },"json");
                      }
                    else
                    {
                        console.log("请求错误");
                    }
                })
            }
            //buy
            
        }
    });
});
