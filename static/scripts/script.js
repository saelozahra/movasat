jQuery(document).ready(function(){

    jQuery("audio").each(function(){
        var datatitle = jQuery(this).parent().find('figcaption').text();
        if(datatitle.length<18){
            var datatitle = document.title;
        }
        jQuery("audio").attr('data-title',datatitle);
    });
    
    jQuery('audio:not(.simple), video:not(.simple)').stylise();
	
	
	if(isFunction(jQuery(".scrollbar").mCustomScrollbar)){
		jQuery(".scrollbar").mCustomScrollbar({
			autoHideScrollbar:true,
			theme:"rounded-dots-dark",
			scrollInertia:400
		});
		
	}
	
//	if(isFunction(Tipped)){
		Tipped.create('.tooltip', {
			size: 'large',
			behavior: 'mouse',
			fadeIn: 313,
			fadeOut: 888,
		});
//	}
	
    if( jQuery('#podcast .hover-bg').length ){
        var podcastGranimInstance = new Granim({
            element: '#podcast .hover-bg',
            direction: 'radial',
            isPausedWhenNotInView: true,
            states : {
                "default-state": {
                    gradients: [
                        ['#6CAF00', '#146C20'],
                        ['#055b11', '#088C20'],
                        ['#7DC826', '#64CB77'],
                        ['#146C20', '#6CAF00']
                    ],
                    transitionSpeed: 1313,
                }
            }
        });
    }
	
	
    if( jQuery('#gozareshtasviri .hover-bg').length ){
        var gozareshtasviriGranimInstance = new Granim({
            element: '#gozareshtasviri .hover-bg',
            direction: 'radial',
            isPausedWhenNotInView: true,
            states : {
                "default-state": {
                    gradients: [
                        ['#EFDCE0', '#ffffff'],
                        ['#FFFCFF', '#D5FEFD'],
                        ['#CACCD1', '#ffffff']
                    ],
                    transitionSpeed: 1313,
                }
            }
        });
    }
	
	
	
    if( jQuery('#lastContent .hover-bg').length ){
        var lastContentGranimInstance = new Granim({
            element: '#lastContent .hover-bg',
            direction: 'radial',
            isPausedWhenNotInView: true,
            states : {
                "default-state": {
                    gradients: [
                        ['#343434', '#676767'],
                        ['#616161', '#959595'],
                        ['#594635', '#616161']
                    ],
                    transitionSpeed: 1313,
                }
            }
        });
    }


    if( jQuery('header #fixed-nav canvas').length ){
        var granimInstance = new Granim({
            element: 'header #fixed-nav canvas',
            direction: 'diagonal',
            isPausedWhenNotInView: true,
            states : {
                "default-state": {
                    gradients: [
                        ['#E6A50F', '#F7C85B'],
                        ['#F1C254', '#E6A50F'],
                        ['#F7C85B', '#F1C254']
                    ],
                    transitionSpeed: 1313,
                }
            }
        });
    }
	
	
	
	
	
    if( jQuery('#fullpage').length ){
		var myFullpage = new fullpage('#fullpage', {
			verticalCentered: true,
			navigation: true,
			slidesNavigation: true,
			sectionsColor: ['#E6A50F', '#FAD74E', '#755508'],
			afterLoad: function(origin, destination, direction){
				var params = {
					origin: origin,
					destination: destination,
					direction: direction
				};

				console.log("--- afterLoad ---");
				console.log(params);
				console.log(destination['index']);
					
				
				gozareshtasviriGranimInstance.pause();
				podcastGranimInstance.pause();
				lastContentGranimInstance.pause();
				
				switch(destination['index']) {
				  case 0:
					break;
				  case 1:
					gozareshtasviriGranimInstance.play();
					break;
				  case 2:
					podcastGranimInstance.play();
					break;
				  case 3:
					lastContentGranimInstance.play();
					break;
				}
			}
		});
	}

	
	if( jQuery('.home-slider,.row-slider').length ){
		jQuery(".home-slider,.row-slider").owlCarousel({
			loop:false,
			margin:10,
			dots:true,
			nav:true,
			autoplay:true,
			items:1,
		});
	}
	
	
    if( jQuery('#background_audio').length ){

		var myAudio = document.getElementById("background_audio");
		var isPlaying = false;

		function togglePlay() {
		  isPlaying ? myAudio.pause() : myAudio.play();
		};

		myAudio.onplaying = function() {
		  isPlaying = true;
		};
		myAudio.onpause = function() {
		  isPlaying = false;
		};
		jQuery(".mediaplayer").click(function(){
			togglePlay();
		});

//		setTimeout(function(){
//			myAudio.play();
//		}, 2000);


	}
	
	
	
	
	
	
	
	if( jQuery('#lastContent .owl-carousel').length ){
		
		var $lastContent = jQuery( '#lastContent .owl-carousel' );

		$lastContent.owlCarousel({
			loop:true,
			margin:10,
			dots:true,
			nav:true,
			navText:["<i class='mdi mdi-arrow-right-drop-circle'></i>","<i class='mdi mdi-arrow-left-drop-circle'></i>"],
			autoplay:true,
			responsive:{
				0:{
					items:1
				},
				300:{
					items:2
				},
				600:{
					items:3
				},
				1400:{
					items:4
				}
			}
		});
		

		// $lastContent.on('mousewheel', '.owl-stage', function (e) {
		// 	if (e.deltaY>0) {
		// 		$timeline_archive.trigger('next.owl');
		// 	} else {
		// 		$timeline_archive.trigger('prev.owl');
		// 	}
		// 	e.preventDefault();
		// });

	}
	
    jQuery(".tab_title").click(function(){
        jQuery(".tab_title").attr("data-active", "false");
		jQuery(this).attr("data-active", "true");
		
		
        jQuery(".tab_content").attr("data-active", "false");
		jQuery('.tab_content[data-id="'+jQuery(this).attr("data-id")+'"]').attr("data-active", "true");
		
		jQuery('.tab_content .left_sld').fadeOut(0);
		jQuery('.tab_content[data-id="'+jQuery(this).attr("data-id")+'"] .left_sld').fadeIn(313);
		
    });
	
	
	
	
	
	
	
    
    jQuery(window).scroll(function() {
        if (jQuery(document).scrollTop() > 313) {
            jQuery("header").addClass("fixed");
        } else {
            jQuery("header").removeClass("fixed");
        }
    });
    
    jQuery(window).scroll(function() {
        if (jQuery(document).scrollTop() > 1100) {
            jQuery("body").addClass("fixed");
        } else {
            jQuery("body").removeClass("fixed");
        }
    });
    

    
    jQuery('#addtobookmark').click(function() {
        if (window.sidebar && window.sidebar.addPanel) { // Mozilla Firefox Bookmark
          window.sidebar.addPanel(document.title, window.location.href, '');
        } else if (window.external && ('AddFavorite' in window.external)) { // IE Favorite
          window.external.AddFavorite(location.href, document.title);
        } else if (window.opera && window.print) { // Opera Hotlist
          this.title = document.title;
          return true;
        } else { // webkit - safari/chrome
          alert('کلید های  ' + (navigator.userAgent.toLowerCase().indexOf('mac') != -1 ? 'Command/Cmd' : 'CTRL') + ' + D را برای اضافه شدن به لیست مورد علاقه ها فشار دهید.');
        }
        return false;
    });
    
    if( jQuery('#tags').length ){
        jQuery('#tags a').addClass("mdi mdi-24px");
    }
    
    
    if( jQuery('.btn_archive_style').length ){
        
        jQuery(".btn_archive_style").click(function(){
			
            document.cookie = "archive_show_type="+jQuery(this).attr('data-value');
            
            jQuery('.btn_archive_style').removeClass('selected');
            jQuery(this).addClass('selected');
            jQuery('#archive_items_section').removeClass('two-columns-width four-columns-width list');
            jQuery('#archive_items_section').addClass( 'row '+ jQuery(this).attr('data-value') );
        });
        
        if(getCookie("archive_show_type")!=""){
            jQuery('#archive_items_section').addClass( 'row '+getCookie("archive_show_type") );
            jQuery('.btn_archive_style').removeClass('selected');
            jQuery('.btn_archive_style[data-value="'+getCookie("archive_show_type")+'"]').addClass('selected');
        }
        
    }
    
    if( jQuery('#like').length ){
        
        var my_id = jQuery("#like").attr('data-id');
        if( getCookie("liked"+my_id)=="true" ){
            jQuery("#like i").removeClass('mdi-heart-multiple-outline');
            jQuery("#like i").addClass('mdi-heart');
            jQuery("#like i").css({'color':'red','cursor':'not-allowed'});
        }else{
            jQuery("#like").click(function(){
                if( getCookie("liked"+my_id)!="true" ){
                    jQuery.post(jQuery(this).attr('data-url'),{
                      like: my_id,
                    },function(data,status){
                        document.cookie = "like="+my_id;
                        document.cookie = "liked"+my_id+"=true";
                        jQuery("#like i").removeClass('mdi-heart-multiple-outline');
                        jQuery("#like i").addClass('mdi-heart');
                        jQuery("#like i").css({'color':'red','cursor':'not-allowed'});
                    });
                }
                return false;
            });
        }
    }
    
    
    

    if( jQuery('#wpp_jcalendar-2').length ){
        var inMah = jQuery('#wpp_jcalendar-2').find("caption").text();
        jQuery('#wpp_jcalendar-2').find('.outer_div_title').text('تقویم '+inMah);
        jQuery('#wpp_jcalendar-2').find("caption").remove();
        jQuery('#wpp_jcalendar-2').find("tfoot").css( {"position":"absolute", "left":0, "bottom":0, "color":"var(--color-light)"} );
        jQuery('#wpp_jcalendar-2').find("tfoot").find("a").css( {"position":"absolute", "left":0, "bottom":0, "width":"max-content", "color":"var(--color-light)"} );
        jQuery('#wpp_jcalendar-2').find("#wp-calendar").css("position","relative");
    }




    if( jQuery('#rss-2').length ){
        jQuery('#rss-2').find("ul").attr("data-mcs-theme","rounded-dots-dark");
        jQuery('#rss-2').find("ul").addClass("scrollbar mCustomScrollbar mCS-autoHide");
        jQuery('#rss-2').find("ul").css("height","202px");
        jQuery('#rss-2').find(".mCSB_container").css("margin-left",0);
        jQuery('#rss-2').parent().css("padding-left",0);
    }



    $('#bookmarkme').click(function() {
        if (window.sidebar && window.sidebar.addPanel) { // Mozilla Firefox Bookmark
            window.sidebar.addPanel(document.title, window.location.href, '');
        } else if (window.external && ('AddFavorite' in window.external)) { // IE Favorite
            window.external.AddFavorite(location.href, document.title);
        } else if (window.opera && window.print) { // Opera Hotlist
            this.title = document.title;
            return true;
        } else { // webkit - safari/chrome
            alert('دکمه  ' + (navigator.userAgent.toLowerCase().indexOf('mac') != -1 ? 'Command/Cmd' : 'CTRL') + ' + D را فشار دهید تا به لیست افزوده شود');
        }
    });
	
	
	
    
    function getCookie(cname){
      var name = cname + "=";
      var ca = document.cookie.split(';');
      for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    }
    
	function isFunction(functionToCheck) {
		return functionToCheck && {}.toString.call(functionToCheck) === '[object Function]';
	}





    const settings = {
      "async": true,
      "crossDomain": true,
      // "url": "https://jahadgaran.org/wp-json/wp/v2/posts",
      "url": "http://hajghasem.ir/wp-json/wp/v2/posts",
      "method": "GET",
      "headers": {}
    };

    $.ajax(settings).done(function (response) {
        $.each(response, function(i, item) {
            $(".newsTickerContainer .newsTicker").append("<a class='row' href='"+response[i].link+"'><h4 class='row white-space'>"+response[i].title.rendered+"</h4></a>");
        });

		jQuery(".newsTickerContainer .newsTicker").owlCarousel({
			loop:true,
			margin:10,
			dots:false,
			nav:false,
			autoplay:true,
			items:1,
		});
    });



	
});