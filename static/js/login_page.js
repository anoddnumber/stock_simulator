(function($) {
    $.LoginPage = function(options) {
        var loginPage = {
             options : $.extend({
             }, options),

             showCreateAccount : function() {
                $('#createAccountLink').hide();
                $('#loginLink').show();

                $('#loginDiv').hide();
                $('#createAccountDiv').show();
             },

             showLogin : function() {
                $('#loginLink').hide();
                $('#createAccountLink').show();

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

var loginPage = $.LoginPage();

$("#loginLink").click(function(e) {
    e.preventDefault();
    loginPage.showLogin();
})

$("#createAccountLink").click(function(e) {
    e.preventDefault();
    loginPage.showCreateAccount();
})