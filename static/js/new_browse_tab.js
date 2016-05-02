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

            updatePage : function() {
                if (table) {
                    browseTab.updateTable();
                } else {
                    browseTab.createTable();
                }
                $('.availableCash').text("Available Cash: $" + userInfo.cash);
            },

            //TODO probably a better way to do this with DataTables
            createTable : function() {
                table = $('#stocks_table').DataTable();
                table.clear();

                var rows = browseTab.buildTable();
                table.rows.add(rows);
                table.draw(false);
            },

            updateTable : function() {
                table.rows().every( function () {
                    var d = this.data();

                    d.counter++; // update data source for the row

                    this.invalidate(); // invalidate the data DataTables has cached for this row
                    var symbol = d[0];
                    //TODO: some reason the table redraws on "this.data(row data here)" as well
                    //Seems like a datatable bug. Should only be redrawing on table.draw(false);
                    this.data(browseTab.getRow(symbol));
                } );

                table.draw(false);
            },

            enableButton: function(symbol) {
                var buttonId = 'buy' + symbol + 'Button';
                //add the on click event after inserting the button into the table
                $( "#stocks_table #" + buttonId ).on( "click", function() {
                    browseTab.previewBuyStock(symbol);
                });
            },

            getRow : function(symbol) {
                var info = stockSymbolsMap[symbol];
                var name = info['name'];
                var dailyPercentChange = info.daily_percent_change;
                var dailyPriceChange = info.daily_price_change;
                var price = info.price;

                var buttonId = 'buy' + symbol + 'Button';
                buttonSymbols.push(symbol);
                var buyButton = '<button id="' + buttonId + '" type="button">Buy</button>';

                var row = [symbol, name, dailyPercentChange, dailyPriceChange, price, buyButton];
                return row;
            },

            getTable : function() {
                return table;
            },

            /**
            *   Builds the stocks table and returns the rows in a 2d array
            *   where each array represents a row in the table.
            *
            *   symbols - an array of stock symbols
            */
            buildTable : function() {
                var symbols = Object.keys(stockSymbolsMap);
                var rows = new Array();
                for (var i = 0; i < symbols.length; i++) {
                    var symbol = symbols[i];
                    if (symbol == "last_updated") {
                        continue;
                    }
                    var row = browseTab.getRow(symbol);
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
            updatePage : browseTab.updatePage,
            displaySortedArray : browseTab.displaySortedArray,
            getTable : browseTab.getTable,
        };
    };
})(jQuery);

var BrowseTab = $.BrowseTab();

$( document ).ready(function() {
    // https://datatables.net/reference/option/dom
    // https://datatables.net/examples/advanced_init/dom_toolbar.html
    $('#stocks_table').DataTable({
        "lengthChange" : false,
        language: {
            search: "_INPUT_", //Don't display any label left of the search box
            searchPlaceholder: "Search"
        },
        // the "columns" key below makes the table static and not dynamic, so if you resize the browser window after
        // the page loads, then the table won't change. The "autoWidth" seems to be okay for now
//        "columns": [
//            { "width": "10%" }, { "width": "30%" }, { "width": "15%" }, { "width": "15%" }, { "width": "15%" }, { "width": "15%" }
//        ],
        "autoWidth": false,
        "dom": 'f<"availableCash">tip' //TODO change the stockInfoPageTotalCash class..
    });

    $('#stocks_table tbody').on('click', 'tr', function(event) {
        table = BrowseTab.getTable();
        var data = table.row( this ).data();
        var symbol = data[0];

        window.location.href = '/stock/' + symbol
    });

    BrowseTab.updatePage();
});





