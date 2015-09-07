var config = {
    numStocksPerPage : 10,
};

$( document ).ready(function() {
    var stockSymbolsMap;
    var curSymbols; //the symbols that should be shown 
    var curPage = 0;
    
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
    
    function displayStocks(stockSymbols) {
        var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
        table.innerHTML = "";
        var begin = curPage * config.numStocksPerPage;
        var end = (curPage + 1) * config.numStocksPerPage;
        var displayedKeys = stockSymbols.slice(begin, end);
        curSymbols = stockSymbols;
        $.ajax("/info", {
            data:{symbols: displayedKeys.toString()},
            success: function(data) {
                console.log("success, got the stock information");
                data = data.split('\n');
                data.pop(); //the last element will be an empty string
                data.forEach(function(value, index, arr) {
                    var symbol = curSymbols[begin + index];
                    var name = '"' + stockSymbolsMap[symbol] + '"'; 
                    arr[index] = symbol + ',' + name + ',' + value;
                });
                data.unshift("Symbol, Name, Stock Price");
                data.forEach(displayRow);
            },
            error: function() {
                console.log("error, could not retreive stock quotes.");
            }
        });
    }
    
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
        if (values) {
            for (i=0; i < values.length; i++) {
                displayCell(row, values[i]);
            }
        }
    }
    
    function displayCell(row, value) {
        value = replaceAll('"', '', value);
        row.insertCell(-1).innerHTML = value;
    }
    
    function replaceAll(find, replace, str) {
      return str.replace(new RegExp(find, 'g'), replace);
    }
    
    $('#previousStocksButton').click(function() {
        if (curPage > 0) {
            curPage--;
            displayStocks(curSymbols);
        }
    });
    
    $('#nextStocksButton').click(function() {
        if (curPage < curSymbols.length/config.numStocksPerPage - 1) {
            curPage++;
            displayStocks(curSymbols);
        }
    });
    
    // Search for stocks that contain the user's query.
    $('#searchStocksForm').submit(function(event) {
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
        
        var query = $('#searchStocksForm input[name=searchbar]').val().trim();
        var regEx = new RegExp(query,'i');
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
});