import time
from pygame import mixer

playAudio = True
audio = 'Pyb_Female/1welcome_msg_f.mp3'
audio1 = 'Pyb_Female/3select.mp3'
def thankYouVoice():
    print("hie")
    
    mixer.init()

    sound = mixer.Sound("Pyb_Female/5thankyoumsg.mp3")
    sound.play()

    time.sleep(5)

    # mixer.init()
    # mixer.music.load('Pyb_Female/5thankyoumsg.mp3')
    # mixer.music.play()
    # mixer.music.queue('Pyb_Female/5thankyoumsg.mp3')
    
thankYouVoice()