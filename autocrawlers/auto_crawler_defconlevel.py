#!/usr/bin/python3.5

import os
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import time
import subprocess

while True:

    try:
        
        write_status = False
        defcon_change = False

        url = ('http://www.defconlevel.com/')
        print('searching '+url)
        rHead  = requests.get(url)
        data = rHead.text
        soup = BeautifulSoup(data, "html.parser")

        defcon_status = ''
        for link in soup.find_all('a'):
            href = (link.get('href'))
            if href != None:
                if 'http://www.defconlevel.com/levels/' in href:
                    defcon_status = href.replace('http://www.defconlevel.com/levels/', '')
                    defcon_status = defcon_status.replace('.php', '')
                    defcon_status = defcon_status.strip()
        print('current status:', defcon_status)

        if not os.path.exists('./temporary/def_con_status.tmp'):
            print('creating new file')
            open('./temporary/def_con_status.tmp', 'w').close()
            with open('./temporary/def_con_status.tmp', 'w') as fo:
                fo.writelines(defcon_status)
            fo.close()

        with open('./temporary/def_con_status.tmp', 'r') as fo:
            for line in fo:
                previous_defcon_status = line.strip()
                print('previous status:', previous_defcon_status)
            fo.close()

        if defcon_status != previous_defcon_status:
            print('status changed: writing new status')
            with open('./temporary/def_con_status.tmp', 'w') as fo:
                fo.writelines(defcon_status)
            fo.close()
            
            text = 'defcon status changed: '+defcon_status
            tts = gTTS(text=text, lang='en')
            tts.save("./transcripts/defcon_status.mp3")
            time.sleep(1)
            os.system("mpg321 " + '"' + "./transcripts/defcon_status.mp3" + '"')
    except:
        time.sleep(180)
        pass
    time.sleep(180)
