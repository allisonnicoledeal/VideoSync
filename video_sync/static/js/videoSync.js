let player1, player2, data1, data2;
let playButton, pauseButton;

function init() {
    // Load it from here so the DOM is already loaded.
    const tag = document.createElement('script');

    tag.src = "https://www.youtube.com/iframe_api";
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    data1 = document.getElementById("data-1");
    data2 = document.getElementById("data-2");
    playButton = document.getElementById("playAll");
    pauseButton = document.getElementById("pauseAll");

    playButton.onclick = onPlayClick;
    pauseButton.onclick = onPauseClick;
}

function onYouTubeIframeAPIReady() { // create function that creates similar elements
    player1 = new YT.Player('iframe-1', {
        height: '400',
        width: '470',
        videoId: data1.getAttribute('data-source').split("embed/")[1],
        playerVars: {autoplay: 0, controls: 0, modestbranding: 1, showinfo: 0},
        events: {
            onReady: onPlayerReady,
        }
    });

    player2 = new YT.Player('iframe-2', {
        height: '400',
        width: '470',
        videoId: data2.getAttribute('data-source').split("embed/")[1],
        playerVars: {autoplay: 0, controls: 0, modestbranding: 1, showinfo: 0},
        events: {
            onReady: onPlayerReady,
        }
    });
}

function onPlayerReady(event) {
    event.target.setPlaybackQuality("small");
    playButton.removeAttribute('disabled');
    pauseButton.removeAttribute('disabled');
}

function onPlayClick() {
    let vFirst, vSecond;

    if (Number(data1.getAttribute("data-sync")) < (Number(data2.getAttribute("data-sync")))) {
        vFirst = player1; // player element
        vFirstData = data1; // dom element
        vSecond = player2;
        vSecondData = data2;
        console.log("one is first");
        console.log("two data status");
        console.log(vSecondData.getAttribute('data-status'));
    } else {
        vFirst = player2;
        vFirstData = data2;
        vSecond = player1;
        vSecondData = data1;
        console.log("two is first");
        console.log("two data status");
        console.log(vSecondData.getAttribute('data-status'));
    }

    // Event listener
    window.setInterval(() => {
        console.log("vFirst current time");
        console.log(vFirst.getCurrentTime());
        console.log("vSecond data-sync");
        console.log(vSecondData.getAttribute('data-sync'));
        console.log("vSecond data-status");
        console.log(vSecondData.getAttribute('data-status'));


        if (vFirst.getCurrentTime() >= vSecondData.getAttribute('data-sync') && vSecondData.getAttribute('data-status') === 'notPlaying') {
            vSecond.mute();
            vSecond.playVideo();
            console.log('VIDEO PLAYING');
            console.log(vFirst.getCurrentTime());
            vSecondData.getAttribute('data-status', "playing");
        }

        if (vFirst.getPlayerState() === 0 && vSecond.getPlayerState() === 1) { // first is done playing
            //unmute second
            vSecond.unMute();
        }
    }, 200);

    vFirst.playVideo();
    vFirstData.getAttribute('data-status', 'playing');

    if (data2.getAttribute('data-status') === 'playing' && data1.getAttribute('data-status') === 'playing') {
        vSecond.playVideo();
        vFirst.playVideo();
    }
}

function onPauseClick() {
    player1.pauseVideo();
    player2.pauseVideo();
}

document.addEventListener("DOMContentLoaded", init);
