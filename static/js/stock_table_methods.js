var config = {
    numStocksPerPage : 10,
};

$( document ).ready(function() {
    var stockSymbolsMap;
    var curSymbols; //the symbols that should be shown 
    var curPage = 0;
    
    /**
     * Stores a map of stock symbols (the keys) to an object with stock information 
     * 
     * The object is as follows: 
     * {
     *     'name' : *Stock Name*,
     *     'price': *Stock Price*
     * }
     */
    $.ajax("/stockSymbolsMap", {
        success : function(data) {
            console.log("successfully got the stock symbols map!");
            stockSymbolsMap = JSON.parse(data);
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
        table.innerHTML = "";
        if (displayedKeys.length > 0) {
            insertRowByValues(["Symbol", "Name", "Stock Price"]);
            insertRowsBySymbols(displayedKeys);
        } else {
            insertRowByValue("Nothing found, please try again.");
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
        
        insertRowByValues([symbol, name, price]);
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