var config = {
    numMinutesToUpdate : 5,
};

/**
* This defines an anonymous function that is executed right away with jQuery as the argument.
*/
(function($) {
    $.BrowseTab = function(options) {
        var buttonSymbols = new Array(); //TODO will be removed later...
        var table;

        var browseTab = {
            options : $.extend({
            }, options),

            /**
             * Displays all of the given stock symbols in a paginated view.
             *
             * stockSymbols - an array of stock symbols (that are strings)
             */
            displayStocks : function(stockSymbols) {
                var oldTable = $('#stocks_table').dataTable();
                oldTable.fnDestroy();

                var tableBody = $('#stocks_table tbody')[0]; //grab the DOM element (0 indexed element of a jQuery object)
                tableBody.innerHTML = "";

                var rows = browseTab.buildTable(stockSymbols);
                Utility.insertEntireTableBody($('#stocks_table tbody')[0], rows);

                for (var i = 0; i < buttonSymbols.length; i++) {
                    var symbol = buttonSymbols[i];
                    browseTab.enableButton(symbol);
                }

                table = $('#stocks_table').DataTable();
            },

            getTable : function() {
                return table;
            },

            enableButton: function(symbol) {
                var buttonId = 'buy' + symbol + 'Button';
                //add the on click event after inserting the button into the table
                $( "#stocks_table #" + buttonId ).on( "click", function() {
                    browseTab.previewBuyStock(symbol);
                });
            },

            /**
            *   Builds the stocks table and returns the rows in a 2d array
            *   where each array represents a row in the table.
            *
            *   symbols - an array of stock symbols
            */
            buildTable : function(symbols) {
                var rows = new Array();
                for (var i = 0; i < symbols.length; i++) {
                    var symbol = symbols[i];

                    var info = stockSymbolsMap[symbol];
                    var name = info['name'];
                    var dailyPercentChange = info.daily_percent_change;
                    var dailyPriceChange = info.daily_price_change;
                    var price = info.price;

                    var buttonId = 'buy' + symbol + 'Button';
                    buttonSymbols.push(symbol);
                    var buyButton = '<button id="' + buttonId + '" type="button">Buy</button>';

                    var row = [symbol, name, dailyPercentChange, dailyPriceChange, price, buyButton];
                    rows.push(row);
                }
                
                return rows;
            },

            previewBuyStock : function(symbol) {
                $('#previewBuyStockCash').text('$' + userInfo.cash);
                $('#previewBuyStockSymolName').text(symbol);
                $('#previewBuyStockPrice').text(stockSymbolsMap[symbol].price);
            },

            //TODO: add an update method for the browseTab
        }

        return {
            displayStocks : browseTab.displayStocks,
            displaySortedArray : browseTab.displaySortedArray,
            getTable : browseTab.getTable,
        };
    };
})(jQuery);

var BrowseTab = $.BrowseTab();

$( document ).ready(function() {
    ApiClient.updateCache(function() {
        ApiClient.updateUserData();
    });

    /**
     * Computes the total amount of money required to buy the number of stocks
     */
    $("#previewBuyStockQuantity").keyup(function() {
        var value = $('#previewBuyStockBox input[name=quantitybar]').val().trim();
        var stockSymbol = $("#previewBuyStockSymolName").html();
        var stockPrice = stockSymbolsMap[stockSymbol].price;
        var quantity = Utility.isPositiveInteger(value);
        if (quantity && stockPrice) {
            var totalPrice = quantity * stockPrice;
            $('#previewBuyStockBox #previewBuyStockTotalPrice').text('$' + totalPrice.toFixed(2));
        } else {
            $('#previewBuyStockBox #previewBuyStockTotalPrice').text("Please input a positive integer");
        }
    });

    $('#previewBuyStocksBuyButton').click(function() {
        var value = $('#previewBuyStockBox input[name=quantitybar]').val().trim();
        quantity = Utility.isPositiveInteger(value);
        if (quantity) {
            ApiClient.buyStock($("#previewBuyStockSymolName").html(), quantity);
        }
    });

    $('#stocks_table tbody').on('click', 'tr', function(event) {
        table = BrowseTab.getTable();
        var data = table.row( this ).data();
        var symbol = data[0];

        StockInfoPage.populatePage(symbol, '#stocks');

        $('#stockTableContainer').hide();
        $('#stocks .stockInfoPage').show();
    })

    $('#stocks .stockInfoPageBackButton').click(function() {
        $('#stockTableContainer').show();
        $('#stocks .stockInfoPage').hide();
    })

    StockInfoPage.setupButtons('#stocks');
});





