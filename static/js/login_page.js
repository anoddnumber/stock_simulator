(function($) {
    $.LoginPage = function(options) {
        var loginPage = {
             options : $.extend({
             }, options),

             showCreateAccount : function() {
                $('#accountLinks').hide();
                $('#loginLink').show();

                $('#loginDiv').hide();
                $('#createAccountDiv').show();
             },

             showLogin : function() {
                $('#loginLink').hide();
                $('#accountLinks').show();

                $('#createAccountDiv').hide();
                $('#loginDiv').show();
             },
        }

        return {
            showCreateAccount : loginPage.showCreateAccount,
            showLogin : loginPage.showLogin,
        };
    }
})(jQuery);

var LoginPage = $.LoginPage();

$( document ).ready(function() {
    $("#loginLink").click(function(e) {
        e.preventDefault();
        LoginPage.showLogin();
    })

    $("#createAccountLink").click(function(e) {
        e.preventDefault();
        LoginPage.showCreateAccount();
    })
});