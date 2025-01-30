from speech_Recog import SpeechToText
from grammar_correction import ProfessionalResponseGenerator

def grammar_correction_enhancement(filename):
    speech_recognizer = SpeechToText()
    transcribed_text = speech_recognizer.transcribe(filename)
    generator = ProfessionalResponseGenerator()
    
    response = generator.generate_response(transcribed_text)
    
    return response

if __name__ == "__main__":
    filename = "harvard.wav"
    output = grammar_correction_enhancement(filename)
    print(output)    