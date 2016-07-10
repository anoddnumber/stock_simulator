(function($) {
    $.ConfirmationPage = function(options) {

        var confirmationPage = {
            options : $.extend({
            }, options),

            init : function() {
                $("#backButton").unbind("click");
                $('#backButton').click(function() {
                    history.back();
                });
            }
         }

         return {
            init: confirmationPage.init,
        };
    }
})(jQuery);

var ConfirmationPage = $.ConfirmationPage();


$( document ).ready(function() {
    ConfirmationPage.init();
});

