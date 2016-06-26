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
                browseTab.createTable();
                $('.availableCash').text("Available Cash: $" + userInfo.cash);
            },

            //TODO probably a better way to do this with DataTables
            createTable : function() {
                // https://datatables.net/reference/option/dom
                // https://datatables.net/examples/advanced_init/dom_toolbar.html
                table = $('#stocks_table').DataTable({
                    "lengthChange" : false,
                    "columns": [
                        { className: "symbol" },
                        null,
                        null,
                        null,
                        null,
                        null,
                    ],
                    "pageLength": 10,
                    language: {
                        search: "_INPUT_", //Don't display any label left of the search box
                        searchPlaceholder: ""
                    },
//                     the "columns" key below makes the table static and not dynamic, so if you resize the browser window after
//                     the page loads, then the table won't change. The "autoWidth" seems to be okay for now
//                    "columns": [
//                        { "width": "10%" }, { "width": "30%" }, { "width": "15%" }, { "width": "15%" }, { "width": "15%" }, { "width": "15%" }
//                    ],
                    "autoWidth": false,
                    "dom": 'f<"availableCash">tip' //TODO change the stockInfoPageTotalCash class..
                });
                table.clear();

                var rows = browseTab.buildTable();
                table.rows.add(rows);
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

                if ( ! info) {
                    console.log("Stock with symbol " + symbol + " trying to be displayed on stocks page but we do not"
                                + " have any information about the stock");
                    return;
                }

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
                    if (row) {
                        rows.push(row);
                    }
                }

                return rows;
            },

            previewBuyStock : function(symbol) {
                $('#previewBuyStockCash').text('$' + userInfo.cash);
                $('#previewBuyStockSymolName').text(symbol);
                $('#previewBuyStockPrice').text(stockSymbolsMap[symbol].price);
            },

            init : function() {
                table = undefined;

                //TODO: make a highlight or change tabs function in Utility
                $('#navbarTabs li').removeClass('active');
                $('#stocksTab').addClass('active');

                browseTab.updatePage();

                var page = Math.floor(Utility.getUrlParameter("page")) - 1;
                if (isNaN(page) || page < 0) {
                    page = 0;
                }
                table.page(page).draw("page");

                browseTab.setupRows();

                // https://datatables.net/reference/event/page
                // This deals with changing pages in the stocks table
                $('#stocks_table').on('page.dt', function () {
                    Utility.modifyPageParam(table);
                } );


                // when changing pages in the table, we have to attach hrefs and the ajax loading plugin to the rows
                $('#stocks_table').on( 'draw.dt', function () {
                    browseTab.setupRows();
                });

                // select the search bar
                $('.dataTables_wrapper .dataTables_filter label input[type=search]').focus();
            },

            onPageLoad : function() {
                // select the search bar
                $('.dataTables_wrapper .dataTables_filter label input[type=search]').focus();
            },

            setupRows : function() {
                $('#stocks_table tbody tr').each(function (i, row) {
                    var symbol = $(row).find('.symbol').text();
                    $(row).attr("href", "/stock/" + symbol);
                    ChangePageHelper.attachChangePageAction($(row), StockInfoPage);
                });
            },
        }

        return {
            updatePage : browseTab.updatePage,
            displaySortedArray : browseTab.displaySortedArray,
            getTable : browseTab.getTable,
            init : browseTab.init,
            onPageLoad : browseTab.onPageLoad
        };
    };
})(jQuery);

var BrowseTab = $.BrowseTab();
