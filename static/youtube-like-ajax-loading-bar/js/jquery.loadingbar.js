/* ===========================================================
 * jquery-loadingbar.js v1
 * ===========================================================
 * Copyright 2013 Pete Rojwongsuriya.
 * http://www.thepetedesign.com
 *
 * Add a Youtube-like loading bar  
 * to all your AJAX links 
 *
 * https://github.com/peachananr/loading-bar
 *
 * ========================================================== */

!function($){
  
  var defaults = {
		replaceURL: false,
		target: "#loadingbar-frame",
		direction: "right",
		
		/* Deafult Ajax Parameters  */
		async: true,
		complete: function(xhr, text) {},
		cache: true,
		error: function(xhr, text, e) {},
		global: true,
		headers: {},
		statusCode: {},
		success: function(data, text, xhr) {},
		dataType: "html"
	};
	
	$.fx.step.textShadowBlur = function(fx) {
    $(fx.elem).prop('textShadowBlur', fx.now).css({textShadow: '0 0 ' + Math.floor(fx.now) + 'px black'});
  };
  
	
  $.fn.loadingbar = function(options){
    var settings = $.extend({}, defaults, options),
        el = $(this),
        href = el.attr("href"),
        target = (el.data("target")) ? el.data("target") : settings.target,
        type = (el.data("type")) ? el.data("type") : settings.type,
        datatype = (el.data("datatype")) ? el.data("datatype") : settings.dataType

    return this.each(function(){
      el.click(function (e){
        // keep the default behavior for middle click (open in new tab)
        if (e.which == 2) {
            // "a" elements open new tabs by default so we don't want to open another tab.
            // Other elements will need to be told to open a new tab. (Like the data tables)
            if ( ! el.is("a")) {
                window.open(href);
            }
            return;
        }

        $.ajax({
          type: type,
          url: href,
          async: settings.async,
          complete: settings.complete,
          cache: settings.cache,
          error: settings.error,
          global: settings.global,
          headers: settings.headers,
          statusCode: settings.statusCode,
          success: settings.success,
          dataType : datatype,
          beforeSend: function() {
            if ($("#loadingbar").length === 0) {
              $("body").append("<div id='loadingbar'></div>")
              $("#loadingbar").addClass("waiting").append($("<dt/><dd/>"));
              
              switch (settings.direction) { 
                case 'right':
                   $("#loadingbar").width((50 + Math.random() * 30) + "%");
                  break;
                case 'left':
                   $("#loadingbar").addClass("left").animate({
                     right: 0,
                     left: 100 - (50 + Math.random() * 30) + "%"
                   }, 200);
                  break;
                case 'down':
                   $("#loadingbar").addClass("down").animate({
                     left: 0,
                     height: (50 + Math.random() * 30) + "%"
                   }, 200);
                  break;
                case 'up':
                   $("#loadingbar").addClass("up").animate({
                     left: 0,
                     top: 100 - (50 + Math.random() * 30) + "%"
                   }, 200);
                  break;
              }
             
            }
          }
        }).always(function() {
          switch (settings.direction) { 
            case 'right':
               $("#loadingbar").width("101%").delay(200).fadeOut(400, function() {
                   $(this).remove();
               });
              break;
            case 'left':
               $("#loadingbar").css("left","0").delay(200).fadeOut(400, function() {
                    $(this).remove();
                });
              break;
            case 'down':
                $("#loadingbar").height("101%").delay(200).fadeOut(400, function() {
                     $(this).remove();
                 });
               break;
            case 'up':
                $("#loadingbar").css("top", "0").delay(200).fadeOut(400, function() {
                     $(this).remove();
                 });
               break;
          }
          
        }).done(function(data) {
          if ( history.replaceState && settings.replaceURL == true ) history.pushState( {}, document.title, href );
          if (settings.done) {
            settings.done(data, target)
          } else {
            $(target).html(data)
          }
          
        });
        return false
      });


    });
  }
  
}(window.jQuery);

$( document ).ready(function() {

    $(window).unbind('popstate');
    $(window).bind('popstate', function(){
        href = window.location.href;
        target = "#loadingbar-frame";
        direction = "right"

        $.ajax({
              type: undefined,
              url: href,
              async: true,
              complete: function(xhr, text) {},
              cache: true,
              error: function(xhr, text) {},
              global: true,
              headers: {},
              statusCode: {},
              success: function(xhr, text) {},
              dataType : "html",
              beforeSend: function() {
                if ($("#loadingbar").length === 0) {
                  $("body").append("<div id='loadingbar'></div>")
                  $("#loadingbar").addClass("waiting").append($("<dt/><dd/>"));

                  switch (direction) {
                    case 'right':
                       $("#loadingbar").width((50 + Math.random() * 30) + "%");
                      break;
                    case 'left':
                       $("#loadingbar").addClass("left").animate({
                         right: 0,
                         left: 100 - (50 + Math.random() * 30) + "%"
                       }, 200);
                      break;
                    case 'down':
                       $("#loadingbar").addClass("down").animate({
                         left: 0,
                         height: (50 + Math.random() * 30) + "%"
                       }, 200);
                      break;
                    case 'up':
                       $("#loadingbar").addClass("up").animate({
                         left: 0,
                         top: 100 - (50 + Math.random() * 30) + "%"
                       }, 200);
                      break;
                  }

                }
              }
            }).always(function() {
              switch (direction) {
                case 'right':
                   $("#loadingbar").width("101%").delay(200).fadeOut(400, function() {
                       $(this).remove();
                   });
                  break;
                case 'left':
                   $("#loadingbar").css("left","0").delay(200).fadeOut(400, function() {
                        $(this).remove();
                    });
                  break;
                case 'down':
                    $("#loadingbar").height("101%").delay(200).fadeOut(400, function() {
                         $(this).remove();
                     });
                   break;
                case 'up':
                    $("#loadingbar").css("top", "0").delay(200).fadeOut(400, function() {
                         $(this).remove();
                     });
                   break;

              }
            }).done(function(data) {
                var simulator = $(data).find("#stock_simulator");
                $(target).html(simulator);
            });
            return false;
    });

});