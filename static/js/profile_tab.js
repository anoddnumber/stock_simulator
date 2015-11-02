(function($) {
    $.ProfileTab = function(options) {
        var profileTab = {
             options : $.extend({
             }, options),

             updatePage : function(userData) {
                var table = $("#profile_table")[0]; //grab the DOM element (0 indexed element of a jQuery object)
                table.innerHTML = "";

                Utility.insertRowByValues("profile_table", ["Symbol", "Amount Owned", "Price Bought", "Current Price",
                "Price Difference", "Percent Difference", "Day Price Difference", "Day Percent Difference", "Buy",
                "Sell"]);
                var keys = Object.keys(userData.stocks_owned);

                for (var i = 0; i < keys.length; i++) {
                    var symbol = keys[i];
                    var symbolData = userData.stocks_owned[symbol];
                    var pricesBought = Object.keys(symbolData);
                    var totalPrice = 0;
                    var totalQuantity = 0;

                    for (var j = 0; j < pricesBought.length; j++) {
                        var price = pricesBought[j];
                        var quantity = Number(symbolData[price]);
                        price = price.replace("_", ".");
                        price = Number(price);

                        totalPrice += price * quantity;
                        totalQuantity += quantity;
                    }

                    var avgPrice = (totalPrice / totalQuantity).toFixed(2);
                    var currentPrice = stockSymbolsMap[symbol].price;
                    var priceDifference = (currentPrice - avgPrice).toFixed(2);
                    var percentDifference = Utility.getPercentDifference(avgPrice, currentPrice).toFixed(2);
                    var dayPriceDifference; //TODO
                    var dayPercentDifference; //TODO

                    var row = [symbol, totalQuantity, avgPrice, currentPrice, priceDifference, percentDifference];

                    Utility.insertRowByValues("profile_table", row);
                }
            }
         }
         return {
            update : profileTab.updatePage,
        };
    }


})(jQuery);
var ProfileTab = $.ProfileTab();