var config = {
    numStocksPerPage : 10,
    numMinutesToUpdate : 5,
};

/**
* This defines an anonymous function that is executed right away with jQuery as the argument.
*/
(function($) {
    $.BrowseTab = function(options) {
        var browseTab = {
            options : $.extend({
            }, options),

            /**
             * Displays all of the given stock symbols in a paginated view.
             * Meaning that the first n stocks will appear on the first page where n is config.numStocksPerPage
             * The other stocks will be displayed on the following pages when the user presses the next button.
             * Updates the Previous and Next buttons at the end.
             *
             * stockSymbols - an array of stock symbols (that are strings)
             */
            displayStocks : function(stockSymbols) {
                var oldTable = $('#stocks_table').dataTable();
                oldTable.fnDestroy();

                var tableBody = $('#stocks_table tbody')[0]; //grab the DOM element (0 indexed element of a jQuery object)
                tableBody.innerHTML = "";
                browseTab.insertRowsBySymbols(stockSymbols);

                $('#stocks_table').DataTable();
            },

             /**
             * Inserts multiple rows of stock information into the stocks table.
             *
             * symbols - an array of stock symbols (that are strings)
             */
            insertRowsBySymbols : function(symbols) {
                for (var i = 0; i < symbols.length; i++) {
                    browseTab.insertRowBySymbol(symbols[i]);
                }
            },

            /**
             * Inserts the symbol's values into the stocks table.
             * This includes the stock's Symbol, Name, and Price
             *
             * symbol - the symbol to get information from (i.e. AMZN)
             */
            insertRowBySymbol : function(symbol) {
                var info = stockSymbolsMap[symbol];
                var name = info['name'];
                var dailyPercentChange = info.daily_percent_change;
                var dailyPriceChange = info.daily_price_change;
                var price = info.price;
                var buttonId = 'buy' + symbol + 'Button';
                var buyButton = '<button id="' + buttonId + '" type="button">Buy</button>';

                Utility.insertRowByValues('stocks_table tbody', [symbol, name, dailyPercentChange, dailyPriceChange,
                 price, buyButton]);

                //add the on click event after inserting the button into the table
                $( "#stocks_table #" + buttonId ).on( "click", function() {
                    browseTab.previewBuyStock(symbol);
                });
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
        };
    };
})(jQuery);


var BrowseTab = $.BrowseTab();

$( document ).ready(function() {
    ApiClient.updateCache();

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

    $('#example').DataTable();
});





