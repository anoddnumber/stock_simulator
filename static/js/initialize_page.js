$( document ).ready(function() {
    initPage();
});

function initPage() {
    var path = window.document.location.pathname;
    if (path.indexOf("stocks") > -1) {
        BrowseTab.init();
    }

    if (path == "/") {
        ProfileTab.init();
    }

    if (path.indexOf("stock/") > -1) {
        StockInfoPage.init();
    }
}