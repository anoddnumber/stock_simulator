var config = {
    numStocksPerPage : 10,
    numMinutesToUpdate : 5,
};
    
$( document ).ready(function() {
    var stockSymbolsMap;
    var curSymbols; //the symbols that should be shown 
    var curPage = 0;
    var lastUpdatedDate; //last time the server's cache was updated
    
    updateCache();
    
    /**
     * Stores a map of stock symbols (the keys) to an object with stock information .
     * Also updates the lastUpdatedDate variable.
     * 
     * The object is as follows: 
     * {
     *     'name' : *Stock Name*,
     *     'price': *Stock Price*
     * }
     */
    function updateCache() {
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
                    setTimeout(updateCache, numMillisecondsToUpdate);
                } else {
                    setTimeout(updateCache, delay);
                }
                
                //the last_updated date should not be shown to the user
                delete stockSymbolsMap['last_updated'];
                
                if ( ! curSymbols) {
                    displayStocks(Object.keys(stockSymbolsMap));
                } else {
                    displayStocks(curSymbols);
                }
                
            },
            error : function() {
                console.log("error, did not get the stock symbols map");
                //try again in a minute...
                var numMillisecondsToUpdate = 60000;
                setTimeout(updateCache, numMillisecondsToUpdate);
            }
        });
    }
    
    /**
     * Displays all of the given stock symbols in a paginated view.
     * Meaning that the first n stocks will appear on the first page where n is config.numStocksPerPage
     * The other stocks will be displayed on the following pages when the user presses the next button.
     * Updates the Previous and Next buttons at the end.
     * 
     * stockSymbols - an array of stock symbols (that are strings)
     */
    function displayStocks(stockSymbols) {
        var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
        var begin = curPage * config.numStocksPerPage;
        var end = (curPage + 1) * config.numStocksPerPage;
        var displayedKeys = stockSymbols.slice(begin, end);
        curSymbols = stockSymbols;
        table.innerHTML = "";
        if (displayedKeys.length > 0) {
            insertRowByValues(["Symbol", "Name", "Stock Price", "Buy"]);
            insertRowsBySymbols(displayedKeys);
        } else {
            insertRowByValue("Nothing found, please try again.");
        }
        
        updateButtons();
    }
    
    /**
     * Hides/shows the Previous and Next buttons depending on if there are more pages to show to the left/right of the current page
     */
    function updateButtons() {
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
    }
    
    /**
     * Inserts multiple rows of stock information into the stocks table.
     * 
     * symbols - an array of stock symbols (that are strings)
     */
    function insertRowsBySymbols(symbols) {
        for (var i = 0; i < symbols.length; i++) {
            insertRowBySymbol(symbols[i]);
        }
    }
    
    /**
     * Inserts the symbol's values into the stocks table.
     * This includes the stock's Symbol, Name, and Price
     * 
     * symbol - the symbol to get information from (i.e. AMZN)
     */
    function insertRowBySymbol(symbol) {
        var info = stockSymbolsMap[symbol];
        var name = info['name'];
        var price = info.price;
        var buttonId = 'buy' + symbol + 'Button';
        var buyButton = '<button id="' + buttonId + '" type="button">Buy</button>';
        
        insertRowByValues([symbol, name, price, buyButton]);
        
        //add the on click event after inserting the button into the table
        $( "#stocks_table #" + buttonId ).on( "click", function() {
            previewBuyStock(symbol);
        });
    }
    
    function previewBuyStock(symbol) {
        $('#previewBuyStockCash').text('$' + userInfo.cash);
        $('#previewBuyStockSymolName').text(symbol);
        $('#previewBuyStockPrice').text(stockSymbolsMap[symbol].price);
    }

    
    /**
     * Inserts the value into the stocks table as a row of its own.
     * 
     * value - the string to be inserted
     */
    function insertRowByValue(value) {
        insertRowByValues([value]);
    }
    
    /**
     * Inserts the given values into the stocks table. Each element in values will be in a new cell
     * 
     * values - an array of strings to be inserted
     */
    function insertRowByValues(values) {
        var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
        var row = table.insertRow(-1);
        for (var i = 0; i < values.length; i++) {
            row.insertCell(-1).innerHTML = values[i];
        }
    }
    
    /**
     * Replaces all the characters that match "find" in "str" with "replace"
     * @param {Object} find - the characters to replace
     * @param {Object} replace - the character to replace with
     * @param {Object} str - the string that will change
     */
    function replaceAll(find, replace, str) {
        return str.replace(new RegExp(find, 'g'), replace);
    }
    
    /**
     * Moves to and displays the previous page of stocks.
     */
    $('#previousStocksButton').click(function() {
        var firstPage = 0;
        if (curPage > firstPage) {
            curPage--;
            displayStocks(curSymbols);
        }
    });
    
    /**
     * Moves to and displays the next page of stocks.
     */
    $('#nextStocksButton').click(function() {
        var lastPage = curSymbols.length/config.numStocksPerPage - 1;
        if (curPage < lastPage) {
            curPage++;
            displayStocks(curSymbols);
        }
    });
    
    /**
     * Computes the total amount of money required to buy the number of stocks
     */
    $("#previewBuyStockQuantity").keyup(function() {
        var value = $('#previewBuyStockBox input[name=quantitybar]').val().trim();
        var stockSymbol = $("#previewBuyStockSymolName").html();
        var stockPrice = stockSymbolsMap[stockSymbol].price;
        console.log("price: " + stockPrice);
        var quantity = isPositiveInteger(value);
        console.log("quantity: " + quantity);
        if (quantity && stockPrice) {
            var totalPrice = quantity * stockPrice;
            $('#previewBuyStockBox #previewBuyStockTotalPrice').text('$' + totalPrice.toFixed(2));
        } else {
            $('#previewBuyStockBox #previewBuyStockTotalPrice').text("Please input a positive integer");
        }
    });
    
    $('#previewBuyStocksBuyButton').click(function() {
        var value = $('#previewBuyStockBox input[name=quantitybar]').val().trim();
        quantity = isPositiveInteger(value);
        if (quantity) {
            buyStock($("#previewBuyStockSymolName").html(), quantity);
        }
    });
    
    function isPositiveInteger(str) {
        if (str.indexOf('.') < 0) {
            var num = parseInt(str);
            if (num && num > 0) {
                return num;
            }
        }
        return false;
    }
    
    /**
     * TODO
     */
    function buyStock(symbol, quantity) {
        $.ajax("/buyStock", {
            method: "POST",
            data: {'symbol' : symbol,
                    'quantity' : quantity,
                    'stockPrice' : stockSymbolsMap[symbol].price
                    },
            success: function(data) {
                console.log(data);
                updateUserData();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("JSON.parse(jqXHR.responseText).message: " + jqXHR.responseText);
                console.log("error, did not buy stock");
            }
        });
    }
    
    /**
     * Finds out which stocks/stock names have matches with the searched value.
     * Then displays those stocks with the queried stock information.
     */
    $("#stockSearchBar").keyup(function() {
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
        displayStocks(keysToShow);
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