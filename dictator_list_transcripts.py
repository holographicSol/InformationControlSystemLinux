import os
import codecs
import time
from gtts import gTTS
import distutils.dir_util
import subprocess

# Files
curDir = os.getcwd()
path = './transcripts'
secondary_key_file = './temporary/secondary-key.tmp'

distutils.dir_util.mkpath(path)

# Data
secondary_key = ''
available_transcription = []
speak_available_transcription = []


def found_sound():
    found_plugin_file_sound = './resources/sound/found_sound.mp3'
    cmd = 'mpg321 ' + found_plugin_file_sound
    fsound = subprocess.Popen(cmd,
                              shell=True,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)


def not_found_sound():
    not_found_plugin_file_sound = './resources/sound/not_found_sound.mp3'
    cmd = 'mpg321 ' + not_found_plugin_file_sound
    nsound = subprocess.Popen(cmd,
                              shell=True,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)


# List All
def list_all():
    print('2. retrieving stored transcripts')
    for dirName, subdirList, fileList in os.walk(path):
        for fname in fileList:
            if fname.endswith('.tmp'):
                fullPath = os.path.join(curDir, dirName, fname)
                available_transcription.append(fullPath)
                if secondary_key in fname:
                    spoken_fname = fname
                    spoken_fname = spoken_fname.replace('.tmp', '')
                    spoken_fname = spoken_fname.replace('_', '')
                    if spoken_fname not in speak_available_transcription:
                        speak_available_transcription.append(spoken_fname)
    if len(speak_available_transcription) > 0:
        found_sound()
        print('available transcripts for '+secondary_key)
        text = 'available transcripts for '+secondary_key
        tts = gTTS(text=text, lang='en')
        tts.save("./transcripts/available_transcripts.mp3")
        time.sleep(1)
        os.system("mpg321 " + "./transcripts/available_transcripts.mp3")

        i = 0
        for speak_available_transcriptions in speak_available_transcription:
            if len(speak_available_transcription[i]) > 1:
                print(speak_available_transcription[i])
                tts = gTTS(text=speak_available_transcription[i], lang='en')
                tts.save("./transcripts/available_transcripts.mp3")
                time.sleep(1)
                os.system("mpg321 " + "./transcripts/available_transcripts.mp3")
            i += 1
    else:
        not_found_sound()


# 0 Begin
with codecs.open(secondary_key_file, 'r', encoding='utf-8') as fo:
    for line in fo:
        secondary_key = line
        secondary_key = secondary_key.strip()
    print('1. list transcripts containing:', secondary_key)
    fo.close()
    if len(secondary_key) > 1:
        list_all()
