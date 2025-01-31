// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    let recognition;
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const status = document.getElementById('status');
    const recordingStatus = document.getElementById('recordingStatus');
    const interimResults = document.getElementById('interimResults');
    const finalResults = document.getElementById('finalResults');

    // Check if browser supports speech recognition
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        setupRecognition();
    } else {
        status.textContent = 'Speech recognition is not supported in this browser.';
        startButton.disabled = true;
    }

    function setupRecognition() {
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            status.textContent = 'Listening...';
            recordingStatus.textContent = '🎤 Recording';
            startButton.disabled = true;
            stopButton.disabled = false;
        };

        recognition.onend = function() {
            status.textContent = 'Recognition stopped.';
            recordingStatus.textContent = '';
            startButton.disabled = false;
            stopButton.disabled = true;
        };

        recognition.onresult = function(event) {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                    sendToServer(transcript);
                } else {
                    interimTranscript += transcript;
                }
            }

            interimResults.textContent = interimTranscript;
            if (finalTranscript !== '') {
                finalResults.textContent = finalTranscript;
            }
        };

        recognition.onerror = function(event) {
            status.textContent = 'Error occurred in recognition: ' + event.error;
        };
    }

    async function sendToServer(query) {
        try {
            const response = await fetch('/inference', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    user_id: 'codegeek03'
                })
            });

            const data = await response.json();
            if (data.status === 'success') {
                finalResults.innerHTML += `<div class="result-item">
                    <span class="timestamp">${data.timestamp}</span>
                    <span class="content">${data.data}</span>
                </div>`;
            }
        } catch (error) {
            console.error('Error:', error);
            status.textContent = 'Error sending to server: ' + error.message;
        }
    }

    startButton.addEventListener('click', function() {
        recognition.start();
    });

    stopButton.addEventListener('click', function() {
        recognition.stop();
    });
});