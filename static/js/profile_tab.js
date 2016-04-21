(function($) {
    $.ProfileTab = function(options) {
        var table;

        var profileTab = {
            options : $.extend({
            }, options),

            updatePage : function() {
                if (table) {
                    var numRows = Object.keys(userInfo.stocks_owned).length;
                    if (numRows != table.rows().count()) {
                        profileTab.createTable();
                    } else {
                        profileTab.updateTable();
                    }
                } else {
                    profileTab.createTable();
                }
            },

            //TODO probably a better way to do this with DataTables
            createTable : function() {
                table = $('#profile_table').DataTable();
                table.clear();

                var rows = profileTab.buildTable();
                table.rows.add(rows);
                table.draw(true);
            },

            updateTable : function() {
                table.rows().every( function () {
                    var d = this.data();

                    d.counter++; // update data source for the row

                    this.invalidate(); // invalidate the data DataTables has cached for this row
                    var symbol = d[0];
                    //TODO: some reason the table redraws on "this.data(row data here)" as well
                    //Seems like a datatable bug. Should only be redrawing on table.draw(false);
                    this.data(profileTab.getRow(symbol));
                } );

                table.draw(false);
            },

            getRow : function(symbol) {
                    var symbolData = userInfo.stocks_owned[symbol];
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

                    return row;
            },

            getTable : function() {
                return table;
            },

            /**
            *   Builds the profile table and returns the rows in a 2d array
            *   where each array represents a row in the table.
            */
            buildTable : function() {
                var rows = new Array();

                var keys = Object.keys(userInfo.stocks_owned);
                for (var i = 0; i < keys.length; i++) {
                    var symbol = keys[i];
                    var row = profileTab.getRow(symbol);
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
    var profileTableContainer = $.MutuallyExclusiveContainer({
        'selectors' : ['#profileTableContainer', '#profile .stockInfoPage']
    });

    $('#profile_table').DataTable({
        "lengthChange" : false,
        language: {
            search: "_INPUT_", //Don't display any label left of the search box
            searchPlaceholder: "  Search"
        }
    });

    $('#profile_table tbody').on('click', 'tr', function(event) {
        table = ProfileTab.getTable();
        var data = table.row( this ).data();
        if (! data) {
            return;
        }

        var symbol = data[0];

        StockInfoPage.populatePage(symbol, '#profile');
        profileTableContainer.show('#profile .stockInfoPage');
    })

    $('#profile .stockInfoPageBackButton').click(function() {
        profileTableContainer.show('#profileTableContainer');
    })

    StockInfoPage.setupButtons('#profile');
});