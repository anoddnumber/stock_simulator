(function($) {
    $.StockInfoPage = function(options) {
        var stockInfoPage = {
             options : $.extend({
             }, options),
        }

        return {
        };
    }
})(jQuery);

var StockInfoPage = $.StockInfoPage();

$( document ).ready(function() {
    $('#stockInfoPageStocksBuyButton').click(function() {
        var value = $('#stockInfoPage input[name=quantitybar]').val().trim();
        var price = $('#stockInfoPageStockPrice').text().trim();
        quantity = Utility.isPositiveInteger(value);
        if (quantity) {
            var symbol = $("#stockInfoPageStockSymbolName").html();
            ApiClient.buyStock($("#stockInfoPageStockSymbolName").html(), quantity, price);
        } else {
            //TODO show error
        }
    });

    $('#stockInfoPageStocksSellButton').click(function() {
        var value = $('#stockInfoPage input[name=quantitybar]').val().trim();
        var price = $('#stockInfoPageStockPrice').text().trim();
        quantity = Utility.isPositiveInteger(value);
        if (quantity) {
            var symbol = $("#stockInfoPageStockSymbolName").html();
            ApiClient.sellStock($("#stockInfoPageStockSymbolName").html(), quantity, price);
        } else {
            //TODO show error
        }
    });
});