var stockSymbolsMap;
var config = {
    numStocksPerPage : 10,
};

var curPage = 0;

$( document ).ready(function() {
    $.ajax("/stockSymbolsMap", {
        success : function(data) {
            console.log("successfully got the stock symbols map!");
            stockSymbolsMap = JSON.parse(data);
            displayStocks();
        },
        error : function() {
            console.log("error, did not get the stock symbols map");
        }
    });
    
    function displayStocks() {
        var table = $('#stocks_table')[0]; //grab the DOM element (0 indexed element of a jQuery object)
        table.innerHTML = "";
        var keys = Object.keys(stockSymbolsMap);
        var displayedKeys = keys.slice(curPage * config.numStocksPerPage, (curPage + 1) * config.numStocksPerPage);
        
        $.ajax("/info", {
            data:{symbols: displayedKeys.toString()},
            success: function(data) {
                console.log("success, got the stock information");
                data = data.split('\n');
                data.pop(); //the last element will be an empty string
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
        for (i=0; i < values.length; i++) {
            displayCell(row, values[i]);
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
            displayStocks();
        }
    });
    
    $('#nextStocksButton').click(function() {
        if (curPage < Object.keys(stockSymbolsMap).length/config.numStocksPerPage - 1) {
            curPage++;
            displayStocks();
        }
    });
});