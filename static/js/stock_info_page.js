(function($) {
    $.StockInfoPage = function(options) {
        var stockInfoPage = {
             options : $.extend({
             }, options),

             populatePage : function(symbol, parent) {
                $(parent + ' .stockInfoPageStockSymbolName').text("(" + symbol + ")");

                var userStockMap = userInfo.stocks_owned[symbol]; //shows what prices the user bought the stock at
                var totalNumOfStock = 0;
                var stockInfo = stockSymbolsMap[symbol];
                var stockName = stockInfo['name'];
                var stockPercentChange = stockInfo['daily_percent_change']
                var stockPriceChange = stockInfo['daily_price_change']
                var currentPrice = stockInfo['price'];
                var day_open = stockInfo.day_open;
                var day_high = stockInfo.day_high;
                var day_low = stockInfo.day_low;

                for (var key in userStockMap) {
                    var value = userStockMap[key];
                    totalNumOfStock += value;
                }
                
                $(parent + ' .stockName').text(stockName);
                $(parent + ' .stockPercentChange').text(stockPercentChange);
                $(parent + ' .stockPriceChange').text(stockPriceChange);
                $(parent + ' .stockInfoPageAmountOwned').text(totalNumOfStock);
                $(parent + ' .stockInfoPageStockPrice').text(currentPrice);
                $(parent + ' .stockInfoPageDayOpen').text(day_open);
                $(parent + ' .stockInfoPageDayHigh').text(day_high);
                $(parent + ' .stockInfoPageDayLow').text(day_low);
            },

            setupButtons : function(parent) {
                $(parent + ' .stockInfoPageStocksBuyButton').click(function() {
                    var value = $(parent + ' .stockInfoPage input[name=quantitybar]').val().trim();
                    var price = $(parent + ' .stockInfoPageStockPrice').text().trim();
                    quantity = Utility.isPositiveInteger(value);
                    if (quantity) {
                        var symbol = $(parent + " .stockInfoPageStockSymbolName").html().replace("(","").replace(")","");
                        ApiClient.buyStock(symbol, quantity, price);
                    } else {
                        //TODO show error
                    }
                });

                $(parent + ' .stockInfoPageStocksSellButton').click(function() {
                    var value = $(parent + ' .stockInfoPage input[name=quantitybar]').val().trim();
                    var price = $(parent + ' .stockInfoPageStockPrice').text().trim();
                    quantity = Utility.isPositiveInteger(value);
                    if (quantity) {
                        var symbol = $(parent + " .stockInfoPageStockSymbolName").html().replace("(","").replace(")","");
                        ApiClient.sellStock(symbol, quantity, price);
                    } else {
                        //TODO show error
                    }
                });
            }
        };

        return {
            populatePage : stockInfoPage.populatePage,
            setupButtons : stockInfoPage.setupButtons,
        };
    }
})(jQuery);

var StockInfoPage = $.StockInfoPage();

$( document ).ready(function() {
});