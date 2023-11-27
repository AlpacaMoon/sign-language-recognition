# from gtts import gTTS
# from playsound import playsound
# import os
# from threading import Thread


# def playAudio(tts):
#     filename = "temptts.mp3"

#     abs_filepath = os.path.join(os.path.dirname(__file__), filename)
#     tts.save(abs_filepath)
#     playsound(abs_filepath)
#     os.remove(abs_filepath)


# # tts = gTTS('something', lang='bho')


# # playAudioThread = Thread(target=playAudio, args=(tts,))
# # playAudioThread.start()

# import gtts

# print(gtts.lang.tts_langs())

from main import Pyttsx3TextToSpeechModule

tts = Pyttsx3TextToSpeechModule()
tts.changeVoice(
    1
)

from threading import Thread

def f():
    tts.say('hello')
# Thread(target=f).start()
f()