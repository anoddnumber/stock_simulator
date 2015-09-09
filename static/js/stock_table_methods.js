var config = {
    numStocksPerPage : 10,
};

$( document ).ready(function() {
    var stockSymbolsMap;
    var curSymbols; //the symbols that should be shown 
    var curPage = 0;
    
    /**
     * Stores a map of stock symbols (the keys) to stock names (the values) in stockSymbolsMap
     */
    $.ajax("/stockSymbolsMap", {
        success : function(data) {
            console.log("successfully got the stock symbols map!");
            stockSymbolsMap = data;
            displayStocks(Object.keys(stockSymbolsMap));
        },
        error : function() {
            console.log("error, did not get the stock symbols map");
        }
    });
    
    /**
     * Displays all of the given stock symbols in a paginated view.
     * Meaning that the first n stocks will appear on the first page where n is config.numStocksPerPage
     * The other stocks will be displayed on the following pages when the user presses the next button.
     * 
     * stockSymbols - an array of stock symbols (that are strings)
     */
    function displayStocks(stockSymbols) {
        var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
        var begin = curPage * config.numStocksPerPage;
        var end = (curPage + 1) * config.numStocksPerPage;
        var displayedKeys = stockSymbols.slice(begin, end);
        curSymbols = stockSymbols;
        
        if (displayedKeys.length > 0) {
            _displayStockData(displayedKeys.toString());
        } else {
            table.innerHTML = "";
            displayRow("Nothing found, please try again.");
        }
    }
    
    /**
     * Helper method to display the stock data.
     * Calls the backend for the stock information and on success, displays all of the stock information in the stocks table.
     * On error, displays an error message.
     * 
     * stockSymbols - a string of stock symbols, delimited by commas (",")
     */
    function _displayStockData(stockSymbols) {
        console.log("stockSymbols: " + stockSymbols);
        var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
        $.ajax("/info", {
            data : {
                symbols : stockSymbols
            },
            success : function(data) {
                console.log("success, got the stock information");
                data = _formatStockData(data);
                data.unshift("Symbol, Name, Stock Price");
                table.innerHTML = "";
                data.forEach(displayRow);
                if (data.length === 1) {
                    displayRow("Nothing found, please try again.");
                }
            },
            error : function() {
                console.log("error, could not retreive stock quotes.");
                displayRow("Could not retreive any stock information. Please try again.");
            }
        }); 
    }
    
    /**
     * Formats the stock data so that it will be displayed correctly in the table.
     * Each row is formatted as "symbol, stock name, value"
     * 
     * data - the stock information returned by the server.
     *        The data is delimited by the newline character ("\n")
     */
    function _formatStockData(data) {
        var begin = curPage * config.numStocksPerPage;
        data = data.split('\n');
        for ( i = data.length - 1; i >= 0; i--) {
            var value = data[i];
            if (value.trim() === '') {
                data.splice(i, 1);
                continue;
            }
            var symbol = curSymbols[begin + i];
            var name = '"' + stockSymbolsMap[symbol] + '"';
            data[i] = symbol + ',' + name + ',' + value;
        }
        return data;
    }
    
    /**
     * Displays a row in the stock table. Designed to be used with the forEach method.
     * 
     * value - the row data, formatted as "symbol, stock name, value"
     * index - the row number (starting at 0)
     * arr - the array holding the values/row data
     */
    function displayRow(value, index, arr) {
        var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
        var row = table.insertRow(-1);
        
        /*
         * find all strings that are not a , or a "
         * but, find strings within double quotes (even if it is a ,)
         
         (?:           # non-capturing group
          [^\s"]+      # anything that's not a space or a double-quote
          |            #   or…
          "            # opening double-quote
          [^"]*        # …followed by zero or more chacacters that are not a double-quote
          "            # …closing double-quote
          )+           # each mach is one or more of the things described in the group
        */
        var values = value.match(/(?:[^,"]+|"[^"]*")+/g);
        if (values && values[values.length-1] !== 'N/A') {
            for (i=0; i < values.length; i++) {
                var value = values[i];
                value = replaceAll('"', '', value);
                row.insertCell(-1).innerHTML = value;
            }
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
        if (curPage > 0) {
            curPage--;
            displayStocks(curSymbols);
        }
    });
    
    /**
     * Moves to and displays the next page of stocks.
     */
    $('#nextStocksButton').click(function() {
        if (curPage < curSymbols.length/config.numStocksPerPage - 1) {
            curPage++;
            displayStocks(curSymbols);
        }
    });
    
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
            if (value.match(regEx) || stockSymbolsMap[value].match(regEx)) {
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