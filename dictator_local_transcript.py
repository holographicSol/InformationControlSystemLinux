import os
import codecs
import distutils.dir_util
import subprocess

curDir = os.getcwd()
path = './transcripts/'
secondary_key = './temporary/secondary-key.tmp'
target_transcript = ''
distutils.dir_util.mkpath(path)

target_found = False


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


# print('1. retrieving stored search string')        
with codecs.open(secondary_key, 'r', encoding='utf-8') as infile:
    for line in infile:
        secondary_key_str = line
        secondary_key_str = secondary_key_str.strip()
    print('requested transcript:', secondary_key_str)
    infile.close()

# print('3. retrieving stored transcripts')
for dirName, subdirList, fileList in os.walk(path):
    for fname in fileList:
        if fname.endswith('.mp3'):
            if secondary_key_str in fname:
                target_transcript = os.path.join(curDir, dirName, fname)
                print('found:', target_transcript)
                target_found = True
                    
if target_found == True:
    found_sound()
    os.system("mpg321 " + '"' + target_transcript + '"')
else:
    not_found_sound()
    print("couldn't find anything...")
