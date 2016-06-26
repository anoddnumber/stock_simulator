var userInfo;
var stockSymbolsMap;

(function($) {
    $.Utility = function(options) {
        var utility = {
            /*
             * If one of the properties is undefined or an empty string, return the property.
             * Otherwise returns false.
             */
            hasEmptyValue : function(object) {
                for (var property in object) {
                    /*
                     * hasOwnProperty is necessary because an object's prototype contains additional properties for the object which are technically part of the object.
                     * These additional properties are inherited from the base object class, but are still properties of object.
                     * hasOwnProperty simply checks to see if this is a property specific to this class, and not one inherited from the base class.
                     */
                    if (object.hasOwnProperty(property)) {
                        if (object[property] === undefined || object[property] === '') {
                            return property;
                        }
                    }
                }
                return false;
            },

            /**
             * Inserts the value into the stocks table as a row of its own.
             *
             * value - the string to be inserted
             */
            insertRowByValue : function(tableId, value) {
                utility.insertRowByValues(tableId, [value]);
            },

            /**
             * Inserts the given values into ths table with id tableId. Each element in values will be in a new cell
             *
             * values - an array of strings to be inserted
             */
            insertRowByValues : function(tableId, values) {
                var table = $('#' + tableId)[0]; //grab the DOM element (0 indexed element of a jQuery object)
                var row = table.insertRow(-1);
                for (var i = 0; i < values.length; i++) {
                    row.insertCell(-1).innerHTML = values[i];
                }
            },

            /**
            *   Inserts an entire table in all at once. Uses an array and strings to build up the table
            *   for efficiency.
            *
            *   values - 2d array, each array is a row in the table
            */
            insertEntireTableBody : function(tableElem, values) {
                var result = new Array(), index = -1;

                for (var i = 0; i < values.length; i++) {
                    var row = values[i];
                    result.push('<tr>');
                    for (var j = 0; j < row.length; j++) {
                        result.push('<td>');
                        result.push(row[j]);
                        result.push('</td>');
                    }
                    result.push('</tr>');
                }
                tableElem.innerHTML = result.join('');
            },

            /**
             * Replaces all the characters that match "find" in "str" with "replace"
             * @param {Object} find - the characters to replace
             * @param {Object} replace - the character to replace with
             * @param {Object} str - the string that will change
             */
            replaceAll : function(find, replace, str) {
                return str.replace(new RegExp(find, 'g'), replace);
            },

            isPositiveInteger : function(str) {
                if (str.indexOf('.') < 0) {
                    var num = parseInt(str);
                    if (num && num > 0) {
                        return num;
                    }
                }
                return false;
            },

            getPercentDifference : function(oldNum, newNum) {
                return (newNum - oldNum)/oldNum * 100;
            },

            replaceUrlParam : function(url, paramName, paramValue) {
                var pattern = new RegExp('\\b('+paramName+'=).*?(&|$)')
                if(url.search(pattern)>=0){
                    return url.replace(pattern,'$1' + paramValue + '$2');
                }
                return url + (url.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue
            },

            getUrlParameter : function(sParam) {
                var sPageURL = decodeURIComponent(window.location.search.substring(1)),
                    sURLVariables = sPageURL.split('&'),
                    sParameterName,
                    i;

                for (i = 0; i < sURLVariables.length; i++) {
                    sParameterName = sURLVariables[i].split('=');

                    if (sParameterName[0] === sParam) {
                        return sParameterName[1] === undefined ? true : sParameterName[1];
                    }
                }
            },

            // used to modify the page parameter in the URL (i.e. /stocks?page=3) for datatables
            modifyPageParam : function(table) {
                var info = table.page.info();

                // info.page has a range of [0, info.pages)
                var url = document.URL;     // Returns full URL
                var newUrl = window.location.href.split('?')[0];

                if (info.page != 0) {
                    newUrl = Utility.replaceUrlParam(url, "page", info.page + 1);
                }

                history.pushState( {}, document.title, newUrl);
            }
        }

        return {
            hasEmptyValue : utility.hasEmptyValue,
            insertRowByValue : utility.insertRowByValue,
            insertRowByValues : utility.insertRowByValues,
            isPositiveInteger : utility.isPositiveInteger,
            getPercentDifference : utility.getPercentDifference,
            insertEntireTableBody : utility.insertEntireTableBody,
            replaceAll : utility.replaceAll,
            replaceUrlParam : utility.replaceUrlParam,
            getUrlParameter : utility.getUrlParameter,
            modifyPageParam : utility.modifyPageParam
        };
    };
})(jQuery);

var Utility = $.Utility();
$( document ).ready(function() {
});

/*
Random notes about useful methods:
JSON.stringify(obj) - use to print out json rather than getting [Object] in the console
.toFixed(n) - round to n decimal places
*/