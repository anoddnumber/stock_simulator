(function($) {
    $.TopBar = function(options) {
        var topBar = {
             options : $.extend({
             }, options),

             showError : function(errorMsg) {
                $('#errorBox').text(errorMsg);
                $('#errorBox').show();
             },

            /**
             * Gets the error message from a jqXHR (jQuery XMLHttpRequest) object.
             */
            showErrorFromJqXHR : function(jqXHR) {
                var obj = JSON.parse(jqXHR.responseText);
                topBar.showError(obj.message);
            },

            changePage : function(page) {
                $('#tabs > div').hide();
                $('#' + page).show();
            },
        }

        return {
            showError : topBar.showError,
            showErrorFromJqXHR : topBar.showErrorFromJqXHR,
            changePage : topBar.changePage,
        };
    }
})(jQuery);
var TopBar = $.TopBar();


$( document ).ready(function() {
    //TODO make it "scalable" to add new pages without having to keep adding these click functions
    $('#loginPageLink').click(function() {
        TopBar.changePage('loginPage');
    });

    $('#stockTablePageLink').click(function() {
        TopBar.changePage('stockTablePage');
    });

    $('#profilePageLink').click(function() {
        TopBar.changePage('profilePage');
    });

    $('#loginLink').click(Login.showLoginForm);
    $('#createAccountLink').click(Login.showCreateAccount);
    $('#createAccountLink').click(Login.showCreateAccount);
//    $('#logoutButton').click(ApiClient.logout);
}) ;