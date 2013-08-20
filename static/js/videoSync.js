        // Youtube iframe API
        var tag = document.createElement('script');

        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        var player1, player2, data1, data2;
        var playButton, pauseButton;

        function init() {
            data1 = $("#data-1");
            data2 = $("#data-2");
            playButton = $("#playAll");
            pauseButton = $("#pauseAll");

            playButton.on("click", onPlayClick);
            pauseButton.on("click", onPauseClick);
        }

        // Create YouTube Iframe elements
        function onYouTubeIframeAPIReady() { // create function that creates similar elements
            player1 = new YT.Player('iframe-1', {
                height: '400',
                width: '470',
                videoId: data1.attr('data-source').split("embed/")[1],
                playerVars: {'autoplay': 0, 'controls': 0, 'modestbranding': 1, 'showinfo': 0},
                events: {
                'onReady': onPlayerReady,
                // 'onStateChange': onPlayerStateChange
                }
            });

            player2 = new YT.Player('iframe-2', {
                height: '400',
                width: '470',
                videoId: data2.attr('data-source').split("embed/")[1],
                playerVars: {'autoplay': 0, 'controls': 0, 'modestbranding': 1, 'showinfo': 0},
                events: {
                'onReady': onPlayerReady,
                // 'onStateChange': onPlayerStateChange
                }
            });
        }

        // Enable Play and Pause buttons if player1 and player2 videos have loaded 2%
        function onPlayerReady(event) {
            event.target.setPlaybackQuality("small");
            event.target.playVideo();
            event.target.pauseVideo();
            window.setInterval(function() {
                // console.log(event.target.getVideoLoadedFraction());
                if (event.target.getVideoLoadedFraction() > 0.02) {
                    event.target.readyToPlayNow = "true";
                }

                if ((player1.readyToPlayNow == "true") && (player2.readyToPlayNow == "true")) {
                    playButton.removeAttr('disabled');
                    pauseButton.removeAttr('disabled');
                    // player1.playVideo();
                    // player2.playVideo();
                }
            }, 500);
        }

        function onPlayClick(event) {
            var vFirst, vSecond;

            if (Number(data1.attr("data-sync")) < (Number(data2.attr("data-sync")))) {
                vFirst = player1; // player element
                vFirstData = data1; // dom element
                vSecond = player2;
                vSecondData = data2;
                console.log("one is first");
                console.log("two data status");
                console.log(vSecondData.attr('data-status'));
            } else {
                vFirst = player2;
                vFirstData = data2;
                vSecond = player1;
                vSecondData = data1;
                console.log("two is first");
                console.log("two data status");
                console.log(vSecondData.attr('data-status'));
            }

            // Event listener
            window.setInterval(function() {
                console.log("vFirst current time");
                console.log(vFirst.getCurrentTime());
                console.log("vSecond data-sync");
                console.log(vSecondData.attr('data-sync'));
                console.log("vSecond data-status");
                console.log(vSecondData.attr('data-status'));


                if ((vFirst.getCurrentTime() >= vSecondData.attr('data-sync')) && (vSecondData.attr('data-status') == 'notPlaying')){
                    vSecond.mute();
                    vSecond.playVideo();
                    console.log('VIDEO PLAYING');
                    console.log(vFirst.getCurrentTime());
                    vSecondData.attr('data-status', "playing");
                }

                if ((vFirst.getPlayerState() == 0) && (vSecond.getPlayerState() == 1)) { // first is done playing
                    //unmute second
                    vSecond.unMute();
                }
            }, 200);

            vFirst.playVideo();
            vFirstData.attr('data-status', 'playing');

            if ((data2.attr('data-status') == 'playing') && (data1.attr('data-status') == 'playing')) {
                vSecond.playVideo();
                vFirst.playVideo();
            }
        }
                  
        function onPauseClick(event) {
            player1.pauseVideo();
            player2.pauseVideo();
        }
       
            init();

