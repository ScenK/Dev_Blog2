jQuery(function(){
		
	window.head = $('#head > div');
		
	window.wing_one = $('#wing-one span');
	window.wing_two = $('#wing-two span');
		
	window.left_eyebrow = $('#left-eye .eyebrow span');
	window.right_eyebrow = $('#right-eye .eyebrow span');
		
	window.left_eye_pupil = $('#left-eye .eye-pupil');
	window.right_eye_pupil = $('#right-eye .eye-pupil');
		
	window.leg_one = $('.legs-a span');
	window.leg_two = $('.legs-b span');
	
	head.css({transformOrigin: "0% 0%"});
	wing_one.css({transformOrigin: "100% 100%"});
	wing_two.css({transformOrigin: "0% 100%"});
	left_eyebrow.css({transformOrigin: "50% 50%"});
	right_eyebrow.css({transformOrigin: "50% 50%"});
	left_eye_pupil.css({transformOrigin: "0% 0%"});
	right_eye_pupil.css({transformOrigin: "0% 0%"});
	leg_one.css({transformOrigin: "0% 0%"});
	leg_two.css({transformOrigin: "0% 0%"});
	
	function wingsTime() {
		if ($.browser.msie && $.browser.version < 10) {
			wing_one.animate({ left:92, top:160}, 400)
						  .animate({  left:84, top:170}, 400)
						  .animate({left:78, top:175}, 400)
						  .animate({left:84, top:170}, 400)
				
			
			wing_two.animate({ right:95, top:160}, 400)
						  .animate({right:87, top:170}, 400)
						  .animate({right:81, top:175}, 400)
						  .animate({right:87, top:170}, 400)	
		}
		else{
		
			wing_one.animate({  transform: 'rotate(0deg)'}, 100, function() {
				})
					.animate({  transform: 'rotate(-10deg)'}, 100, function() {
					})
					.animate({  transform: 'rotate(-15deg)'}, 100, function() {
						})
					.animate({  transform: 'rotate(-20deg)'}, 100, function() {
					})
					.animate({  transform: 'rotate(-15deg)'}, 100, function() {})
					.animate({  transform: 'rotate(-10deg)'}, 100, function() {})
					.animate({  transform: 'rotate(0deg)'}, 200, function() {})
					.animate({  transform: 'rotate(10deg)'}, 100, function() {})
					.animate({  transform: 'rotate(15deg)'}, 100, function() {})
					.animate({  transform: 'rotate(10deg)'}, 100, function() {})
					.animate({  transform: 'rotate(0deg)'}, 100, function() {});
		
			wing_two.animate({  transform: 'rotate(0deg)'}, 100, function() {})
					.animate({  transform: 'rotate(10deg)'}, 100, function() {})
					.animate({  transform: 'rotate(15deg)'}, 100, function() {})
					.animate({  transform: 'rotate(20deg)'}, 100, function() {})
					.animate({  transform: 'rotate(15deg)'}, 100, function() {})
					.animate({  transform: 'rotate(10deg)'}, 100, function() {})
					.animate({  transform: 'rotate(0deg)'}, 200, function() {})		
					.animate({  transform: 'rotate(-10deg)'}, 100, function() {})
					.animate({  transform: 'rotate(-15deg)'}, 100, function() {})
					.animate({  transform: 'rotate(-10deg)'}, 100, function() {})
					.animate({  transform: 'rotate(0deg)'}, 100, function() {})	;
		}
		
	}
		
	IntervalWings = setInterval(wingsTime, 200);
	
	//Eyes
	function eyeBrowTime() {
		if ($.browser.msie && $.browser.version < 10) {
			left_eyebrow.animate({ left:8, top:-23}, 800)
						  .animate({  left:5, top:-20}, 800)
						  .animate({left:3, top:-18}, 800)
						  .animate({left:5, top:-20}, 800)
				
			
			right_eyebrow.animate({ left:-6, top:-23}, 800)
						  .animate({left:-3, top:-20}, 800)
						  .animate({left:-1, top:-18}, 800)
						  .animate({left:-3, top:-20}, 800)
		}
		 else{
			left_eyebrow.animate({transform: 'rotate(0deg)'}, 1000, function(){})
						.animate({  transform: 'rotate(5deg)'}, 1000, function() {})
						.animate({  transform: 'rotate(10deg)'}, 1000, function() {})
						.animate({  transform: 'rotate(15deg)'}, 1000, function() {})
							.animate({  transform: 'rotate(10deg)'}, 1000, function() {})	
							.animate({  transform: 'rotate(5deg)'}, 1000, function() {})	
							.animate({  transform: 'rotate(0deg)'}, 1000, function() {});																	
			
			right_eyebrow.animate({transform: 'rotate(0deg)'}, 1000, function(){})
						.animate({  transform: 'rotate(-5deg)'}, 1000, function() {})
						.animate({  transform: 'rotate(-10deg)'}, 1000, function() {})
						.animate({  transform: 'rotate(-15deg)'}, 1000, function() {})
						.animate({  transform: 'rotate(-10deg)'}, 1000, function() {})
						.animate({  transform: 'rotate(-5deg)'}, 1000, function() {})		
						.animate({  transform: 'rotate(0deg)'}, 1000, function() {});
		 }
	}
	
	
	IntervalEyebrow = setInterval(eyeBrowTime, 3000);
	
	function eyeTime() {
		 if ($.browser.msie && $.browser.version < 10) {
			 left_eye_pupil.animate({ left:31}, 2000)
						  .animate({  left:26}, 2000)
						  .animate({left:19, top:7}, 2000)
						  .animate({left:26}, 2000)
				
			
			right_eye_pupil.animate({ left:17, top:7}, 2000)
						  .animate({  left:10}, 2000)
						  .animate({left:8}, 2000)
						  .animate({left:10}, 2000)	
											
			 
		}
		 else {	
			left_eye_pupil.animate({ transform: 'translateX(5px)'}, 2000, function() {})
						  .animate({   transform: 'translateX(0px)'}, 2000, function() {})
						  .animate({transform: 'translateX(-5px)'}, 2000, function() {})
				
			
			right_eye_pupil.animate({transform: 'translateX(5px)'}, 2000, function() {})
							.animate({   transform: 'translateX(0px)'}, 2000, function() {})
							.animate({transform: 'translateX(-5px)'}, 2000, function() {});	
							//counter++	
						
			 }

	};

	IntervalEye = setInterval(eyeTime, 6000);
	
	
		function legsTime() {
			 if ($.browser.msie && $.browser.version  < 10 || $.browser.opera) {
				  leg_one.animate({ left:22, top:-6}, 400)
								  .animate({  left:20, top:-4}, 400)
								  .animate({left:18, top:-3}, 400)
								  .animate({left:20, top:-4}, 400)
						
					
					leg_two.animate({ right:-14, top:-5}, 400)
								  .animate({right:-15, top:-7}, 400)
								  .animate({right:-17, top:-2}, 400)
								  .animate({right:-15, top:-7}, 400)
				}
	
			 else {
	//Legs animate
		
				/*leg_one.animate({  transform: 'rotate(0deg) translate(0px)'}, 300, function() {})
						.animate({  transform: 'rotate(-1deg) translate(3px,1px)'}, 300, function() {})
						.animate({  transform: 'rotate(0deg) translate(0px)'}, 300, function() {})
						.animate({  transform: 'rotate(1deg) translate(-3px,-1px)'}, 300, function() {})
						.animate({  transform: 'rotate(0deg) translate(0px)'}, 300, function() {});
						
				leg_two.animate({  transform: 'rotate(0deg) translate(0px)'}, 300, function() {})
						.animate({  transform: 'rotate(1deg) translate(3px,1px)'}, 300, function() {})
						.animate({  transform: 'rotate(0deg) translate(0px)'}, 300, function() {})
						.animate({  transform: 'rotate(-1deg) translate(-3px,-1px)'}, 300, function() {})
						.animate({  transform: 'rotate(0deg) translate(0px)'}, 300, function() {});*/
						
			}
		}
		Interval5 = setInterval(legsTime, 500);
	
	$(window).resize(function () {

		var top = ($(window).height()-(712+56))/2;
		if(top > 20){
			$("#wraper").css({
				"padding-top" : top+"px"
			});
		} else {
			$("#wraper").css({
				"padding-top" : "20px"
			});
		}

		$('#nav').css({				  
			left: ($(window).width() - $('#nav').width())/2	
		})
		var width_bot_l = $('#nav').offset().left;
		$('.bot-l').css({
			width: width_bot_l
		})
		$('.bot-r').css({
			width: $(window).width() - ($('.bot-l').width() + $('#nav').width())
		})
	})
	$(window).resize();
})
	
jQuery(function() {	
	function CircleArc(i){
		var SineWave = function() {
			this.css = function(p) {
				if (p <= 1 && p >= 0.5) {
					var x = 120 - p*160;
					var y = 30*Math.sin(p*4*Math.PI);
				} else {
					var x = p*160 - 40;
					var y = 30*Math.sin(p*4*Math.PI);
				}
				return {top: y + "px", left: x + "px"}
			} 
		};
		$("#head").animate({			 
			path : new SineWave
		}, 10000, "linear", CircleArc);
	};			
	CircleArc();
});
