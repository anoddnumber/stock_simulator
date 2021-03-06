(function($) {
    $.ProfilePage = function(options) {
        var table;
        var totalEquities;

        var profilePage = {
            options : $.extend({
            }, options),

            updatePage : function() {
                profilePage.createTable();
            },

            //TODO probably a better way to do this with DataTables
            createTable : function() {
                // https://datatables.net/reference/option/dom
                // https://datatables.net/examples/advanced_init/dom_toolbar.html
                table = $('#profile_table').DataTable({
                    "columns": [
                        { className: "symbol" },
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                        null,
                    ],
                    "pageLength": 10,
                    "paging": true,
                    "lengthChange" : false,
                    language: {
                        search: "_INPUT_", //Don't display any label left of the search box
                        searchPlaceholder: ""
                    },
                    "dom": 'f<"availableCash"><"totalEquities"><"total">tip' //TODO change the stockInfoPageTotalCash class..
                });

                table.clear();

                var rows = profilePage.buildTable();
                table.rows.add(rows);
                table.draw(true);
            },

            getRow : function(symbol) {
                    var symbolData = userInfo.stocks_owned[symbol];
                    var pricesBought = Object.keys(symbolData);
                    var totalPriceBought = 0;
                    var totalQuantity = 0;
                    for (var j = 0; j < pricesBought.length; j++) {
                        var price = pricesBought[j];
                        var quantity = Number(symbolData[price]);
                        if (price === "total") continue;
                        price = price.replace("_", ".");
                        price = Number(price);

                        totalPriceBought += price * quantity;
                        totalQuantity += quantity;
                    }
                    var symbolInfo = stockSymbolsMap[symbol];
                    if ( ! symbolInfo) {
                        console.log("User owns stock with symbol " + symbol + " but we do not have any information"
                        + " about this stock");
                        return;
                    }

                    var avgPrice = (totalPriceBought / totalQuantity).toFixed(2);
                    var currentPrice = symbolInfo.price;
                    var priceDifference = (currentPrice - avgPrice).toFixed(2);
                    var percentDifference = Utility.getPercentDifference(avgPrice, currentPrice).toFixed(2);
                    var dayPriceDifference = symbolInfo.daily_price_change;
                    var dayPercentDifference = symbolInfo.daily_percent_change;
                    totalPriceBought = totalPriceBought.toFixed(2);
                    var currentTotalValue = (totalQuantity * currentPrice).toFixed(2);

                    totalEquities += parseFloat(currentTotalValue);

                    var row = [symbol, totalQuantity, avgPrice, currentPrice, priceDifference, percentDifference,
                    dayPriceDifference, dayPercentDifference, totalPriceBought, currentTotalValue]

                    return row;
            },

            getTable : function() {
                return table;
            },

            /**
            *   Builds the profile table and returns the rows in a 2d array
            *   where each array represents a row in the table.
            */
            buildTable : function() {
                var rows = new Array();

                var keys = Object.keys(userInfo.stocks_owned);
                for (var i = 0; i < keys.length; i++) {
                    var symbol = keys[i];
                    var row = profilePage.getRow(symbol);
                    if (row) {
                        rows.push(row);
                    }
                }

                return rows;
            },

            init : function() {
                table = undefined;
                totalEquities = 0;

                profilePage.updatePage();

                var page = Math.floor(Utility.getUrlParameter("page")) - 1;
                if (isNaN(page) || page < 0) {
                    page = 0;
                }
                table.page(page).draw("page");

                profilePage.setupRows();

                $('#navbarTabs li').removeClass('active');
                $('#profileTab').addClass('active');

                // select the search bar
                $('.dataTables_wrapper .dataTables_filter label input[type=search]').focus();
                $('.availableCash').text("Available Cash: $" + userInfo.cash);
                $('.totalEquities').text("Total Equities: $" + totalEquities.toFixed(2));
                $('.total').text( "Total: $" + (parseFloat(userInfo.cash) + totalEquities).toFixed(2) );

                // https://datatables.net/reference/event/page
                $('#profile_table').on('page.dt', function () {
                    Utility.modifyPageParam(table);
                } );

                // when changing pages in the table, we have to attach hrefs and the ajax loading plugin to the rows
                // this should come after table.page(page).draw("page"); or else the rows will be set up twice
                // and the next page will be pushed onto the browser's history twice.
                $('#profile_table').on( 'draw.dt', function () {
                    profilePage.setupRows();
                });
            },

            onPageLoad : function() {
                // select the search bar
                $('.dataTables_wrapper .dataTables_filter label input[type=search]').focus();
            },

            setupRows : function() {
                $('#profile_table tbody tr').each(function (i, row) {
                    var symbol = $(row).find('.symbol').text();
                    if (symbol && symbol != "") {
                        $(row).attr("href", "/stock/" + symbol);
                        ChangePageHelper.attachChangePageAction($(row));
                    }
                });
            },
         }

         return {
            updatePage : profilePage.updatePage,
            getTable : profilePage.getTable,
            init : profilePage.init,
            onPageLoad : profilePage.onPageLoad,
        };
    }
})(jQuery);

var ProfilePage = $.ProfilePage();


$( document ).ready(function() {
    ProfilePage.init();
    $('#loadingbar-frame').show();
});

