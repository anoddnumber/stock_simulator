(function($) {
    $.StockInfoPage = function(options) {
        var stockInfoPage = {
             options : $.extend({
             }, options),

             populatePage : function(symbol, parent) {
                $(parent + ' .stockInfoPageStockSymbolName').text(symbol);

                var stockInfo = userInfo.stocks_owned[symbol];
                var totalNumOfStock = 0;
                for(var key in stockInfo) {
                    var value = stockInfo[key];
                    totalNumOfStock += value;
                }
                $(parent + ' .stockInfoPageAmountOwned').text(totalNumOfStock);

                var currentPrice = stockSymbolsMap[symbol].price;
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