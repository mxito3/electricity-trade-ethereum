$(document).ready(function ($) {
    $("#announce").click(function (e) {
        e.preventDefault();
        $(".mask").show();
        $(".bomb_box").show();
    })
    $("#sellButton").click(function (e) {
        e.preventDefault();
        sellerId = parseInt($("#sellerId").attr("value"));
        sellAmount = parseInt($("#sellAmount").val());
        price = parseInt($("#price").val());
        address = $("#address").attr("value");
        console.log(address)
        if (sellAmount == NaN || price == NaN) {
            alert("只能填入数字");
            return
        }
        else {
            console.log(sellerId + "   " + sellAmount + "  " + price);
            sellInfo = {}
            sellInfo.sellerId = sellerId
            sellInfo.sellAmount = sellAmount
            sellInfo.price = price
            sellInfo.address = address
            let buyUrl = "/api/elect/announce";
            $.post(buyUrl, sellInfo, function (data, status, xhr) {
                if (status == "success") {
                    $(".mask").hide();
                    $(".bomb_box").hide();
                    if (data == true) {
                        alert("售卖交易成功发起,请稍后刷新首页")
                    }
                    else {
                        alert("欲出售数量大于电力余额");
                    }
                }
                else {
                    console.log("出错了");
                }
            }, "json");
        }
    });
});