import pyaudio as pa, gtts
import wave, speech_recognition as sr
from translate import Translator

class audioManager:
    def __init__(self):
        self.FORMAT = pa.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "orignal.wav"

        self.audio = pa.PyAudio()

    def get_stream(self):
        # start Recording
        stream = self.audio.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                input=True,
                                frames_per_buffer=self.CHUNK)
        print ("recording...")
        frames = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        else:
            print ("finished recording")
            # stop Recording
            stream.stop_stream()
            stream.close()
            self.audio.terminate()

        return frames

    def get_wave_file(self, frames):
        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def waveToText(self, wave):
        r = sr.Recognizer()
        waveFile = sr.AudioFile(wave)
        with waveFile as source:
            audio = r.record(source)

        value = r.recognize_google(audio)
        return value

    def convertLangSave(self, lang, text):
        try:
            translator = Translator(from_lang="en-in",to_lang='french')
            translated_text = translator.translate(text)
            gtts.gTTS(text=translated_text, lang='hi', slow=False).save('translated.mp3') # saving the hindi file
            error = False

        except:
            error = True
            translated_text = 'An Error Occured ):'


        return translated_text, error

    def all_in_one(self):
        self.frames = self.get_stream()
        wav_conversion = self.get_wave_file(self.frames)
        text = self.waveToText(self.WAVE_OUTPUT_FILENAME)
        translated = self.convertLangSave('hi', text)

        return translated
