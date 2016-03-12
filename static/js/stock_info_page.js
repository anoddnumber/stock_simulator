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

                for(var key in userStockMap) {
                    var value = userStockMap[key];
                    totalNumOfStock += value;
                }
                
                $(parent + ' .stockName').text(stockName);
                $(parent + ' .stockPercentChange').text(stockPercentChange);
                $(parent + ' .stockPriceChange').text(stockPriceChange);
                $(parent + ' .stockInfoPageAmountOwned').text(totalNumOfStock);
                $(parent + ' .stockInfoPageStockPrice').text(currentPrice);
            },

            setupButtons : function(parent) {
                $(parent + ' .stockInfoPageStocksBuyButton').click(function() {
                    var value = $(parent + ' .stockInfoPage input[name=quantitybar]').val().trim();
                    var price = $(parent + ' .stockInfoPageStockPrice').text().trim();
                    quantity = Utility.isPositiveInteger(value);
                    if (quantity) {
                        var symbol = $(parent + " .stockInfoPageStockSymbolName").html();
                        ApiClient.buyStock($(parent + " .stockInfoPageStockSymbolName").html(), quantity, price);
                    } else {
                        //TODO show error
                    }
                });

                $(parent + ' .stockInfoPageStocksSellButton').click(function() {
                    var value = $(parent + ' .stockInfoPage input[name=quantitybar]').val().trim();
                    var price = $(parent + ' .stockInfoPageStockPrice').text().trim();
                    quantity = Utility.isPositiveInteger(value);
                    if (quantity) {
                        var symbol = $(parent + " .stockInfoPageStockSymbolName").html();
                        ApiClient.sellStock($(parent + " .stockInfoPageStockSymbolName").html(), quantity, price);
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