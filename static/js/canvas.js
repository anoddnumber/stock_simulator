/**
 * This is the $.Canvas class that contains information about the HTML canvas element.
 * The canvas' attributes will be changed when the canvas is resized due to the browser (including entering and exiting full screen).
 */
(function($) {
    $.Canvas = function() {
        var fontSize = 15;
        var font = fontSize + "px Verdana";
        var canvas = $("#canvas")[0];
        var ctx = canvas.getContext("2d");
        var w, h;
        
        var c = {
            /**
             * Resizes the canvas to the browser size and assigns the internal variables to the appropriate values.
             */
            _resizeCanvas : function() {
                var windowWidth = $(window).width();
                var windowHeight = $(window).height();
                
                canvas.width = windowWidth-10;
                canvas.height = windowHeight-10;
                
                ctx.font = font;
                w = $("#canvas").width();
                h = $("#canvas").height();
            },
            
            /**
             * Returns the width of the canvas (pixels)
             */
            getWidth : function() {
                return w;
            },
            
            /**
             * Returns the height of the canvas (pixels)
             */
            getHeight : function() {
                return h;
            },
            
            /**
             * Returns the context. The context provides methods to actually draw on the canvas.
             */
            getCtx : function() {
                return ctx;
            },
            
            /**
             * Returns the canvas. The canvas is just the container of where graphics will be drawn.
             * Use the canvas' context to draw onto the canvas.
             */
            getCanvas : function() {
                return canvas;
            },
            
            /**
             * Return the font size
             */
            getFontSize : function() {
                return fontSize;
            },
        };
        
        window.addEventListener('resize', c._resizeCanvas, false);
        c._resizeCanvas();
        
        return {
            getWidth : c.getWidth,
            getHeight : c.getHeight,
            getCtx : c.getCtx,
            getCanvas : c.getCanvas,
            getFontSize : c.getFontSize,
        };
    };
})(jQuery);
