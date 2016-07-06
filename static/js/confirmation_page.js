(function($) {
    $.ConfirmationPage = function(options) {

        var confirmationPage = {
            options : $.extend({
            }, options),

            init : function() {
                $("#backButton").attr("href", $(location).attr('href'));
                ChangePageHelper.attachChangePageAction($("#backButton"));
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

