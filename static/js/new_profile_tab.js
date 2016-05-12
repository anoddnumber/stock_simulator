(function($) {
    $.ProfileTab = function(options) {
        var table;
        var totalEquities;

        var profileTab = {
            options : $.extend({
            }, options),

            updatePage : function() {
                if (table) {
                    var numRows = Object.keys(userInfo.stocks_owned).length;
                    if (numRows != table.rows().count()) {
                        profileTab.createTable();
                    } else {
                        profileTab.updateTable();
                    }
                } else {
                    profileTab.createTable();
                }
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

                var rows = profileTab.buildTable();
                table.rows.add(rows);
                table.draw(true);
            },

            updateTable : function() {
                table.rows().every( function () {
                    var d = this.data();

                    d.counter++; // update data source for the row

                    this.invalidate(); // invalidate the data DataTables has cached for this row
                    var symbol = d[0];
                    //TODO: some reason the table redraws on "this.data(row data here)" as well
                    //Seems like a datatable bug. Should only be redrawing on table.draw(false);
                    this.data(profileTab.getRow(symbol));
                } );

                table.draw(false);
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
                    var row = profileTab.getRow(symbol);
                    rows.push(row);
                }

                return rows;
            },

            init : function() {
                table = undefined;
                totalEquities = 0;

                profileTab.updatePage();

                var page = Math.floor(getUrlParameter("page")) - 1;
                if (isNaN(page) || page < 0) {
                    page = 0;
                }
                table.page(page).draw("page");

                profileTab.setupRows();

                $('#navbarTabs li').removeClass('active');
                $('#profileTab').addClass('active');

                // select the search bar
                $('.dataTables_wrapper .dataTables_filter label input[type=search]').focus();
                $('.availableCash').text("Available Cash: $" + userInfo.cash);
                $('.totalEquities').text("Total Equities: $" + totalEquities);
                $('.total').text( "Total: $" + (parseFloat(userInfo.cash) + totalEquities).toFixed(2) );

                // https://datatables.net/reference/event/page
                $('#profile_table').on('page.dt', function () {
                    var info = table.page.info();

                    // info.page has a range of [0, info.pages)
                    var url = document.URL;     // Returns full URL
                    var newUrl = document.location.origin;

                    if (info.page != 0) {
                        newUrl = replaceUrlParam(url, "page", info.page + 1);
                    }

                    history.pushState( {}, document.title, newUrl);
                } );

                // when changing pages in the table, we have to attach hrefs and the ajax loading plugin to the rows
                // this should come after table.page(page).draw("page"); or else the rows will be set up twice
                // and the next page will be pushed onto the browser's history twice.
                $('#profile_table').on( 'draw.dt', function () {
                    profileTab.setupRows();
                });
            },

            onPageLoad : function() {
                // select the search bar
                $('.dataTables_wrapper .dataTables_filter label input[type=search]').focus();
            },

            setupRows : function() {
                $('#profile_table tbody tr').each(function (i, row) {
                    var symbol = $(row).find('.symbol').text();
                    $(row).attr("href", "/stock/" + symbol);
                    ChangePageHelper.attachChangePageAction($(row), StockInfoPage);
                });
            },
         }

         return {
            updatePage : profileTab.updatePage,
            getTable : profileTab.getTable,
            init : profileTab.init,
            onPageLoad : profileTab.onPageLoad,
        };
    }
})(jQuery);

var ProfileTab = $.ProfileTab();

function replaceUrlParam(url, paramName, paramValue){
    var pattern = new RegExp('\\b('+paramName+'=).*?(&|$)')
    if(url.search(pattern)>=0){
        return url.replace(pattern,'$1' + paramValue + '$2');
    }
    return url + (url.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue
}

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};