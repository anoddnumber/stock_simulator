(function($) {
    $.StockInfoPage = function(options) {
        var stockInfoPage = {
             options : $.extend({
             }, options),

             populatePage : function(symbol, parent) {
                $(parent + ' .stockInfoPageStockSymbolName').text("(" + symbol + ")");

                var userStockMap = userInfo.stocks_owned[symbol]; //shows what prices the user bought the stock at
                var totalNumOfStock = 0;
                if (userStockMap) {
                    totalNumOfStock = userStockMap.total;
                }
                var stockInfo = stockSymbolsMap[symbol];
                var stockName = stockInfo['name'];
                var stockPercentChange = stockInfo['daily_percent_change']
                var stockPriceChange = stockInfo['daily_price_change']
                var currentPrice = stockInfo['price'];
                var day_open = stockInfo.day_open;
                var day_high = stockInfo.day_high;
                var day_low = stockInfo.day_low;

                $(parent + ' .stockName').text(stockName);
                $(parent + ' .stockPercentChange').text(stockPercentChange);
                $(parent + ' .stockPriceChange').text(stockPriceChange);
                $(parent + ' .stockInfoPageAmountOwned').text(totalNumOfStock);
                $(parent + ' .stockInfoPageStockPrice').text(currentPrice);
                $(parent + ' .stockInfoPageDayOpen').text(day_open);
                $(parent + ' .stockInfoPageDayHigh').text(day_high);
                $(parent + ' .stockInfoPageDayLow').text(day_low);

                // by default, the buy radio button is selected
                // TODO refactor to make a "set slider bar max/min" function
                $(parent + ' .stockInfoPage input').attr({
                    "min" : 0,
                    "max" : Math.floor(userInfo.cash / currentPrice),
                });

                //make sure we don't stack up actions on the click event..
                $(parent + " input[name=market]").unbind("click");

                $(parent + " input[name=market]").click(function(){
                    var defaultValue = 0;
                    $(parent + ' .stockInfoPage input[name=amountRange]')[0].value = defaultValue;
                    $(parent + ' .stockInfoPage input[name=amountInput]')[0].value = defaultValue;

                    if ($(parent + ' .buyStockRadioButton').is(':checked')) {
                        // clicked the buy radio button

                        $(parent + ' .stockInfoPage input[name=amountRange]').attr({
                            "min" : 0,
                            "max" : Math.floor(userInfo.cash / currentPrice),
                        });
                    } else if ($(parent + ' .sellStockRadioButton').is(':checked')) {
                        // clicked the sell radio button

                        var maxAvailableToSell = 0;
                        if (userInfo.stocks_owned[symbol]) {
                            maxAvailableToSell = userInfo.stocks_owned[symbol].total
                        }

                        $(parent + ' .stockInfoPage input[name=amountRange]').attr({
                            "min" : 0,
                            "max" : maxAvailableToSell,
                        });

                    }
                });
            },

            setupButtons : function(parent) {
                $('.stockInfoPageStocksConfirmButton').click(function() {
                    var value = $('.stockInfoPage input[name=amountInput]').val().trim();

                    var price = $('.stockInfoPageStockPrice').text().trim();
                    quantity = Utility.isPositiveInteger(value);

                    if (quantity) {
                        var symbol = $(".stockInfoPageStockSymbolName").html().replace("(","").replace(")","");
                        if ($('.buyStockRadioButton').is(':checked')) {
                            ApiClient.buyStock(symbol, quantity, price, function(data) {
                                data = JSON.parse(data);

                                $('.stockInfoPageAmountOwned').text(data.stocks_owned[symbol].total);
                                $('.stockInfoPageTotalCash').text("Available Cash: $" + data.cash);
                            });
                        } else if ($('.sellStockRadioButton').is(':checked')) {
                            ApiClient.sellStock(symbol, quantity, price, function(data) {
                                data = JSON.parse(data);

                                if (data.stocks_owned[symbol]) {
                                    $('.stockInfoPageAmountOwned').text(data.stocks_owned[symbol].total);
                                } else {
                                    $('.stockInfoPageAmountOwned').text("0");
                                }

                                $('.stockInfoPageTotalCash').text("Available Cash: $" + data.cash);
                            });
                        } else {
                            console.log("nothing happened");
                            //TODO show error
                        }
                    } else {
                        //TODO show error
                    }

                });
            },

            init : function() {
                //nothing to do
                stockInfoPage.setupButtons();
            },
        };

        return {
            populatePage : stockInfoPage.populatePage,
            setupButtons : stockInfoPage.setupButtons,
            init : stockInfoPage.init,
        };
    }
})(jQuery);

var StockInfoPage = $.StockInfoPage();

$( document ).ready(function() {
    var url = window.location.href;
    if (url.indexOf("stock/") > -1) {
        StockInfoPage.init();
    }
});

function onStockQuantityInputChange(form, value) {
    form.amountRange.value = value.replace(/[^0-9]/g,'0');
    console.log("form: " + form);
//    console.log("form: " + $(form + " .stockInfoPageStockTotalPrice"));
//    form.totalPrice

    $('.stockInfoPageStockTotalPrice').text("abc");
}

function onStockQuantityBarChange(form, value) {
    form.amountInput.value=value
}