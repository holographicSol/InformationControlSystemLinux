import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import time
import subprocess


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


print('plugged in: transcript-wiktionary-define.py')

secondary_key_store = './temporary/secondary-key.tmp'

with open(secondary_key_store, 'r', encoding='utf-8') as fo:
    for line in fo:
        line = line.strip()

url = ("https://en.wiktionary.org/wiki/" + line)
print('searching ' + url)
rHead = requests.get(url)
data = rHead.text
soup = BeautifulSoup(data)
print('Define Word:', line)

text = ''
for row in soup.find_all('ol'):
    text = row.get_text()
    text = text.strip()
    if text != line:
        text = line + '. ' + text

try:
    tts = gTTS(text=text, lang='en')
    found_sound()
    tts.save("./transcripts/define_" + line + ".mp3")
    time.sleep(1)
    cmd = "mpg321 " + "'" + "./transcripts/define_" + line + ".mp3" + "'"
    play_definition = subprocess.Popen(cmd,
                                       shell=True,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

except:
    not_found_sound()
    pass
