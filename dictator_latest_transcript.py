import os
import time
import codecs
from operator import itemgetter
from gtts import gTTS
import subprocess

# Files
curDir = os.getcwd()
path = ''
secondary_key_file = './temporary/secondary-key.tmp'
article_path = 'transcripts/'

# lists
article = []
newest_list = []
time_keeper = []

# Data
found_file = False
secondary_key = ''
newest_file = ''
newest_file_human = ''


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


# 3.
def found_one_newest():
    global newest_file_human
    global newest_file
    newest_file_human = newest_file.replace('.tmp', '')
    print('latest transcription for ' + secondary_key + ': ' + newest_file_human + ' ' + dated_files2)
    text = 'latest transcription for:' + newest_file_human + ' : ' + dated_files2
    tts = gTTS(text=text, lang='en')
    tts.save("./transcripts/latest_transcription.mp3")
    time.sleep(1)
    os.system("mpg321 " + "./transcripts/latest_transcription.mp3")


# 0. Get Key
with codecs.open(secondary_key_file, 'r', encoding='utf-8') as fo:
    for line in fo:
        secondary_key = line

# 1. Append all transcripts to list article
for dirName, subdirList, fileList in os.walk(article_path):
    for fname in fileList:
        lnkext = [".tmp", ".txt"]
        if fname.endswith(tuple(lnkext)):
            fname_path = os.path.join(curDir, dirName, fname)
            # print(fname_path)
            article.append(fname_path)

# 2. Get timestamp for all files names containing value & append to newest_plural
i = 0
article_length = len(article)
print(article_length)
article_length -= 1
for articles in article:
    dated_files = [(os.path.getmtime(article[i]), os.path.basename(article[i]))]
    dated_files2 = time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(article[i])))
    print(article[i], dated_files2)
    if secondary_key in article[i]:
        if article[i].endswith('.tmp'):
            dated_files.sort()
            dated_files.reverse()
            if len(dated_files) >= 1:
                newest = dated_files[0]
                newest_list.append(newest)
                print('checking:', newest)
                newest_file = max(newest_list, key=itemgetter(0))[1]
                found_file = True
    else:
        i += 1

if found_file == True:
    found_sound()
    found_one_newest()
elif found_file == False:
    not_found_sound()
