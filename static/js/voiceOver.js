var SpeechRecognition = window.webkitSpeechRecognition;
var recognition = new SpeechRecognition();
var latestRef = ''
var voiceOver = false


$(".start-voiceOver").click(function (e) {
    e.preventDefault();
    voiceOver = true
    $(".backdrop").fadeOut()
});
$(".close-modaal").click(function (e) {
    e.preventDefault();
    $(".backdrop").fadeOut()
});

$("input,select").focusin(function (e) {
    e.preventDefault();
    latestRef = $(this)
    speak($(this).attr("voice-data"))
    console.log("focused")
});


$("input").focusout(function (e) {
    e.preventDefault();
    console.log("unfocused")
});


recognition.continuous = true;

recognition.onresult = function (event) {

    var current = event.resultIndex;
    var transcript = event.results[current][0].transcript;

    // Content += transcript;
    latestRef.val(latestRef.val() + transcript)
    // latestRef.val(transcript);

};

recognition.onstart = function () {
    console.log('Voice recognition is ON.');
}

recognition.onspeechend = function () {
    console.log('No activity.');
    console.log("speech ended")
}

recognition.onerror = function (event) {
    if (event.error == 'no-speech') {
        console.log('Try again.');
    }
}








// speech engine
async function speak(text) {
    if ('speechSynthesis' in window) {
        console.log("supported")
        var msg = new SpeechSynthesisUtterance();
        var voices = window.speechSynthesis.getVoices();
        var index = 10
        for (let i = 0; i < voices.length; i++) {
            if (voices[i].lang == "hi-IN") {
                console.log(voices[i])
                index = i
            }
            else {
                console.log(i)
            }
        }
        msg.voice = voices[index];
        msg.volume = 1;
        msg.rate = 0.8;
        msg.pitch = 0.9;
        msg.text = text
        msg.lang = 'hi';
        if (voiceOver) {
            speechSynthesis.speak(msg);
        }
        msg.onend = () => {
            recognition.start();
            console.log("speak now")
        }
    } else {
        alert("Sorry, your browser doesn't support text to speech!");
    }
}