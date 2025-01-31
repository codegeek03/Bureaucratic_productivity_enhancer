from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import speech_recognition as sr
import time
from datetime import datetime
import os
import logging
import threading
from grammar_correction import ProfessionalResponseGenerator        
# [Previous imports and configuration remain the same...]

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speech Recognition App</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }

        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #2c3e50;
            text-align: center;
        }

        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }

        #startButton {
            background-color: #2ecc71;
            color: white;
        }

        #stopButton {
            background-color: #e74c3c;
            color: white;
        }

        #adjustNoiseButton {
            background-color: #3498db;
            color: white;
        }

        button:disabled {
            background-color: #95a5a6;
            cursor: not-allowed;
        }

        #status {
            text-align: center;
            margin: 10px 0;
            padding: 10px;
            border-radius: 4px;
        }

        #transcriptionArea {
            width: 100%;
            min-height: 200px;
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            resize: vertical;
        }

        .success {
            background-color: #d5f5e3;
            color: #27ae60;
        }

        .error {
            background-color: #fadbd8;
            color: #c0392b;
        }

        .warning {
            background-color: #fef9e7;
            color: #f1c40f;
        }

        #downloadSection {
            margin-top: 20px;
            text-align: center;
        }

        #downloadLink {
            color: #3498db;
            text-decoration: none;
        }

        #downloadLink:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Speech Recognition App</h1>
        
        <div class="controls">
            <button id="adjustNoiseButton">Adjust for Noise</button>
            <button id="startButton">Start Recording</button>
            <button id="stopButton" disabled>Stop Recording</button>
        </div>

        <div id="status"></div>
        
        <textarea id="transcriptionArea" readonly placeholder="Transcription will appear here..."></textarea>
        
        <div id="downloadSection">
            <a id="downloadLink" style="display: none">Download Transcription</a>
        </div>
    </div>

    <script>
        const startButton = document.getElementById('startButton');
        const stopButton = document.getElementById('stopButton');
        const adjustNoiseButton = document.getElementById('adjustNoiseButton');
        const status = document.getElementById('status');
        const transcriptionArea = document.getElementById('transcriptionArea');
        const downloadLink = document.getElementById('downloadLink');

        let isRecording = false;

        function updateStatus(message, type = 'info') {
            status.textContent = message;
            status.className = type;
        }

        function toggleButtons(recording) {
            startButton.disabled = recording;
            stopButton.disabled = !recording;
            adjustNoiseButton.disabled = recording;
        }

        adjustNoiseButton.addEventListener('click', async () => {
            try {
                updateStatus('Adjusting for ambient noise...', 'warning');
                adjustNoiseButton.disabled = true;
                
                const response = await fetch('/adjust-noise', {
                    method: 'POST'
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    updateStatus('Noise adjustment complete', 'success');
                } else {
                    updateStatus(`Error: ${data.detail}`, 'error');
                }
            } catch (error) {
                updateStatus(`Error: ${error.message}`, 'error');
            } finally {
                adjustNoiseButton.disabled = false;
            }
        });

        startButton.addEventListener('click', async () => {
            isRecording = true;
            toggleButtons(true);
            updateStatus('Recording...', 'warning');
            
            try {
                const response = await fetch('/listen', {
                    method: 'POST'
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    transcriptionArea.value = data.text;
                    updateStatus('Recording complete', 'success');
                    
                    // Update download link
                    downloadLink.href = `/download/${data.filename}`;
                    downloadLink.download = data.filename;
                    downloadLink.textContent = `Download ${data.filename}`;
                    downloadLink.style.display = 'inline';
                } else {
                    updateStatus(`Error: ${data.detail}`, 'error');
                }
            } catch (error) {
                updateStatus(`Error: ${error.message}`, 'error');
            } finally {
                isRecording = false;
                toggleButtons(false);
            }
        });

        stopButton.addEventListener('click', async () => {
            try {
                const response = await fetch('/stop-listening', {
                    method: 'POST'
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    updateStatus('Recording stopped', 'success');
                } else {
                    updateStatus(`Error: ${data.detail}`, 'error');
                }
            } catch (error) {
                updateStatus(`Error: ${error.message}`, 'error');
            } finally {
                isRecording = false;
                toggleButtons(false);
            }
        });

        // Check server health on page load
        async function checkHealth() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                
                if (data.speech_recognition_available) {
                    updateStatus('Ready to record', 'success');
                } else {
                    updateStatus('Speech recognition not available', 'error');
                    startButton.disabled = true;
                    stopButton.disabled = true;
                    adjustNoiseButton.disabled = true;
                }
            } catch (error) {
                updateStatus('Cannot connect to server', 'error');
                startButton.disabled = true;
                stopButton.disabled = true;
                adjustNoiseButton.disabled = true;
            }
        }

        checkHealth();
    </script>
</body>
</html>
"""


# [Rest of the FastAPI code remains the same...]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modify the root endpoint to return the HTML template
@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=HTML_TEMPLATE)


# Create a directory for storing audio files if it doesn't exist
UPLOAD_DIR = "audio_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class SpeechRecognizer:
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.is_listening = False
            self.recording_thread = None
            logger.info("Successfully initialized SpeechRecognizer")
        except Exception as e:
            logger.error(f"Error initializing SpeechRecognizer: {str(e)}")
            raise Exception(f"Failed to initialize speech recognition: {str(e)}")
        
    def adjust_for_noise(self):
        try:
            logger.info("Starting noise adjustment")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logger.info("Noise adjustment completed successfully")
            return {"message": "Noise adjustment complete", "status": "success"}
        except Exception as e:
            logger.error(f"Error during noise adjustment: {str(e)}")
            return {"message": f"Error during noise adjustment: {str(e)}", "status": "error"}
    
    def stop_listening(self):
        self.is_listening = False
        logger.info("Stopping recording...")
        if hasattr(self, 'recording_thread') and self.recording_thread:
            self.recording_thread.join()
        return {"success": True, "message": "Recording stopped"}

    def listen(self):
        self.is_listening = True
        try:
            logger.info("Starting audio capture")
            with self.microphone as source:
                logger.info("Listening for audio input...")
                # Reduce timeout and phrase_time_limit for better responsiveness
                audio = self.recognizer.listen(source, timeout=600, phrase_time_limit=40)
                logger.info("Audio captured, processing...")
                
                if not self.is_listening:  # Check if we should stop
                    return {"success": False, "error": "Recording stopped by user"}
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    logger.info("Successfully transcribed audio to text")
                    return {"success": True, "text": text}
                except sr.UnknownValueError:
                    logger.error("Could not understand the audio")
                    return {"success": False, "error": "Could not understand the audio"}
                except sr.RequestError as e:
                    logger.error(f"Could not request results from speech recognition service: {str(e)}")
                    return {"success": False, "error": "Speech recognition service error"}
                    
        except Exception as e:
            logger.error(f"Error during speech recognition: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            self.is_listening = False

# Create a global instance of SpeechRecognizer
try:
    speech_engine = SpeechRecognizer()
except Exception as e:
    logger.error(f"Failed to create SpeechRecognizer instance: {str(e)}")
    speech_engine = None

@app.post("/stop-listening")
async def stop_listening():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    return speech_engine.stop_listening()

@app.post("/listen")
async def listen_audio():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    
    result = speech_engine.listen()
    ans=ProfessionalResponseGenerator().generate_response(result["text"])
    if result["success"]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dictation_{timestamp}.txt"
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(ans)
            
            logger.info(f"Successfully saved transcription to {filename}")
            return {
                "success": True,
                "text": ans,
                "filename": filename
            }
        except Exception as e:
            logger.error(f"Error saving transcription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving transcription: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail=result["error"])

# Your other existing endpoints remain the same...

@app.get("/health")
async def health_check():
    """Endpoint to check if the server is running and speech recognition is available"""
    return {
        "status": "healthy",
        "speech_recognition_available": speech_engine is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/adjust-noise")
async def adjust_noise():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    
    result = speech_engine.adjust_for_noise()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.post("/listen")
async def listen_audio():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    
    result = speech_engine.listen()
    if result["success"]:
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dictation_{timestamp}.txt"
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            # Save the text to a file
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(result["text"])
            
            logger.info(f"Successfully saved transcription to {filename}")
            return {
                "success": True,
                "text": result["text"],
                "filename": filename
            }
        except Exception as e:
            logger.error(f"Error saving transcription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving transcription: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.get("/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

# Serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("./templates/index.html", "r", encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"Error serving HTML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving HTML: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)