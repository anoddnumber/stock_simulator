var config = {
    numMinutesToUpdate : .1,
};

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
                    method: "GET",
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

            /**
             * TODO, create a central helper for all the APIs, or maybe a client.
             *  since all the success and error parts of the functions are the same..
             */
            buyStock : function(symbol, quantity, price, onSuccess) {
                if (price == undefined) {
                    price = stockSymbolsMap[symbol].price;
                }

                $.ajax("/buy", {
                    method: "POST",
                    data: {'symbol' : symbol,
                           'quantity' : quantity,
                           'stockPrice' : price
                          },
                    success: function(data) {
                        onSuccess(data);
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("JSON.parse(jqXHR.responseText).message: " + jqXHR.responseText);
                        console.log("error, did not buy stock");
                    }
                });
            },

            sellStock : function(symbol, quantity, price, onSuccess) {
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
                        onSuccess(data);
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("JSON.parse(jqXHR.responseText).message: " + jqXHR.responseText);
                        console.log("error, did not buy stock");
                    }
                });
            },
        }

        return {
            login : apiClient.login,
            logout : apiClient.logout,
            buyStock : apiClient.buyStock,
            sellStock : apiClient.sellStock,
        }
    }
})(jQuery);
var ApiClient = $.ApiClient();