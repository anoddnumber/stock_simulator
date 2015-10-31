/**
* The API Client contains methods to help call the backend API.
*/
(function($) {
    $.ApiClient = function(options) {
        var apiClient = {
             options : $.extend({
             }, options),

             /**
             *   TODO: Make the other methods in here call this. Also change its name.
             */
             helper : function (apiName, method, data, onSuccess, onError) {
                $.ajax(apiName, {
                    method: method,
                    data: data,
                    success: function(data) {
                        if (onSuccess) {
                            onSuccess();
                        } else {
                            ApiClient.updateUserData();
                        }
                        console.log(data);
                        $('#usernameBox').text(formData.username);
                        ApiClient.updateUserData();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        TopBar.showErrorFromJqXHR(jqXHR);
                        console.log("error, did not login");
                    }
                });
             },

             login : function(formData) {
                $.ajax("/login", {
                    method: "POST",
                    data: formData,
                    success: function(data) {
                        console.log(data);
                        $('#usernameBox').text(formData.username);
                        ApiClient.updateUserData();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        TopBar.showErrorFromJqXHR(jqXHR);
                        console.log("error, did not login");
                    }
                });
             },

             logout : function() {
                $.ajax("/logout", {
                    method: "POST",
                    success: function(data) {
                        console.log(data);
                        $('#usernameBox').text("Not logged in");
                        $('#cashBox').text("");
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        TopBar.showErrorFromJqXHR(jqXHR);
                        console.log("error, did not log out");
                    }
                });
             },

             createAccount : function(formData) {
                $.ajax("/createAccount", {
                    method: "POST",
                    data: formData,
                    success: function(data) {
                        console.log("successfully created account!");
                    },
                    error: function(jqXHR, textStatus, errorThrown ) {
                        TopBar.showErrorFromJqXHR(jqXHR);
                    }
                });
            },

            /**
             * TODO, create a central helper for all the APIs, or maybe a client.
             *  since all the success and error parts of the functions are the same..
             */
            buyStock : function(symbol, quantity) {
                $.ajax("/buyStock", {
                    method: "POST",
                    data: {'symbol' : symbol,
                            'quantity' : quantity,
                            'stockPrice' : stockSymbolsMap[symbol].price
                            },
                    success: function(data) {
                        console.log(data);
                        ApiClient.updateUserData();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("JSON.parse(jqXHR.responseText).message: " + jqXHR.responseText);
                        console.log("error, did not buy stock");
                    }
                });
            },

            updateUserData : function() {
                console.log("updateUserData");
                $.ajax("/getUserInfo", {
                    method: "GET",
                    success: function(data) {
                        try {
                            userInfo = JSON.parse(data);
                            $('#cashBox').text('Cash: $' + userInfo.cash);
                            $('#previewBuyStockCash').text('$' + userInfo.cash);

                            //TODO: Update stocks in profile page
                            ProfileTab.update(userInfo)
                        } catch (err){
                            //not logged in, thus the response is not in JSON format
                            console.log("not logged in");
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        TopBar.showErrorFromJqXHR(jqXHR);
                        console.log("error, did not retrieve user data");
                    }
                });
            },

                        /**
             * Stores a map of stock symbols (the keys) to an object with stock information .
             * Also updates the lastUpdatedDate variable.
             *
             * The object is as follows:
             * {
             *     'name' : *Stock Name*,
             *     'price': *Stock Price*
             * }
             * Updates the cache: TODO move to global area
             */
            updateCache : function() {
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
                            setTimeout(apiClient.updateCache, numMillisecondsToUpdate);
                        } else {
                            setTimeout(apiClient.updateCache, delay);
                        }

                        //the last_updated date should not be shown to the user
                        delete stockSymbolsMap['last_updated'];

                        //TODO: create a displayStocksHelper that takes in a list of symbols to display
                        //displayStocks will then have no parameters and defaults to curSymbols or Object.keys(stockSymbolsMap)
                        if ( ! BrowseTab.getCurSymbols()) {
                            BrowseTab.displayStocks(Object.keys(stockSymbolsMap));
                        } else {
                            BrowseTab.displayStocks(BrowseTab.getCurSymbols());
                        }

                    },
                    error : function() {
                        console.log("error, did not get the stock symbols map");
                        //try again in a minute...
                        var numMillisecondsToUpdate = 60000;
                        setTimeout(apiClient.updateCache, numMillisecondsToUpdate);
                    }
                });
            },
        }

        return {
            login : apiClient.login,
            logout : apiClient.logout,
            createAccount : apiClient.createAccount,
            buyStock : apiClient.buyStock,
            updateUserData : apiClient.updateUserData,
            updateCache : apiClient.updateCache,
        }
    }
})(jQuery);
var ApiClient = $.ApiClient();