// executes when the DOM is ready
$( document ).ready(function() {
    initPage();
});

// executes when the complete page is fully loaded, including all frames, objects and images
$(window).load(function() {
    onPageLoad();
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

function onPageLoad() {
    var path = window.document.location.pathname;
    if (path.indexOf("stocks") > -1) {
        BrowseTab.onPageLoad();
    }

    if (path == "/") {
        ProfileTab.onPageLoad();
    }

    if (path.indexOf("stock/") > -1) {
        StockInfoPage.onPageLoad();
    }
}