import speech_recognition as sr
import time

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def adjust_for_noise(self):
        """Adjust microphone for ambient noise"""
        print("Adjusting for ambient noise... Please be quiet.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Noise adjustment complete!")
    
    def listen(self):
        """Listen to audio input and convert to text"""
        try:
            with self.microphone as source:
                print("\nListening... Speak now!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    return text
                except sr.UnknownValueError:
                    return "Could not understand the audio"
                except sr.RequestError:
                    return "Could not request results from speech recognition service"
                    
        except Exception as e:
            return f"Error occurred: {str(e)}"

def main():
    # Create instance of speech recognizer
    speech_engine = SpeechRecognizer()
    
    # Initial noise adjustment
    speech_engine.adjust_for_noise()
    
    while True:
        try:
            # Get speech input
            result = speech_engine.listen()
            
            # Print timestamp and result
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print(f"\nTime: {current_time}")
            print(f"Recognized Text: {result}")
            
            # Ask to continue
            choice = input("\nContinue listening? (y/n): ").lower()
            if choice != 'y':
                break
                
        except KeyboardInterrupt:
            print("\nStopping the program...")
            break

if __name__ == "__main__":
    # First, install required package:
    # pip install SpeechRecognition
    # pip install pyaudio
    main()