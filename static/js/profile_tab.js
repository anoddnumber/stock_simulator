(function($) {
    $.ProfileTab = function(options) {
        var profileTab = {
             options : $.extend({
             }, options),

             updatePage : function(userData) {
                var oldTable = $('#profile_table').dataTable();
                oldTable.fnDestroy();

                var tableBody = $("#profile_table tbody")[0]; //grab the DOM element (0 indexed element of a jQuery object)
                tableBody.innerHTML = "";

                var keys = Object.keys(userData.stocks_owned);
                for (var i = 0; i < keys.length; i++) {
                    var symbol = keys[i];
                    var symbolData = userData.stocks_owned[symbol];
                    var pricesBought = Object.keys(symbolData);
                    var totalPriceBought = 0;
                    var totalQuantity = 0;
                    for (var j = 0; j < pricesBought.length; j++) {
                        var price = pricesBought[j];
                        var quantity = Number(symbolData[price]);
                        price = price.replace("_", ".");
                        price = Number(price);

                        totalPriceBought += price * quantity;
                        totalQuantity += quantity;
                    }
                    var symbolInfo = stockSymbolsMap[symbol];
                    var avgPrice = (totalPriceBought / totalQuantity).toFixed(2);
                    var currentPrice = symbolInfo.price;
                    var priceDifference = (currentPrice - avgPrice).toFixed(2);
                    var percentDifference = Utility.getPercentDifference(avgPrice, currentPrice).toFixed(2);
                    var dayPriceDifference = symbolInfo.daily_price_change;
                    var dayPercentDifference = symbolInfo.daily_percent_change;
                    var currentTotalValue = (totalQuantity * currentPrice).toFixed(2);

                    var row = [symbol, totalQuantity, avgPrice, currentPrice, priceDifference, percentDifference,
                    dayPriceDifference, dayPercentDifference, currentTotalValue]

                    Utility.insertRowByValues("profile_table tbody", row);
                }
                $('#profile_table').DataTable();
            },

            search : function() {

            },
         }
         return {
            update : profileTab.updatePage,
        };
    }


})(jQuery);
var ProfileTab = $.ProfileTab();


$( document ).ready(function() {
    /**
     * Finds out which stocks/stock names have matches with the searched value.
     * Then displays those stocks with the queried stock information.
     */
    $("#profileSearchBar").keyup(function() {
        ProfileTab.search();
    });

    /**
     * Do nothing when the searchProfileForm is submitted.
     * Searching should be done on the keyup event.
     */
    $('#searchProfileForm').submit(function(event) {
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });

//    $("#symbol-column-link").click(function(e) {
//        e.preventDefault();
//        var sortedArray = browseTabTableSortManager.sort($('#symbol-column-link').text(), function(a, b) {
//            return a.stock_symbol.localeCompare(b.stock_symbol);
//        });
//        BrowseTab.displaySortedArray(sortedArray);
//    })
//
//    $("#name-column-link").click(function(e) {
//        e.preventDefault();
//        var sortedArray = browseTabTableSortManager.sort($('#name-column-link').text(), function(a, b) {
//            return a.stock_info.name.localeCompare(b.stock_info.name);
//        });
//        BrowseTab.displaySortedArray(sortedArray);
//    })
//
//    $("#stock-column-link").click(function(e) {
//        e.preventDefault();
//        var sortedArray = browseTabTableSortManager.sort($('#stock-column-link').text(), function(a, b) {
//            return a.stock_info.price - b.stock_info.price;
//        });
//        BrowseTab.displaySortedArray(sortedArray);
//    })
});