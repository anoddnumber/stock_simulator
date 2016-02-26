(function($) {
    $.LoginPage = function(options) {
        var loginPage = {
             options : $.extend({
             }, options),
        }

        return {
        };
    }
})(jQuery);

var LoginPage = $.LoginPage();

$( document ).ready(function() {

    var loginPageContainer = $.MutuallyExclusiveContainer({
        'selectors' : ['#loginDiv', '#createAccountDiv']
    });

    $("#loginLink").click(function(e) {
        e.preventDefault();
        loginPageContainer.show('#loginDiv');
    })

    $("#createAccountLink").click(function(e) {
        e.preventDefault();
        loginPageContainer.show('#createAccountDiv');
    })
});