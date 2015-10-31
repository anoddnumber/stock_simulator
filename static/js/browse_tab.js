var config = {
    numStocksPerPage : 10,
    numMinutesToUpdate : 5,
};

/**
* This defines an anonymous function that is executed right away with jQuery as the argument.
*/
(function($) {
    $.BrowseTab = function(options) {
        var curSymbols; //the symbols that should be shown
        var curPage = 0;
        var lastUpdatedDate; //last time the server's cache was updated

        var browseTab = {
            options : $.extend({
            }, options),

            getCurSymbols : function() {
                return curSymbols;
            },

            getCurPage : function() {
                return curPage;
            },

            getLastUpdatedDate : function() {
                return lastUpdatedDate;
            },

            search : function() {
                var query = $('#searchStocksForm input[name=searchbar]').val().trim();
                var regEx = new RegExp(query,'i'); //i flag to ignore case
                var keys = Object.keys(stockSymbolsMap);
                var keysToShow = [];

                keys.forEach(function(value, index, arr) {
                    var info = stockSymbolsMap[value];
                    var infoKeys = Object.keys(info);
                    var flag = false;

                    for (var i = 0; i < infoKeys.length; i++) {
                        if (info[infoKeys[i]].toString().match(regEx)) {
                            flag = true;
                            break;
                        }
                    }

                    if (flag === true || value.match(regEx)) {
                        keysToShow.push(value);
                    }
                });

                curPage = 0;
                browseTab.displayStocks(keysToShow);
            },

            showNextPage : function() {
                var lastPage = curSymbols.length/config.numStocksPerPage - 1;
                if (curPage < lastPage) {
                    curPage++;
                    browseTab.displayStocks(curSymbols);
                }
            },

            showPreviousPage : function() {
                var firstPage = 0;
                if (curPage > firstPage) {
                    curPage--;
                    browseTab.displayStocks(browseTab.getCurSymbols());
                }
            },

            /**
             * Stores a map of stock symbols (the keys) to an object with stock information .
             * Also updates the lastUpdatedDate variable.
             *
             * The object is as follows:
             * {
             *     'name' : *Stock Name*,
             *     'price': *Stock Price*
             * }
             * Updates the cache: TODO move to global area
             */
            updateCache : function() {
                $.ajax("/stockSymbolsMap", {
                    success : function(data) {
                        console.log("successfully got the stock symbols map!");
                        stockSymbolsMap = JSON.parse(data);
                        lastUpdatedDate = stockSymbolsMap['last_updated'];

                        var lastUpdatedTime = Date.parse(lastUpdatedDate);
                        var currentTime = Date.now();
                        var lenientTime = 2000; //give the server more time to update, in milliseconds
                        var numMillisecondsToUpdate = config.numMinutesToUpdate * 60 * 1000;
                        var delay = lenientTime + numMillisecondsToUpdate - (currentTime - lastUpdatedTime);


                        if (delay < 0) {
                            setTimeout(browseTab.updateCache, numMillisecondsToUpdate);
                        } else {
                            setTimeout(browseTab.updateCache, delay);
                        }

                        //the last_updated date should not be shown to the user
                        delete stockSymbolsMap['last_updated'];

                        //TODO: create a displayStocksHelper that takes in a list of symbols to display
                        //displayStocks will then have no parameters and defaults to curSymbols or Object.keys(stockSymbolsMap)
                        if ( ! curSymbols) {
                            browseTab.displayStocks(Object.keys(stockSymbolsMap));
                        } else {
                            browseTab.displayStocks(curSymbols);
                        }

                    },
                    error : function() {
                        console.log("error, did not get the stock symbols map");
                        //try again in a minute...
                        var numMillisecondsToUpdate = 60000;
                        setTimeout(browseTab.updateCache, numMillisecondsToUpdate);
                    }
                });
            },

            /**
             * Displays all of the given stock symbols in a paginated view.
             * Meaning that the first n stocks will appear on the first page where n is config.numStocksPerPage
             * The other stocks will be displayed on the following pages when the user presses the next button.
             * Updates the Previous and Next buttons at the end.
             *
             * stockSymbols - an array of stock symbols (that are strings)
             */
            displayStocks : function(stockSymbols) {
                var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
                var begin = curPage * config.numStocksPerPage;
                var end = (curPage + 1) * config.numStocksPerPage;
                var displayedKeys = stockSymbols.slice(begin, end);
                curSymbols = stockSymbols;
                table.innerHTML = "";
                if (displayedKeys.length > 0) {
                    Utility.insertRowByValues('stocks_table', ["Symbol", "Name", "Stock Price", "Buy"]);
                    browseTab.insertRowsBySymbols(displayedKeys);
                } else {
                    Utility.insertRowByValue('stocks_table', "Nothing found, please try again.");
                }

                browseTab.updateButtons();
            },

            /**
             * Hides/shows the Previous and Next buttons depending on if there are more pages to show to the left/right of the current page
             */
            updateButtons : function() {
                var firstPage = 0;
                var lastPage = curSymbols.length/config.numStocksPerPage - 1;
                if (firstPage === curPage) {
                    $('#previousStocksButton').hide();
                } else {
                    $('#previousStocksButton').show();
                }

                if (lastPage <= curPage) {
                    $('#nextStocksButton').hide();
                } else {
                    $('#nextStocksButton').show();
                }
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
                var price = info.price;
                var buttonId = 'buy' + symbol + 'Button';
                var buyButton = '<button id="' + buttonId + '" type="button">Buy</button>';

                Utility.insertRowByValues('stocks_table', [symbol, name, price, buyButton]);

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

            /**
             * TODO, create a central helper for all the APIs, or maybe a client.
             *  since all the success and error parts of the functions are the same..
             */
            buyStock : function(symbol, quantity) {
                $.ajax("/buyStock", {
                    method: "POST",
                    data: {'symbol' : symbol,
                            'quantity' : quantity,
                            'stockPrice' : stockSymbolsMap[symbol].price
                            },
                    success: function(data) {
                        console.log(data);
                        Utility.updateUserData();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("JSON.parse(jqXHR.responseText).message: " + jqXHR.responseText);
                        console.log("error, did not buy stock");
                    }
                });
            }
        }

        return {
            updateCache : browseTab.updateCache,
            getCurSymbols : browseTab.getCurSymbols,
            getCurPage : browseTab.getCurPage,
            getLastUpdatedDate : browseTab.getLastUpdatedDate,
            buyStock : browseTab.buyStock,
            showPreviousPage : browseTab.showPreviousPage,
            showNextPage : browseTab.showNextPage,
            search : browseTab.search,
        };
    };
})(jQuery);


var BrowseTab = $.BrowseTab();
$( document ).ready(function() {

    BrowseTab.updateCache();

    /**
     * Moves to and displays the previous page of stocks.
     */
    $('#previousStocksButton').click(function() {
        BrowseTab.showPreviousPage();
    });

    /**
     * Moves to and displays the next page of stocks.
     */
    $('#nextStocksButton').click(function() {
        BrowseTab.showNextPage();
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
            BrowseTab.buyStock($("#previewBuyStockSymolName").html(), quantity);
        }
    });

    /**
     * Finds out which stocks/stock names have matches with the searched value.
     * Then displays those stocks with the queried stock information.
     */
    $("#stockSearchBar").keyup(function() {
        BrowseTab.search();
    });

    /**
     * Do nothing when the searchStocksForm is submitted.
     * Searching should be done on the keyup event.
     */
    $('#searchStocksForm').submit(function(event) {
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });
});





