(function($) {
    $.ProfileTab = function(options) {
        var table;

        var profileTab = {
             options : $.extend({
             }, options),

             updatePage : function(userData) {
                $('#stockInfoPageTotalCash').text(userData.cash);
                profileTab.updateTable(userData);
            },

            updateTable : function(userData) {
                //dataTable is using the old API, may need to look into if there is a newer way to do this
                var oldTable = $('#profile_table').dataTable();
                oldTable.fnDestroy();

                var tableBody = $("#profile_table tbody")[0]; //grab the DOM element (0 indexed element of a jQuery object)
                tableBody.innerHTML = "";

                var rows = profileTab.buildTable(userData);
                Utility.insertEntireTableBody($('#profile_table tbody')[0], rows);

                table = $('#profile_table').DataTable();
            },

            getTable : function() {
                return table;
            },

            /**
            *   Builds the profile table and returns the rows in a 2d array
            *   where each array represents a row in the table.
            *
            *   userData - an object containing user data
            */
            buildTable : function(userData) {
                if (userData == undefined || userData.stocks_owned == undefined) return [];

                var rows = new Array();

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
                    totalPriceBought = totalPriceBought.toFixed(2);
                    var currentTotalValue = (totalQuantity * currentPrice).toFixed(2);

                    var row = [symbol, totalQuantity, avgPrice, currentPrice, priceDifference, percentDifference,
                    dayPriceDifference, dayPercentDifference, totalPriceBought, currentTotalValue]
                    rows.push(row);
                }

                return rows;
            },
         }
         return {
            update : profileTab.updatePage,
            getTable : profileTab.getTable,
        };
    }


})(jQuery);
var ProfileTab = $.ProfileTab();


$( document ).ready(function() {
    $('#profile_table tbody').on('click', 'tr', function(event) {
        table = ProfileTab.getTable();
        var data = table.row( this ).data();
        var symbol = data[0];
//        var amountOwned = data[1];
//        var priceBought = data[2];
        var currentPrice = data[3];
//        var priceDifference = data[4];
//        var dayPriceDifference = data[5];
//        var investment = data[6];
//        var totalValue = data[7];

        $('#stockInfoPageStockSymbolName').text(symbol);

        var stockInfo = userInfo.stocks_owned[symbol];
        var totalNumOfStock = 0;
        for(var key in stockInfo) {
            var value = stockInfo[key];
            totalNumOfStock += value;
        }
        $('#stockInfoPageAmountOwned').text(totalNumOfStock);


        $('#stockInfoPageStockPrice').text(currentPrice);

        $('#profileTableContainer').hide();
        $('#stockInfoPage').show();
        $('#stockInfoPageBackButton').click(function() {
            $('#profileTableContainer').show();
            $('#stockInfoPage').hide();
        })
    })
});