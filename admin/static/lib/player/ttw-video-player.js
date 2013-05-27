/**
 * Created by 23rd and Walnut for Codebasehero.com
 * www.23andwalnut.com
 * www.codebasehero.com
 * User: Saleem El-Amin
 * Date: 7/20/11
 * Time: 6:41 AM
 *
 * Version: 1.00
 * License: You are free to use this file in personal and commercial products, however re-distribution 'as-is' without prior consent is prohibited.
 */

(function($) {
    $.fn.ttwVideoPlayer = function(arg1) {

        var data,
            mb = this.data('ttwVideoPlayer');

        // Method calling logic
        if (typeof mb !== 'undefined' && mb.api[arg1]) {

            var apiFunctionArgs = Array.prototype.slice.call(arguments, 1);

            return mb.api[arg1].apply(this, apiFunctionArgs);
        }
        else if (typeof arg1 === 'object') {

            //add the media box class
            this.addClass('ttwVideoPlayer');

            //create the media box object
            mb = new $.ttwVideoPlayer(this, arg1, arguments[1]);

            //save a reference to the media box object on the relevant selector
            this.data('ttwMediaBox', mb);

            return this;
        }
        else {
            $.error(arg1 + ' is not a valid method or playlist for ttwVideoPlayer');
        }
    };

    $.ttwVideoPlayer = function(anchor, playlist, userOptions) {
        var $self = anchor , self = this, defaultOptions, options, cssSelector, appMgr, playlistMgr, interfaceMgr, playlist,
                layout,  myPlaylist, current, fullscreen = false, $myJplayer = {}, validButtons, jPlayerDefaults, jPlayerOptions;

        cssSelector = {
            main:'.ttw-video-player ',
            jPlayer: "#jquery_jplayer",
            jPlayerContainer: '.jPlayer-container',
            jPlayerInterface: '.jp-interface',
            playerPrevious: ".jp-interface .jp-previous",
            playerNext: ".jp-interface .jp-next",
            playlist:'.playlist',
            playlistItems:'.playlist-items',
            playlistItem:'.playlist-item',
            playing:'.playing',
            player:'.player',
            progress:'.progress-wrapper',
            volume:'.volume-wrapper',
            playerControls:'.player-controls',
            playlistButton:'.playlist-button',
            hdButton:'.hd-button',
            heartButton:'.heart-button',
            settingsButton:'.settings-button',
            fullscreenButton:'.fullscreen-button',
            heartCount:'.heart-count',
            scrollViewport:'.viewport'
        };

        validButtons = ['playlist', 'hd', 'heart', 'settings', 'fullscreen'];

        defaultOptions = {
            autoplay:false,
            autoHidePlaylist:true,
            autoHidePlaylistDelay:3000,
            jPlayer:{},
            buttons:['playlist', 'hd', 'heart', 'settings'],
            width: "554px",
            height: "312px",
            allowHeartIncrement:function(){
                return true;
            }
        };

        this.heartCount = 0;

        this.api = {
            updateHeartCount: function(){
                layout.updateHeartCount();
            }
        };

        options = $.extend(true, {}, defaultOptions, userOptions);

        myPlaylist = playlist;

        current = 0;

        appMgr = function() {
            debugMessage('Starting');
            
            playlist = new playlistMgr();
            layout = new interfaceMgr();

            layout.buildInterface();
            playlist.init(options.jPlayer);
        
            $self.bind('mbPlaylistLoaded', function() {
                layout.init();
            });
        };
        


        playlistMgr = function() {

            var playing = false;


            function init(playlistOptions) {


                $myJplayer = $(cssSelector.main).find('.jPlayer-container');

                jPlayerDefaults = {
                    swfPath: "jquery-jplayer",
                    supplied: "mp3, m4a, m4v, oga, ogv, wav",
                    cssSelectorAncestor:  cssSelector.jPlayerInterface,
                    errorAlerts: false,
                    warningAlerts: false,
                    size: {
                        height:options.height,
                        width:options.width,
                        cssClass: "show-video"
                    },
                    sizeFull: {
                        width: "100%",
                        height: "90%",
                        cssClass: "show-video-full"
                    }
                };

                //apply any user defined jPlayer options
                jPlayerOptions = $.extend(true, {}, jPlayerDefaults, playlistOptions);
                
                $myJplayer.bind($.jPlayer.event.ready, function() {

                    debugMessage('jPlayer Ready');
                    
                    //Bind jPlayer events. Do not want to pass in options object to prevent them from being overridden by the user
                    $myJplayer.bind($.jPlayer.event.ended, function(event) {
                        playlistNext();
                    });

                    $myJplayer.bind($.jPlayer.event.play, function(event) {
                        $myJplayer.jPlayer("pauseOthers");
             
                    });

                    $myJplayer.bind($.jPlayer.event.playing, function(event) {
                        playing = true;
                    });

                    $myJplayer.bind($.jPlayer.event.pause, function(event) {
                        playing = false;
                    });

                    //Bind next/prev click events
                    $(cssSelector.playerPrevious).click(function() {
                        playlistPrev();
                        $(this).blur();
                        return false;
                    });

                    $(cssSelector.playerNext).click(function() {
                        playlistNext();
                        $(this).blur();
                        return false;
                    });

                    $self.bind('mbInitPlaylistAdvance', function(e, changeTo) {
                        if (changeTo != current) {
                            current = changeTo;
                            playlistAdvance(current);
                        }
                        else {
                            if (!$myJplayer.data('jPlayer').status.srcSet) {
                                playlistAdvance(0);
                            }
                            else {
                                togglePlay();
                            }
                        }
                    });

                    $self.bind('mbInitPlayMedia', function(e, mediaObject){
                        playlistPlayMedia(mediaObject);
                    });

                    //If the user doesn't want to wait for widget loads, start playlist now
                    $self.trigger('mbPlaylistLoaded');

                    playlistInit(options.autoplay);
                });

                //Initialize jPlayer
                $myJplayer.jPlayer(jPlayerOptions);
            }

            function playlistInit(autoplay) {
                current = 0;

                if (autoplay) {
                    playlistAdvance(current);
                }
                else {
                    playlistConfig(current);
                    $self.trigger('mbPlaylistInit');
                }
            }

            function playlistConfig(index) {
                current = index;
                $myJplayer.jPlayer("setMedia", myPlaylist[current]);
            }


            function playlistAdvance(index) {
                playlistConfig(index);

                $self.trigger('mbPlaylistAdvance');
                $myJplayer.jPlayer("play");
            }

            //This function will play media that isn't in the playlist
            function playlistPlayMedia(mediaObject) {
                $myJplayer.jPlayer("setMedia", mediaObject);

                $self.trigger('mbPlaylistAdvance');
                $myJplayer.jPlayer("play");
            }

            function playlistNext() {
                var index = (current + 1 < myPlaylist.length) ? current + 1 : 0;
                playlistAdvance(index);
            }

            function playlistPrev() {
                var index = (current - 1 >= 0) ? current - 1 : myPlaylist.length - 1;
                playlistAdvance(index);
            }

            function togglePlay() {
                if (!playing)
                    $myJplayer.jPlayer("play");
                else $myJplayer.jPlayer("pause");
            }

            return{
                init:init,
                playlistInit:playlistInit,
                playlistAdvance:playlistAdvance,
                playlistNext:playlistNext,
                playlistPrev:playlistPrev,
                togglePlay:togglePlay,
                $myJplayer:$myJplayer
            };

        };

        interfaceMgr = function() {

            var $player, $playlist, playlistHideTimeout;


            function init() {
                $player = $(cssSelector.player),
                        $playlist = $(cssSelector.playlist);

                buildPlaylist();
                bindButtonActions();
            }

            function buildInterface() {
                var  playerMarkup, $interface, progressWidth, intPlayerWidth,  buttonAndSeparatorWidth,
                        volumeAndSeparatorWidth, progressPadding, last;

                //I would normally use the templating plugin for something like this, but I wanted to keep this plugin's footprint as small as possible
                playerMarkup = '<div class="ttw-video-player">' +
                    '<div class="jPlayer-container"></div>' +
                    '<div class="player jp-interface">' +

                        '<div class="player-controls">' +

                            '<div class="play jp-play button"></div>' +
                            '<div class="pause jp-pause button"></div>' +
                            '<div class="separator"></div>' +


                            '<div class="playlist-button button"></div>' +
                            '<div class="separator"></div>' +

                            '<div class="hd-button button"></div>' +
                            '<div class="separator"></div>' +


                            '<div class="progress-wrapper">' +
                                '<div class="progress-bg">' +
                                    '<div class="progress jp-seek-bar">' +
                                        '<div class="elapsed jp-play-bar"></div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="separator"></div>' +

                            '<div class="volume-wrapper">' +
                                '<div class="volume jp-volume-bar">' +
                                    '<div class="volume-value jp-volume-bar-value"></div>' +
                                '</div>' +

                            '</div>' +
                            '<div class="separator"></div>' +

                            '<div class="heart-button button"></div>' +
                            '<div class="heart-count"></div>' +
                            '<div class="separator"></div>' +

                            '<div class="settings-button button"></div>' +
                            '<div class="separator"></div>' +

                            '<div class="fullscreen-button  button"></div>' +


                        '</div>' +
                        '<!-- These controls aren\'t used by this plugin, but jPlayer seems to require that they exist -->' +
                            '<span class="unused-controls">' +
                                    '<span class="previous jp-previous"></span>' +
                                    '<span class="next jp-next"></span>' +
                                    '<span class="jp-video-play"></span>' +
                                    '<span class="jp-stop"></span>' +
                                    '<span class="jp-mute"></span>' +
                                    '<span class="jp-unmute"></span>' +
                                    '<span class="jp-volume-max"></span>' +
                                    '<span class="jp-current-time"></span>' +
                                    '<span class="jp-duration"></span>' +
                                    '<span class="jp-repeat"></span>' +
                                    '<span class="jp-repeat-off"></span>' +
                                    '<span class="jp-gui"></span>' +
                                    '<span class="jp-restore-screen"></span>' +
                                    '<span class="jp-full-screen"></span>' +
                                '</span>' +
                    '</div>' +
                    '<div class="playlist">' +
                        '<div class="viewport">' +
                            '<ol class="scroll-content playlist-items">' +
                            '</ol>' +
                        '</div>' +
                        '<div class="scrollbar">' +
                            '<div class="track">' +
                                '<div class="thumb">' +
                                    '<div class="end"></div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<div class="clear"></div>' +
                   '</div>' +
                '</div>';


                
                //Build the html
                $interface = $(playerMarkup).css({display:'none', opacity:0}).appendTo($self).slideDown('slow', function() {
                    
                    //set the size of the player
                    $interface.width(options.width).find(cssSelector.jPlayerInterface + ', ' + cssSelector.jPlayerContainer).width(options.width);
                    $interface.height(pxToInt(options.height)).find(cssSelector.jPlayerContainer).height(pxToInt(options.height) - 34);

                    $interface.animate({opacity:1}, 200, function() {

                        $self.trigger('mbInterfaceBuilt');

                        //Manipulation of the player controls needs to happen after the interface is faded in otherwise the heart button position calculation will be wrong
                        //hide the buttons that aren't being used
                        for (var i = 0; i < validButtons.length; i++) {
                            if ($.inArray(validButtons[i], options.buttons) == -1)
                                $interface.find(cssSelector[validButtons[i] + 'Button']).css('display', 'none').next('.separator').css('display', 'none');
                        }

                        //figure out which button is the last button
                        if ($.inArray('fullscreen', options.buttons) != -1)
                            last = 'fullscreen';
                        else if ($.inArray('settings', options.buttons) != -1)
                            last = 'settings';
                        else if ($.inArray('heart', options.buttons) != -1)
                            last = 'heart';
                        else last = 'volume';

                        //hide the separator for the last button
                        if (last != 'volume')
                            $interface.find(cssSelector[last + 'Button']).next('.separator').css('display', 'none');
                        else $interface.find(cssSelector.volume).next('.separator').css('display', 'none')

                        //resize the progress wrapper based on the number of buttons being shown
                        intPlayerWidth = options.width.substr(0, options.width.length - 2);
                        buttonAndSeparatorWidth = ((options.buttons.length + 1) * 34);
                        volumeAndSeparatorWidth = $interface.find(cssSelector.volume).outerWidth() + 2;
                        progressPadding = 20;
                        progressWidth = intPlayerWidth - buttonAndSeparatorWidth - volumeAndSeparatorWidth - progressPadding;

                        $interface.find(cssSelector.progress).width(progressWidth);

                        //reposition the heart icon based on the position of the heart button
                        if ($.inArray('heart', options.buttons) != -1)
                            $interface.find(cssSelector.heartCount).css({left: $interface.find(cssSelector.heartButton).position()['left'] - 10});

                    });
                });
            }


            function togglePlaylist(playlistButton){
                  if($playlist.hasClass('showing')){
                        playlistButton.removeClass('pressed');
                        $playlist.stop().removeClass('showing').animate({opacity:0}, 200, function(){
                            $(this).css('display', 'none');
                        });
                    }
                    else {
                        playlistButton.addClass('pressed');
                        $playlist.stop().css({opactiy:0, display:'block'}).addClass('showing').animate({opacity:1}, 200);

                      if(options.autoHidePlaylist)
                          setPlaylistHideTimeout(playlistButton);
                    }
            }


            function bindButtonActions(){
                var $controls = $self.find(cssSelector.playerControls);

                //Playlist Button
                $controls.find(cssSelector.playlistButton).bind('click', function(){
                    clearTimeout(playlistHideTimeout);
                    togglePlaylist($(this));
                    runCallback(options.playlistButtonCallback);
                });

                //HD Button
                $controls.find(cssSelector.hdButton).bind('click', function(){
                    if(options.hdPlaylist && options.hdPlaylist[current]){
                        $self.trigger('mbInitPlayMedia', [options.hdPlaylist[current]]);
                    }
                    runCallback(options.hdButtonCallback);
                });

                //Heart Button
                $controls.find(cssSelector.heartButton).bind('click', function(e){
                    if(runCallback(options.allowHeartIncrement, e) === true){
                        self.heartCount++;
                        updateHeartCount();
                        runCallback(options.heartButtonCallback, self.heartCount);
                    }
                });

                //Settings Button
                $controls.find(cssSelector.settingsButton).bind('click', function(e){
                    runCallback(options.settingsButtonCallback);
                });

                //FullScreen Button
                $controls.find(cssSelector.fullscreenButton).bind('click', function(e){
                    runCallback(options.fullscreenCallback);
                });

            }



            function buildPlaylist() {
                var markup, $playlist, $playlistWrapper;

                markup = {
                    listItem:'<li class="playlist-item">' +
                            '</li>'
                };

                $playlistWrapper = $self.find(cssSelector.playlistItems);

                for (var j = 0; j < myPlaylist.length; j++) {
                    var $playlistItem = $(markup.listItem);

                    $playlistItem.data('index', j);

                    if (!isUndefined(myPlaylist[j].poster)) {
                        $('<img src="' + myPlaylist[j].poster + '" alt="video poster" />')
                                .css({'opacity': 0}).appendTo($playlistItem)
                                .imagesLoaded(function() {
                                    $(this).animate({opacity:1})
                                });
                    }
                    else $playlistItem.html(trackName(j));

                    $playlistWrapper.append($playlistItem);
                }

                $self.find(cssSelector.playlistItem).click(function() {
                    $self.trigger('mbInitPlaylistAdvance', [$(this).data('index')]);
                });

                //set the height of the playlist based on options
                $playlistWrapper.parents(cssSelector.playlist).height(pxToInt(options.height) - 34)
                        .find(cssSelector.scrollViewport).height(pxToInt(options.height) - 34);

                //The playlist is initialized with opacity 0 and display block. This is because tinyscrollbar will not
                //initialze if display is set to none. Set display = none once tinyscrollbar has initialized.
                $playlist = $playlistWrapper.parents(cssSelector.playlist).tinyscrollbar({sizethumb:114}).css('display', 'none');

                //auto hide the playlist if the auto hide option is set
                if (options.autoHidePlaylist) {
                    $playlist.mouseleave(function() {
                        setPlaylistHideTimeout($self.find(cssSelector.playlistButton));
                    });

                    $playlist.mouseenter(function() {
                        clearTimeout(playlistHideTimeout)
                    });
                }

            }

            function setPlaylistHideTimeout(playlistButton){
                playlistHideTimeout = setTimeout(function(){
                    togglePlaylist(playlistButton);
                }, options.autoHidePlaylistDelay);
            }

            function duration(index) {
                return !isUndefined(myPlaylist[index].duration) ? myPlaylist[index].duration : '-';
            }

            function updateHeartCount(){
                if(self.heartCount > 0){
                    var $heartCount = $self.find(cssSelector.heartCount);

                    if(self.heartCount == 1)
                        $heartCount.css({opacity:0, display:'block'}).addClass('showing').animate({opacity:1});

                    $heartCount.html(self.heartCount);
                }
            }

            return{
                buildInterface:buildInterface,
                buildPlaylist:buildPlaylist,
                updateHeartCount:updateHeartCount,
                init:init
            }

        };

        /** Common Functions **/
        function pxToInt(value){
            return parseInt(value.substr(0, value.length -2));
        }

        function debugMessage (msg){
            if(options.debug && window.console) {
                console.log('MEDIA PLAYER: ' + msg);
            }
        }

        function trackName(index) {         
            if (!isUndefined(myPlaylist[index].title))
                return myPlaylist[index].title;
            else {
                var name = '', supplied  = jPlayerOptions.supplied.split(',');
                for(var i = 0; i < supplied.length; i++) {
                    supplied[i] = $.trim(supplied[i]);
                    if (!isUndefined(myPlaylist[index][supplied[i]])) {
                        name = fileName(myPlaylist[index][supplied[i]]);
                        break;
                    }
                }
                return name;
            }
        }

        function fileName(path) {
            path = path.split('/');
            return path[path.length - 1];
        }


        /** Utility Functions **/
        function attr(selector) {
            return selector.substr(1);
        }

        function runCallback(callback) {
            var functionArgs = Array.prototype.slice.call(arguments, 1);

            if ($.isFunction(callback)) {
                return callback.apply(this, functionArgs);
            }
            else return false;
        }

        function isUndefined(value) {
            return typeof value == 'undefined';
        }

        appMgr();

    };
})(jQuery);

/*!
 * Tiny Scrollbar 1.65
 * http://www.baijs.nl/tinyscrollbar/
 *
 * Copyright 2010, Maarten Baijs
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.opensource.org/licenses/gpl-2.0.php
 *
 * Date: 10 / 05 / 2011
 * Depends on library: jQuery
 *
 */

(function($){
	$.tiny = $.tiny || { };

	$.tiny.scrollbar = {
		options: {
			axis: 'y', // vertical or horizontal scrollbar? ( x || y ).
			wheel: 40,  //how many pixels must the mouswheel scroll at a time.
			scroll: true, //enable or disable the mousewheel;
			size: 'auto', //set the size of the scrollbar to auto or a fixed number.
			sizethumb: 'auto' //set the size of the thumb to auto or a fixed number.
		}
	};

	$.fn.tinyscrollbar = function(options) {
		var options = $.extend({}, $.tiny.scrollbar.options, options);
		this.each(function(){ $(this).data('tsb', new Scrollbar($(this), options)); });
		return this;
	};
	$.fn.tinyscrollbar_update = function(sScroll) { return $(this).data('tsb').update(sScroll); };

	function Scrollbar(root, options){
		var oSelf = this;
		var oWrapper = root;
		var oViewport = { obj: $('.viewport', root) };
		var oContent = { obj: $('.scroll-content', root) };
		var oScrollbar = { obj: $('.scrollbar', root) };
		var oTrack = { obj: $('.track', oScrollbar.obj) };
		var oThumb = { obj: $('.thumb', oScrollbar.obj) };
		var sAxis = options.axis == 'x', sDirection = sAxis ? 'left' : 'top', sSize = sAxis ? 'Width' : 'Height';
		var iScroll, iPosition = { start: 0, now: 0 }, iMouse = {};

		function initialize() {
			oSelf.update();
			setEvents();
			return oSelf;
		}
		this.update = function(sScroll){
			oViewport[options.axis] = oViewport.obj[0]['offset'+ sSize];
			oContent[options.axis] = oContent.obj[0]['scroll'+ sSize];
			oContent.ratio = oViewport[options.axis] / oContent[options.axis];
			oScrollbar.obj.toggleClass('disable', oContent.ratio >= 1);
			oTrack[options.axis] = options.size == 'auto' ? oViewport[options.axis] : options.size;
			oThumb[options.axis] = Math.min(oTrack[options.axis], Math.max(0, ( options.sizethumb == 'auto' ? (oTrack[options.axis] * oContent.ratio) : options.sizethumb )));
			oScrollbar.ratio = options.sizethumb == 'auto' ? (oContent[options.axis] / oTrack[options.axis]) : (oContent[options.axis] - oViewport[options.axis]) / (oTrack[options.axis] - oThumb[options.axis]);
			iScroll = (sScroll == 'relative' && oContent.ratio <= 1) ? Math.min((oContent[options.axis] - oViewport[options.axis]), Math.max(0, iScroll)) : 0;
			iScroll = (sScroll == 'bottom' && oContent.ratio <= 1) ? (oContent[options.axis] - oViewport[options.axis]) : isNaN(parseInt(sScroll)) ? iScroll : parseInt(sScroll);
			setSize();
		};
		function setSize(){
			oThumb.obj.css(sDirection, iScroll / oScrollbar.ratio);
			oContent.obj.css(sDirection, -iScroll);
			iMouse['start'] = oThumb.obj.offset()[sDirection];
			var sCssSize = sSize.toLowerCase();
			oScrollbar.obj.css(sCssSize, oTrack[options.axis]);
			oTrack.obj.css(sCssSize, oTrack[options.axis]);
			oThumb.obj.css(sCssSize, oThumb[options.axis]);
		};
		function setEvents(){
			oThumb.obj.bind('mousedown', start);
			oThumb.obj[0].ontouchstart = function(oEvent){
				oEvent.preventDefault();
				oThumb.obj.unbind('mousedown');
				start(oEvent.touches[0]);
				return false;
			};
			oTrack.obj.bind('mouseup', drag);
			if(options.scroll && this.addEventListener){
				oWrapper[0].addEventListener('DOMMouseScroll', wheel, false);
				oWrapper[0].addEventListener('mousewheel', wheel, false );
			}
			else if(options.scroll){oWrapper[0].onmousewheel = wheel;}
		};
		function start(oEvent){
			iMouse.start = sAxis ? oEvent.pageX : oEvent.pageY;
			var oThumbDir = parseInt(oThumb.obj.css(sDirection));
			iPosition.start = oThumbDir == 'auto' ? 0 : oThumbDir;
			$(document).bind('mousemove', drag);
			document.ontouchmove = function(oEvent){
				$(document).unbind('mousemove');
				drag(oEvent.touches[0]);
			};
			$(document).bind('mouseup', end);
			oThumb.obj.bind('mouseup', end);
			oThumb.obj[0].ontouchend = document.ontouchend = function(oEvent){
				$(document).unbind('mouseup');
				oThumb.obj.unbind('mouseup');
				end(oEvent.touches[0]);
			};
			return false;
		};
		function wheel(oEvent){
			if(!(oContent.ratio >= 1)){
				oEvent = $.event.fix(oEvent || window.event);
				var iDelta = oEvent.wheelDelta ? oEvent.wheelDelta/120 : -oEvent.detail/3;
				iScroll -= iDelta * options.wheel;
				iScroll = Math.min((oContent[options.axis] - oViewport[options.axis]), Math.max(0, iScroll));
				oThumb.obj.css(sDirection, iScroll / oScrollbar.ratio);
				oContent.obj.css(sDirection, -iScroll);
				oEvent.preventDefault();
			};
		};
		function end(oEvent){
			$(document).unbind('mousemove', drag);
			$(document).unbind('mouseup', end);
			oThumb.obj.unbind('mouseup', end);
			document.ontouchmove = oThumb.obj[0].ontouchend = document.ontouchend = null;
			return false;
		};
		function drag(oEvent){
			if(!(oContent.ratio >= 1)){
				iPosition.now = Math.min((oTrack[options.axis] - oThumb[options.axis]), Math.max(0, (iPosition.start + ((sAxis ? oEvent.pageX : oEvent.pageY) - iMouse.start))));
				iScroll = iPosition.now * oScrollbar.ratio;
				oContent.obj.css(sDirection, -iScroll);
				oThumb.obj.css(sDirection, iPosition.now);
			}
			return false;
		};

		return initialize();
	};
})(jQuery);

(function($) {
// $('img.photo',this).imagesLoaded(myFunction)
// execute a callback when all images have loaded.
// needed because .load() doesn't work on cached images

// mit license. paul irish. 2010.
// webkit fix from Oren Solomianik. thx!

// callback function is passed the last image to load
//   as an argument, and the collection as `this`


    $.fn.imagesLoaded = function(callback) {
        var elems = this.filter('img'),
                len = elems.length;

        elems.bind('load',
                function() {
                    if (--len <= 0) {
                        callback.call(elems, this);
                    }
                }).each(function() {
            // cached images don't fire load sometimes, so we reset src.
            if (this.complete || this.complete === undefined) {
                var src = this.src;
                // webkit hack from http://groups.google.com/group/jquery-dev/browse_thread/thread/eee6ab7b2da50e1f
                // data uri bypasses webkit log warning (thx doug jones)
                this.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
                this.src = src;
            }
        });

        return this;
    };
})(jQuery);