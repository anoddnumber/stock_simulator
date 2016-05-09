(function($) {
    $.ChangePageHelper = function(options) {

        var changePageHelper = {
            attachChangePageAction : function (selector, page, tabId) {
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

                        $(this.target).html(simulator.get(0));
                        page.init();

                        if (tabId != '') {
                            $('#navbarTabs > li').removeClass('active');
                            $('#' + tabId).addClass('active');
                        }

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
    ChangePageHelper.attachChangePageAction($(".stocksTabLink"), BrowseTab, 'stocksTab');
    ChangePageHelper.attachChangePageAction($(".profileTabLink"), ProfileTab, 'profileTab');
//    changePageHelper($(".profileTabLink"), StockInfoPage, '');
});