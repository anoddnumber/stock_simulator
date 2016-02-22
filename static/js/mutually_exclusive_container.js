(function($) {
    $.MutuallyExclusiveContainer = function(options) {
        var selectors = options.selectors; //an array of IDs (strings) of the components

        var mutuallyExclusiveContainer = {
            options : $.extend({
            }, options),

            show : function(selector) {
                for (var i = 0; i < selectors.length; i++) {
                    if (selector !== selectors[i]) {
                        $(selectors[i]).hide();
                    }
                    $(selector).show();
                }
            },
        }

        return {
            show : mutuallyExclusiveContainer.show,
        };
    };
})(jQuery);