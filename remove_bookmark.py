import os
import subprocess
from gtts import gTTS
import time

target_found = False
bookmark_file = ''
curDir = os.getcwd()
secondary_key = ''


def found_sound():
    found_plugin_file_sound = './resources/sound/found_sound.mp3'
    cmd = 'mpg321 ' + found_plugin_file_sound
    subprocess.Popen(cmd,
                     shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


def not_found_sound():
    not_found_plugin_file_sound = './resources/sound/not_found_sound.mp3'
    cmd = 'mpg321 ' + not_found_plugin_file_sound
    subprocess.Popen(cmd,
                     shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


with open('./temporary/secondary-key.tmp', 'r') as fo:
    for line in fo:
        secondary_key = line.strip()
        print('secondary key:', secondary_key)

for dirName, subdirList, fileList in os.walk('temporary'):
    for fname in fileList:
        if fname.endswith('.tmp'):
            if secondary_key in fname:
                if fname.endswith('_bookmark.tmp'):
                    print('found:', fname)
                    bookmark_file = fname
                    target_found = True

if target_found == True:
    found_sound()
    text = 'bookmark found: '+bookmark_file.replace('.tmp', '')
    text = text.replace('_', ' ')
    text = text + '. Removing bookmark.'
    tts = gTTS(text=text, lang='en')
    tts.save("./transcripts/remove_bookmark.mp3")
    time.sleep(1)
    remove_bookmark_audio = './transcripts/remove_bookmark.mp3'
    cmd = 'mpg321 ' + remove_bookmark_audio
    xcmd = subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    xcmd.wait()
    xcmd.terminate()
    xcmd.communicate()
    with open('./temporary/'+bookmark_file, 'w') as write_bookmark:
        write_bookmark.writelines('0')
    write_bookmark.close()

else:
    not_found_sound()
    text = secondary_key + ' bookmark not found'
    tts = gTTS(text=text, lang='en')
    tts.save("./transcripts/remove_bookmark.mp3")
    time.sleep(1)
    remove_bookmark_audio = './transcripts/remove_bookmark.mp3'
    cmd = 'mpg321 ' + remove_bookmark_audio
    xcmd = subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    xcmd.wait()
    xcmd.terminate()
    xcmd.communicate()

open('./temporary/primary-key.tmp', 'w').close()
