import os
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import time

url = 'http://www.defconlevel.com/'
print('searching '+ url)
rHead = requests.get(url)
data = rHead.text
soup = BeautifulSoup(data, "html.parser")

defcon_status = ''
for link in soup.find_all('a'):
    href = (link.get('href'))
    if href != None:
        if 'http://www.defconlevel.com/levels/' in href:
            defcon_status = href.replace('http://www.defconlevel.com/levels/', '')
            defcon_status = defcon_status.replace('.php', '')
print(defcon_status)

try:
    tts = gTTS(text=defcon_status, lang='en')
    tts.save("./plugins/MilitaryInformation/defcon_status.mp3")
    time.sleep(1)
    os.system("mpg321 " + '"' + "./plugins/MilitaryInformation/defcon_status.mp3" + '"')

except:
    pass
