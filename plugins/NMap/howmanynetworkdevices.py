import os
import subprocess
from gtts import gTTS
import time

device_count = 0
default_gate_prepared = ''
host_list = './plugins/NMap/host_count.xml'

with open('./configuration/config.conf', 'r') as fo:
    for line in fo:
        if line.startswith('DEFAULT_GATEWAY: '):
            default_gateway = line.replace('DEFAULT_GATEWAY: ', '')
            print('found default gateway in config:', default_gateway)
            idx = default_gateway.rfind('.', 1)
            default_gate_prepared = default_gateway[:idx]

cmd = 'nmap -sL '+default_gate_prepared+'.0/24 -oX '+host_list
print('command:', cmd)

xcmd = subprocess.Popen(cmd,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
xcmd.wait()

if os.path.exists(host_list):
    hostListRead = open(host_list, 'r')
    for line in hostListRead:
        txt = '<hostname name='
        if line.startswith(txt):
            device_count += 1
            print(device_count)
    hostListRead.close()
    os.remove(host_list)

if device_count > 1:
    device_plural_singular = 'devices'
if device_count == 0:
    device_plural_singular = 'devices'
elif device_count == 1:
    device_plural_singular = 'device'

device_count = str(device_count)
print('device count:', device_count)
text = device_count + ' network ' + device_plural_singular

try:
    tts = gTTS(text=text, lang='en')
    tts.save("./plugins/NMap/device_count.mp3")
    time.sleep(1)
    os.system("mpg321 " + '"' + "./plugins/NMap/device_count.mp3" + '"')
except:
    pass
