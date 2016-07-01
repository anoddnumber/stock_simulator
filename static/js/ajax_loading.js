(function($) {
    $.ChangePageHelper = function(options) {

        var changePageHelper = {
            attachChangePageAction : function (selector) {
                selector.unbind("click");
                selector.loadingbar({
                    target: "#loadingbar-frame",
                    replaceURL: true,
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
                    }
                });
            }
        }

        return  {
            attachChangePageAction : changePageHelper.attachChangePageAction
        };
    }
})(jQuery);

var ChangePageHelper = $.ChangePageHelper();

$( document ).ready(function() {
    ChangePageHelper.attachChangePageAction($(".stocksPageLink"));
    ChangePageHelper.attachChangePageAction($(".profilePageLink"));
});