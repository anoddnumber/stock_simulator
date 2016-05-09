(function($) {
    $.StockInfoPage = function(options) {
        var stockInfoPage = {
             options : $.extend({
             }, options),

             setupSlider : function() {
                $('.stockInfoPageStockTotalPrice').text("0.00");

                var cash = $('.stockInfoPageTotalCash').text();
                var price = $('.stockInfoPageStockPrice').text();
                var numOwned = $('.stockInfoPageAmountOwned').text();

                // by default, the buy radio button is selected
                // TODO refactor to make a "set slider bar max/min" function
                $(".stockInfoPage .buyStockRadioButton").prop("checked", true);
                $('.stockInfoPage input').attr({
                    "min" : 0,
                    "max" : Math.floor(cash / price),
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
                            ApiClient.sellStock(symbol, quantity, price, function(data) {
                                data = JSON.parse(data);

                                if (data.stocks_owned[symbol]) {
                                    $('.stockInfoPageAmountOwned').text(data.stocks_owned[symbol].total);
                                } else {
                                    $('.stockInfoPageAmountOwned').text("0");
                                }

                                $('.stockInfoPageTotalCash').text(data.cash);

                                stockInfoPage.init();
                            });
                        } else {
                            console.log("nothing happened");
                            //TODO show error
                        }
                    } else {
                        //TODO show error
                    }

                });
            },

            init : function() {
                stockInfoPage.setupButtons();
                stockInfoPage.setupSlider();
            },
        };

        return {
            init : stockInfoPage.init,
        };
    }
})(jQuery);

var StockInfoPage = $.StockInfoPage();

$( document ).ready(function() {
    var path = window.document.location.pathname;
    if (path.indexOf("stock/") > -1) {
        StockInfoPage.init();
    }
});

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
    var commission = 0;

    var totalPrice = quantity * price + commission;
    $('.stockInfoPageStockTotalPrice').text(totalPrice.toFixed(2));
}