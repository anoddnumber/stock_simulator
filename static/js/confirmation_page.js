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

                var errArg = $('#err-arg').data('err-arg');
                var a = Utility.replaceUrlParam("err", errArg);
                history.replaceState({}, document.title, a);
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

