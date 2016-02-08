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
                        //TODO redirect to login page
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
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
                        console.log("error when creating an account");
                    }
                });
            },

            /**
             * TODO, create a central helper for all the APIs, or maybe a client.
             *  since all the success and error parts of the functions are the same..
             */
            buyStock : function(symbol, quantity, price) {
                if (price == undefined) {
                    price = stockSymbolsMap[symbol].price;
                }

                $.ajax("/buyStock", {
                    method: "POST",
                    data: {'symbol' : symbol,
                           'quantity' : quantity,
                           'stockPrice' : price
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

            sellStock : function(symbol, quantity, price) {
                if (price == undefined) {
                    price = stockSymbolsMap[symbol].price;
                }

                $.ajax("/sellStock", {
                    method: "POST",
                    data: {'symbol' : symbol,
                           'quantity' : quantity,
                           'stockPrice' : price
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
                $.ajax("/getUserInfo", {
                    method: "GET",
                    success: function(data) {
                        try {
                            userInfo = JSON.parse(data);
                        } catch (err){
                            console.log("getting user info error: " + err);
                        }

                        $('.stockInfoPageTotalCash').text(userInfo.cash);
                        $('#cashBox').text('Cash: $' + userInfo.cash);
                        $('#previewBuyStockCash').text('$' + userInfo.cash);
                        console.log("userInfo: " + JSON.stringify(userInfo));

                        //TODO: Update stocks in profile page
                        ProfileTab.update(userInfo)
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
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
            updateCache : function(onSuccess) {
                $.ajax("/stockSymbolsMap", {
                    success : function(data) {
                        stockSymbolsMap = data.stockSymbolsMap;
                        var delay = data.delay;

                        //in case the delay is undefined, we don't want to continually call updateCache
                        if ( ! delay) {
                            delay = config.numMinutesToUpdate * 60 * 1000; //in milliseconds
                        }
                        setTimeout(apiClient.updateCache, delay);

                        //the last_updated date should not be shown to the user
                        delete stockSymbolsMap['last_updated'];

                        if (onSuccess) {
                            onSuccess();
                        }

                        BrowseTab.displayStocks(Object.keys(stockSymbolsMap));
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
            sellStock : apiClient.sellStock,
        }
    }
})(jQuery);
var ApiClient = $.ApiClient();