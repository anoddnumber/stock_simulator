(function($) {
    $.StockInfoPage = function(options) {
        var stockInfoPage = {
             options : $.extend({
             }, options),

             setupSlider : function() {
                var cash = $('.stockInfoPageTotalCash').text();
                var price = $('.stockInfoPageStockPrice').text();
                var numOwned = $('.stockInfoPageAmountOwned').text();

                // by default, the buy radio button is selected
                // TODO refactor to make a "set slider bar max/min" function
                $(".stockInfoPage .buyStockRadioButton").prop("checked", true);
                $('.stockInfoPage input').attr({
                    "min" : 0,
                    "max" : Math.floor( (cash - commission) / price),
                });

                //make sure we don't stack up actions on the click event..
                $("input[name=market]").unbind("click");
                var defaultValue = 0;
                $('.stockInfoPage input[name=amountRange]')[0].value = defaultValue;
                $('.stockInfoPage input[name=amountInput]')[0].value = defaultValue;

                $("input[name=market]").click(function(){
                    $('.stockInfoPage input[name=amountRange]')[0].value = defaultValue;
                    $('.stockInfoPage input[name=amountInput]')[0].value = defaultValue;

                    if ($('.buyStockRadioButton').is(':checked')) {
                        // clicked the buy radio button

                        $('.stockInfoPage input[name=amountRange]').attr({
                            "min" : 0,
                            "max" : Math.floor(cash / price),
                        });
                    } else if ($('.sellStockRadioButton').is(':checked')) {
                        // clicked the sell radio button

                        $('.stockInfoPage input[name=amountRange]').attr({
                            "min" : 0,
                            "max" : numOwned,
                        });

                    }
                });
            },

            setupButtons : function() {
                $(".stockInfoPageStocksConfirmButton").unbind("click");

                $('.stockInfoPageStocksConfirmButton').click(function() {
                    var value = $('.stockInfoPage input[name=amountInput]').val().trim();
                    var quantity = Utility.isPositiveInteger(value);

                    var price = $('.stockInfoPageStockPrice').text().trim();

                    if (quantity) {
                        var symbol = $(".stockInfoPageStockSymbolName").html().replace("(","").replace(")","");
                        if ($('.buyStockRadioButton').is(':checked')) {
                            ApiClient.buyStock(symbol, quantity, price, function(data) {
                                data = JSON.parse(data);

                                $('.stockInfoPageAmountOwned').text(data.stocks_owned[symbol].total);
                                $('.stockInfoPageTotalCash').text(data.cash);

                                stockInfoPage.init();
                            });
                        } else if ($('.sellStockRadioButton').is(':checked')) {
                            ApiClient.sellStock(symbol, quantity, price, function(response) {
                                response = JSON.parse(response);
                                data = response["data"];
                                error = response["error"];

                                if ( ! error) {
                                    if (data.stocks_owned[symbol]) {
                                        $('.stockInfoPageAmountOwned').text(data.stocks_owned[symbol].total);
                                    } else {
                                        $('.stockInfoPageAmountOwned').text("0");
                                    }

                                    $('.stockInfoPageTotalCash').text(data.cash);

                                    stockInfoPage.init();
                                } else {
                                    console.log("error selling stock");
                                    //TODO show error
                                }
                            });
                        } else {
                            console.log("nothing happened");
                            //TODO show error
                        }
                    } else {
                        //TODO show error
                    }

                });

                $('#backButton').click(function() {
                    history.back();
                })
            },

            createStockChart : function() {
                var chart = new AmCharts.AmStockChart();

                // DATASETS //////////////////////////////////////////
                var dataSet = new AmCharts.DataSet();
                dataSet.color = "#b0de09";
                dataSet.fieldMappings = [{
                    fromField: "value",
                    toField: "value"
                }];
                dataSet.dataProvider = chartData;
                dataSet.categoryField = "date";

                chart.dataSets = [dataSet];

                // PANELS ///////////////////////////////////////////
                var stockPanel = new AmCharts.StockPanel();
                stockPanel.showCategoryAxis = true;
                stockPanel.title = "Value";
                stockPanel.eraseAll = false;
        //        stockPanel.addLabel(0, 100, "Click on the pencil icon on top-right to start drawing", "center", 16);

                var graph = new AmCharts.StockGraph();
                graph.valueField = "value";
                graph.bullet = "round";
                graph.bulletColor = "#FFFFFF";
                graph.bulletBorderColor = "#00BBCC";
                graph.bulletBorderAlpha = 1;
                graph.bulletBorderThickness = 2;
                graph.bulletSize = 7;
                graph.lineThickness = 2;
                graph.lineColor = "#00BBCC";
                graph.useDataSetColors = false;
                stockPanel.addStockGraph(graph);

                var stockLegend = new AmCharts.StockLegend();
                stockLegend.valueTextRegular = " ";
                stockLegend.markerType = "none";
                stockPanel.stockLegend = stockLegend;
        //        stockPanel.drawingIconsEnabled = true;

                chart.panels = [stockPanel];


                // OTHER SETTINGS ////////////////////////////////////
                var scrollbarSettings = new AmCharts.ChartScrollbarSettings();
                scrollbarSettings.graph = graph;
                scrollbarSettings.updateOnReleaseOnly = false;
                chart.chartScrollbarSettings = scrollbarSettings;

                var cursorSettings = new AmCharts.ChartCursorSettings();
                cursorSettings.valueBalloonsEnabled = true;
                chart.chartCursorSettings = cursorSettings;

                var panelsSettings = new AmCharts.PanelsSettings();
                panelsSettings.creditsPosition = "bottom-right";
                panelsSettings.marginRight = 16;
                panelsSettings.marginLeft = 16;
                chart.panelsSettings = panelsSettings;


                // PERIOD SELECTOR ///////////////////////////////////
                var periodSelector = new AmCharts.PeriodSelector();
                periodSelector.position = "bottom";
                periodSelector.periods = [{
                    period: "DD",
                    count: 10,
                    label: "10 days"
                }, {
                    period: "MM",
                    count: 1,
                    label: "1 month"
                }, {
                    period: "YYYY",
                    count: 1,
                    label: "1 year"
                }, {
                    period: "YTD",
                    label: "YTD"
                }, {
                    period: "MAX",
                    label: "MAX"
                }];
                chart.periodSelector = periodSelector;
                chart.dataDateFormat = "YYYY-MM-DD";

                chart.write('stockGraph');

                var lastDate = chartData[chartData.length - 1]["date"];
                var end = new Date(lastDate);

                // Set it to UTC time. The 22 is to have the end of the graph
                // a little bit to the right of the last point
                end.setHours(end.getHours() + 22 + end.getTimezoneOffset() / 60);
                var start = new Date(end);
                start.setDate(start.getDate() - 31);
                chart.zoom(start, end);
            },

            onPageLoad : function() {

            },

            init : function() {
                stockInfoPage.createStockChart();
                $('#navbarTabs li').removeClass('active');
                $('#stocksTab').addClass('active');
                stockInfoPage.setupButtons();
                stockInfoPage.setupSlider();
            },
        };

        return {
            init : stockInfoPage.init,
            onPageLoad : stockInfoPage.onPageLoad,
        };
    }
})(jQuery);

var StockInfoPage = $.StockInfoPage();

function onStockQuantityInputChange(form, value) {
    form.amountRange.value = value.replace(/[^0-9]/g,'0');
    updateTotalPrice();
}

function onStockQuantityBarChange(form, value) {
    form.amountInput.value=value;
    updateTotalPrice();
}

function updateTotalPrice() {
    var value = $('.stockInfoPage input[name=amountInput]').val().trim();
    var quantity = Utility.isPositiveInteger(value);
    var price = $('.stockInfoPageStockPrice').text();

    var totalPrice = quantity * price + commission;
    $('.stockInfoPageStockTotalPrice').text(totalPrice.toFixed(2));
}

$( document ).ready(function() {
});
