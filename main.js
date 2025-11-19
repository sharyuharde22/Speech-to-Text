#Storeinstaticfolder
let chunks = [];
let recorder;

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        recorder = new MediaRecorder(stream);

        recorder.start();
        chunks = [];

        recorder.ondataavailable = e => chunks.push(e.data);

        recorder.onstop = () => {
            let blob = new Blob(chunks, { type: "audio/webm" });
            uploadAudio(blob);
        };

        setTimeout(() => recorder.stop(), 4000); // record 4 sec
    });
}

function uploadAudio(blob) {
    let form = new FormData();
    form.append("audio", blob, "recording.webm");

    fetch("/speech_to_text", {
        method: "POST",
        body: form
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText = data.text;
    });
}
