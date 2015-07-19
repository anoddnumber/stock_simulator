(function($) {
    $.Simulator = function() {
        var simulator = {
            start : function() {
                var ctx = Canvas.getCtx();
                var playImg = Resources.get('resources/images/play.png');
                ctx.drawImage(playImg, Math.floor((Canvas.getWidth() - playImg.width)/2), Math.floor((Canvas.getHeight() - playImg.height)/2));
                console.log("start");
            },
        };
        
        return {
            start : simulator.start,
        };
    };
})(jQuery);


/**
 * Resources contains all the images used in the game. 
 * All the resources must be loaded before the game is started.
 */
var ready = function() {
    if (document.getElementById('stock_simulator') != null) {
        Simulator = $.Simulator();
        Resources = $.Resources();
        Canvas = $.Canvas();
        
        //paths are relative to index.html
        Resources.load([
            'resources/images/play.png',
        ]);
        
        Resources.onReady(Simulator.start);
    }
};

console.log("hi");
/**
 * Global variables listed here.
 */
var Simulator, Resources, Canvas;
$(document).ready(ready);