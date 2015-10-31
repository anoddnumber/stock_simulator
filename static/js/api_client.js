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
                $.ajax("/getUserInfo", {
                    method: "GET",
                    success: function(data) {
                        try {
                            userInfo = JSON.parse(data);
                            $('#cashBox').text('Cash: $' + userInfo.cash);
                            $('#previewBuyStockCash').text('$' + userInfo.cash);

                            //TODO: Update stocks in profile page
                            updateProfilePage(userInfo)
                        } catch (err){
                            //not logged in, thus the response is not in JSON format
                        }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        TopBar.showErrorFromJqXHR(jqXHR);
                        console.log("error, did not retrieve user data");
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
        }
    }
})(jQuery);
var ApiClient = $.ApiClient();