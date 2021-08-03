import os
import codecs
import requests
from bs4 import BeautifulSoup
import distutils.dir_util
import re
import webbrowser
from gtts import gTTS
import time
import subprocess

# Files
path = './transcripts/'
secondary_key = './temporary/secondary-key.tmp'
system_config_file = './configuration/system_config.conf'
distutils.dir_util.mkpath(path)

# Data
article_name = ''
text_paragraph = []
name = ''
initial_found_file = False
show_browser = False
dictation = False
use_local_server = False
local_server_addr = ''
local_server_port = ''
found_file = False
trigger = True


def found_sound():
    found_sound_file = './resources/sound/found_sound.mp3'
    cmd = 'mpg321 ' + found_sound_file
    subprocess.Popen(cmd,
                     shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


def not_found_sound():
    not_found_sound_file = './resources/sound/not_found_sound.mp3'
    cmd = 'mpg321 ' + not_found_sound_file
    subprocess.Popen(cmd,
                     shell=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)


def conf_write():
    global name
    line_list = []
    with codecs.open(system_config_file, 'r', encoding="utf-8") as fo:
        for line in fo:
            line_list.append(line)
    i = 0
    for line_lists in line_list:
        if line_list[i].startswith('TRANSCRIPT_NAME: '):
            line_list[i] = str('TRANSCRIPT_NAME: ' + name + '\n')
        i += 1
    fo.close()
    i = 0
    with codecs.open(system_config_file, 'w', encoding="utf-8") as fo:
        for line_lists in line_list:
            fo.writelines(line_list[i])
            i += 1
    fo.close()
    print('updated: system_config.conf')


def compile_audio_tracks():
    global found_file
    global name
    global trigger
    i = 0
    x = ()
    conf_write()
    for text_paragraphs in text_paragraph:
        track = text_paragraph[i]
        tts = gTTS(text=track, lang='en')
        track_no = str(i)
        tts.save("./transcripts/" + name + "_track_" + track_no + ".mp3")
        if trigger == True:
            try:
                if os.path.exists("./transcripts/" + name + "_track_0.mp3"):
                    track_size = os.stat("./transcripts/" + name + "_track_0.mp3").st_size
                    if track_size > 1:
                        cmd = 'python3.5 ./dictator_wikipedia.py'
                        x = subprocess.Popen(cmd,
                                             shell=True,
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        trigger = False
            except:
                print('waiting for first transcript')
        i += 1
    time.sleep(1)
    print('audio information compiled')
    print('waiting for process to finish')
    x.wait()
    x.terminate()
    x.communicate()


def found():
    global local_server_addr
    global local_server_port
    global use_local_server
    global name
    global found_file
    global dictation
    global show_browser

    conf_write()
    found_sound()
    url = ''
    print('plugged in : found function')
    if use_local_server == True:
        name = name.title()
        name = name.replace(' ', '_')
        url = (local_server_addr+':'+local_server_port+'/wikipedia/A/'+name+'.html')
        url = url.strip()
        print('searching local url:',url)

    if use_local_server == False:
        url = ("https://www.wikipedia.org/wiki/" + name)

    if show_browser == True:
        webbrowser.open(url)

    if dictation == True:
        open('./temporary/track_list.tmp', 'w').close()

        if os.path.exists("./transcripts/" + name + "_track_0.mp3"):
            cmd = 'python3.5 ./dictator_wikipedia.py'
            x = subprocess.Popen(cmd,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            x.wait()
            x.terminate()
            x.communicate()


def not_found():
    global name
    global local_server_port
    global local_server_addr
    global use_local_server
    global dictation
    global show_browser

    print('plugged in: not found function')
    found_information = False
    url = ''
    article_name = (path+name+'.tmp')

    if use_local_server == True:
        name = name.title()
        name = name.replace(' ', '_')
        url = (local_server_addr+':'+local_server_port+'/wikipedia/A/'+name+'.html')
        url = url.strip()
        print('searching local url:',url)
    elif use_local_server == False:
        url = ("https://www.wikipedia.org/wiki/" + name)

    print('searching',url)
    rHead  = requests.get(url)
    data = rHead.text
    soup = BeautifulSoup(data, "html.parser")
    
    # opt 1
    open(article_name, 'w').close()
    for row in soup.find_all('p'):
        text = row.get_text()
        text = re.sub(r'\[.*?\]', '', text)
        text = (text+'\n')
        if len(text) > 1:
            found_information = True
            outFile = codecs.open(article_name, "a", encoding="utf-8")
            outFile.writelines(text)
            outFile.close()
        
    # opt 2
    if "refer to:" in text:
        open(article_name, 'w').close()
        outFile = codecs.open(article_name, "a", encoding="utf-8")
        outFile.writelines(name+' may refer to: \n')
        for row in soup.find_all('ul'):
            ref = row.get_text()
            ref = ref.strip()
            if name in ref:
                outFile = codecs.open(article_name, "a", encoding="utf-8")
                outFile.writelines(ref+'. ')
                found_information = True
        outFile.close()

    # opt 3
    if "Other reasons this message may be displayed:" in text:
        url = ''
        open(article_name, 'w').close()
        for link in soup.find_all('a'):
            y = (link.get('href'))
            if y == None:
                pass
            else:
                valuestring = name.replace(' ', '+')
                if valuestring in y:
                    if valuestring in y:
                        if y.startswith('//en.wikipedia.org/w/index.php?search='):
                            url = 'https:'+y
        print('redirecting:', url)
        try:
            rHead = requests.get(url)
            data = rHead.text
            soup = BeautifulSoup(data, "html.parser")
            for link in soup.find_all('a'):
                y = (link.get('href'))
                if y == None:
                    pass
                else:
                    ystring = y.lower()
                    ystring = ystring.replace('(', '')
                    ystring = ystring.replace(')', '')
                    valuestring = name.replace(' ','_')
                    valuestring = ('/wiki/'+valuestring).lower()
                    if valuestring in ystring:
                        print(y)
                        url = ('https://en.wikipedia.org'+y)
                        rHead  = requests.get(url)
                        data = rHead.text
                        soup = BeautifulSoup(data, "html.parser")
                        for row in soup.find_all('p'):
                            text = row.get_text()
                            if text == None:
                                pass
                            else:
                                text = re.sub(r'\[.*?\]', '', text)
                                text = (text+'\n')
                                text_len = len(text)
                                text_len = int(text_len)
                                if text_len > 1:
                                    outFile = codecs.open(article_name, "a", encoding="utf-8")
                                    outFile.writelines(text+'\n')
                                    found_information = True
                    elif valuestring not in ystring:
                        print(y)
            outFile.close()

        except:
            print('crawled and crawled redirects, no results')
            os.remove(article_name)
            found_information = False

    if found_information == True:
        with codecs.open(article_name, 'r', encoding='utf-8') as infile:
            for line in infile:
                if len(line) > 1:
                    text_paragraph.append(line)
            infile.close()
            found_sound()

            if show_browser == True:
                url = ("https://www.wikipedia.org/wiki/" + name)
                webbrowser.open(url)

            if dictation == True:
                i = 0
                compile_audio_tracks()

    elif found_information == False:
        not_found_sound()


def get_local_config_func():
    global local_server_port
    global local_server_addr
    global use_local_server
    global show_browser
    global dictation
    global name

    with codecs.open(secondary_key, 'r', encoding='utf-8') as infile:
        for line in infile:
            name = line.strip()
            name = name.title()
        infile.close()

    with open('./configuration/config.conf', 'r') as fo:
        for line in fo:
            line = line.strip()

            if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: enabled':
                print('show browser: enabled')
                show_browser = True

            if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: disabled':
                print('show browser: disabled')
                show_browser = False

            if line == 'WIKI_TRANSCRIPT_DICTATE: enabled':
                print('dictation: enabled')
                dictation = True

            if line == 'WIKI_TRANSCRIPT_DICTATE: disabled':
                print('dictation: disabled')
                dictation = False

            if line.startswith('ALLOW_WIKI_LOCAL_SERVER: enabled'):
                print('local wiki enabled: getting address and port configuration')
                use_local_server = True
                if line.startswith('WIKI_LOCAL_SERVER: '):
                    local_server_addr = line.replace('WIKI_LOCAL_SERVER: ', '')
                    local_server_addr = local_server_addr.strip()
                    print('local wiki server:', local_server_addr)

                if line.startswith('WIKI_LOCAL_SERVER_PORT: '):
                    local_server_port = line.replace('WIKI_LOCAL_SERVER_PORT: ', '')
                    local_server_port = local_server_port.strip()
                    print('local wiki port:', local_server_port)

            if line.startswith('ALLOW_WIKI_LOCAL_SERVER: disabled'):
                print('local wiki server disabled: using world wide web')
                use_local_server = False


get_local_config_func()

for dirName, subdirList, fileList in os.walk(path):
    for fname in fileList:
        if fname.endswith('.tmp'):
            if name in fname:
                print(fname)
                initial_found_file = True

if initial_found_file == True:
    print('found')
    found()
else:
    print('not found')
    not_found()
