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
                            Utility.updateUserData();
                        }
                        console.log(data);
                        $('#usernameBox').text(formData.username);
                        Utility.updateUserData();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        showErrorFromJqXHR(jqXHR);
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
                        Utility.updateUserData();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        showErrorFromJqXHR(jqXHR);
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
                        showErrorFromJqXHR(jqXHR);
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
                        showErrorFromJqXHR(jqXHR);
                    }
                });
            }
        }

        return {
            login : apiClient.login,
            logout : apiClient.logout,
            createAccount : apiClient.createAccount,
        }
    }
})(jQuery);
var ApiClient = $.ApiClient();