/**
 * The Resources object is responsible for loading and keeping track of resources (i.e. images) that are used in the game.
 * This object also takes in call back functions that will be called when all the images are loaded/ready.
 * Note that this class was written by someone else.
 */
(function($) {
    $.Resources = function() {
        var resourceCache = {};
        var loading = [];
        var readyCallbacks = [];

        var resources = {
            /**
             * Loads a url or an array. If it is an array of urls, loads each element of the array.
             * If it is a url, just loads that url.
             * @param {Object} urlOrArr - a url or an array of urls
             */
            load : function(urlOrArr) {
                if ( urlOrArr instanceof Array) {
                    urlOrArr.forEach(function(url) {
                        resources._load(url);
                    });
                } else {
                    _load(urlOrArr);
                }
            },

            /**
             * If the resource (url) is already in the cache, return it.
             * Otherwise, create an image and add it to the resource cache when it is loaded.
             * Then, when all the resources are ready, execute all of the call back functions.
             * @param {Object} url
             */
            _load : function(url) {
                if (resourceCache[url]) {
                    return resourceCache[url];
                } else {
                    var img = new Image();
                    img.onload = function() {
                        resourceCache[url] = img;

                        if (resources.isReady()) {
                            readyCallbacks.forEach(function(func) {
                                func();
                            });
                        }
                    };
                    resourceCache[url] = false;
                    img.src = url;
                }
            },

            /**
             * Returns the resource corresponding to the url given.
             */
            get : function(url) {
                return resourceCache[url];
            },

            /**
             * Determines if all the resources are ready.
             */
            isReady : function() {
                var ready = true;
                for (var k in resourceCache) {
                    if (resourceCache.hasOwnProperty(k) && !resourceCache[k]) {
                        ready = false;
                    }
                }
                return ready;
            },

            /**
             * Adds a function to the call backs list.
             * @param {Object} func - the function to be executed when all the resources are ready.
             */
            onReady : function(func) {
                readyCallbacks.push(func);
            },
        };
        return {
            load : resources.load,
            get : resources.get,
            onReady : resources.onReady,
            isReady : resources.isReady
        };
    };

})(jQuery); 