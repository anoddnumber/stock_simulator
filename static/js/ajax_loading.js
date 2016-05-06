$( document ).ready(function() {
    changePageHelper($(".stocksTabLink"), BrowseTab, 'stocksTab');
    changePageHelper($(".profileTabLink"), ProfileTab, 'profileTab');
});


function changePageHelper(selector, tab, tabId) {
    console.log("selector: " + selector);
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
            tab.init();
            $('#navbarTabs > li').removeClass('active');
            $('#' + tabId).addClass('active');
        }
    });
}
