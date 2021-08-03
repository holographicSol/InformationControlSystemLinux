import os
import subprocess
from gtts import gTTS
import time

default_gate_prepared = ''
host_list = './plugins/NMap/host_name_list.xml'

with open('./configuration/config.conf', 'r') as fo:
    for line in fo:
        if line.startswith('DEFAULT_GATEWAY: '):
            default_gateway = line.replace('DEFAULT_GATEWAY: ', '')
            print('found default gateway in config:', default_gateway)
            idx = default_gateway.rfind('.', 1)
            default_gate_prepared = default_gateway[:idx]

cmd = 'nmap -sL ' + default_gate_prepared + '.0/24 -oX ' + host_list
print('command:', cmd)

xcmd = subprocess.Popen(cmd,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
xcmd.wait()

host_names = 'local online host names: '
if os.path.exists(host_list):
    hostListRead = open(host_list, 'r')
    for line in hostListRead:
        txt = '<hostname name='
        if line.startswith(txt):
            line = line.strip()
            line = line[16:]
            line = line.split('"')[0]
            print('Found Host: ', line)
            host_names = host_names + '. ' + line
    hostListRead.close()
    os.remove(host_list)

try:
    text = str(host_names)
    tts = gTTS(text=text, lang='en')
    tts.save("./plugins/NMap/host_names.mp3")
    time.sleep(1)
    os.system("mpg321 " + '"' + './plugins/NMap/host_names.mp3' + '"')
except:
    pass
