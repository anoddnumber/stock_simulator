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
        var begin = curPage * config.numStocksPerPage;
        var end = (curPage + 1) * config.numStocksPerPage;
        var displayedKeys = stockSymbols.slice(begin, end);
        curSymbols = stockSymbols;
        
        if (displayedKeys.length > 0) {
            $.ajax("/info", {
                data:{symbols: displayedKeys.toString()},
                success: function(data) {
                    console.log("success, got the stock information");
                    data = data.split('\n');
                    for (i = data.length - 1; i >= 0; i--) {
                        var value = data[i];
                        if (value.trim() === '') {
                            data.splice(i,1);
                            continue;
                        }
                        var symbol = curSymbols[begin + i];
                        var name = '"' + stockSymbolsMap[symbol] + '"'; 
                        data[i] = symbol + ',' + name + ',' + value;
                    }
                    data.unshift("Symbol, Name, Stock Price");
                    table.innerHTML = "";
                    data.forEach(displayRow);
                    if (data.length === 1) {
                        displayRow("Nothing found, please try again.");
                    }
                },
                error: function() {
                    console.log("error, could not retreive stock quotes.");
                }
            });
        } else {
            table.innerHTML = "";
            displayRow("Nothing found, please try again.");
        }
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
        if (values && values[values.length-1] !== 'N/A') {
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
    
    $("#stockSearchBar").keyup(event, function() {
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