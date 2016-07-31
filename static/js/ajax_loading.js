(function($) {
    $.ChangePageHelper = function(options) {

        var changePageHelper = {
            attachChangePageAction : function (selector, replaceURL) {
                if ( replaceURL == undefined) {
                    replaceURL = true;
                }

                for (var i = 0; i < selector.length; i++) {
                    value = $(selector.get(i));
                    value.unbind("click");
                    value.loadingbar({
                        target: "#loadingbar-frame",
                        replaceURL: replaceURL,
                        direction: "right",

                        /* Default Ajax Parameters.  */
                        async: true,
                        complete: function(xhr, text) {},
                        cache: true,
                        error: function(xhr, text, e) {},
                        global: true,
                        headers: {},
                        statusCode: {},
                        success: function(data, text, xhr) {},
                        dataType: "html",
                        done: function(data) {
                            var simulator = $(data).find("#stock_simulator");
                            $(this.target).html(simulator);

                            var dropdownElem = $('.dropdown-toggle');
                            if (dropdownElem && dropdownElem.attr('aria-expanded') === "true") {
                                dropdownElem.dropdown("toggle");
                            }
                        }
                    });
                }
            }
        }

        return  {
            attachChangePageAction : changePageHelper.attachChangePageAction
        };
    }
})(jQuery);

var ChangePageHelper = $.ChangePageHelper();

$( document ).ready(function() {
    // attach the page helper to all a elements with attribute href
    ChangePageHelper.attachChangePageAction($('a[href]'));
});