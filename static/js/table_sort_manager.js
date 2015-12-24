/**
* Helps sort tables by column by keeping track of which column is currently sorted and which way it is sorted.
* (can be sorted forward or backwards).
*/
(function($) {
    $.TableSortManager = function(options) {
        var tableSortManager = {
            options : $.extend({
                data : undefined,
                sortedColumn : undefined,
                forward : undefined,
            }, options),

            /**
            * Sorts the data based on sortFunc. If the column is already sorted, toggle the search direction.
            * The sortFunc will automatically be toggled.
            */
            sort : function(colName, sortFunc) {
                console.log("colName: " + colName);
                console.log("tableSortManager.options.forward: " + tableSortManager.options.forward);
                console.log("tableSortManager.options.sortedColumn: " + tableSortManager.options.sortedColumn);
                if (tableSortManager.options.sortedColumn === colName) {
                    if (tableSortManager.options.forward) {
                        tableSortManager.options.forward = false;
                    } else {
                        tableSortManager.options.forward = true;
                    }
                } else {
                    tableSortManager.options.sortedColumn = colName;
                    tableSortManager.options.forward = true;
                }

                console.log("tableSortManager.options.forward 2: " + tableSortManager.options.forward);
                console.log("tableSortManager.options.data: " + tableSortManager.options.data);

                var sortedArray = Utility.sortObj(tableSortManager.options.data, sortFunc);
                if ( ! tableSortManager.options.forward) {
                    return sortedArray.reverse();
                }
                return sortedArray;
            },
        }

        return {
            sort : tableSortManager.sort,
        };
    };
})(jQuery);