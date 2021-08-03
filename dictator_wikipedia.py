import os
import subprocess
import codecs
import time
from gtts import gTTS

bookmark = ()
bookmark_str = ''
run_this = True
transcript_name = ''
bookmark_file = ''
dictate = True


# while line in system_config = True, iterate through tracks. check each time ensuring mpg321 does not restart if False.
def mainFunction():
    global run_this
    global bookmark_str
    global bookmark
    global transcript_name
    global dictate

    if bookmark != 0:
        text = transcript_name + 'bookmark found: paragraph, ' + bookmark_str
        tts = gTTS(text=text, lang='en')
        tts.save("./transcripts/bookmark_notification_2.mp3")
        time.sleep(1)
        cmd = "mpg321 " + "'./transcripts/bookmark_notification_2.mp3'"
        xcmd = subprocess.Popen(cmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        xcmd.wait()
        xcmd.terminate()
        xcmd.communicate()

    while run_this == True:
        with open('./configuration/system_config.conf', 'r') as fo1:
            for line in fo1:
                line = line.strip()
                if line == 'DICTATE_TRANSCRIPT: True':
                    dictate = True
                elif line == 'DICTATE_TRANSCRIPT: False':
                    dictate = False

        if dictate == True:
            print('dictate: True')
            cmd = "mpg321 " + '"./transcripts/' + transcript_name + '_track_' + bookmark_str + '.mp3' + '"'
            print(cmd)
            x = subprocess.Popen(cmd,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            x.wait()
            x.terminate()
            x.communicate()
            bookmark += 1
            bookmark_str = str(bookmark)
            with open(bookmark_file, 'w') as write_bm:
                print('bookmark:', bookmark)
                write_bm.writelines(bookmark_str)
            write_bm.close()

        elif dictate == False:

            print('dictate: False')
            with open('./temporary/primary-key.tmp', 'r') as primary_key_file:
                for line in primary_key_file:
                    primary_key = line.strip()
                    if not primary_key.startswith('remove bookmark'):

                        # write bookmark on exit
                        if bookmark > 0:
                            bookmark -= 1
                            bookmark_str = str(bookmark)
                        with open(bookmark_file, 'w') as write_bm:
                            print('making bookmark:', bookmark)
                            write_bm.writelines(bookmark_str)
                        text = 'placing bookmark: ' + bookmark_str + '. in article ' + transcript_name
                        tts = gTTS(text=text, lang='en')
                        tts.save("./transcripts/bookmark_notification_2.mp3")
                        time.sleep(1)
                        cmd = "mpg321 " + '"./transcripts/bookmark_notification_2.mp3' + '"'
                        x = subprocess.Popen(cmd,
                                             shell=True,
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        x.wait()
                        x.terminate()
                        x.communicate()
                print('quitting while loop')
                run_this = False


def config():
    global transcript_name
    line_list = []
    with codecs.open('./configuration/system_config.conf', 'r', encoding="utf-8") as fo:
        for line in fo:
            line_list.append(line)
    i = 0
    for line_lists in line_list:
        if line_list[i].startswith('DICTATE_TRANSCRIPT: '):
            line_list[i] = str('DICTATE_TRANSCRIPT: True' + '\n')
        i += 1
    fo.close()
    i = 0
    with codecs.open('./configuration/system_config.conf', 'w', encoding="utf-8") as fo:
        for line_lists in line_list:
            fo.writelines(line_list[i])
            i += 1
    fo.close()
    print('updated: system_config.conf')

    # get requested transcript name.
    with open('./configuration/system_config.conf', 'r') as fo0:
        for line in fo0:
            if line.startswith('TRANSCRIPT_NAME: '):
                line = line.strip()
                transcript_name = line.replace('TRANSCRIPT_NAME: ', '')
        fo0.close()


# create/get bookmark.
def createGetBookmark():
    global bookmark
    global bookmark_str
    global bookmark_file
    bookmark_file = './temporary/'+transcript_name+'_bookmark.tmp'
    if not os.path.exists(bookmark_file):
        with open(bookmark_file, 'w') as write_bm:
            write_bm.writelines('0')
            bookmark = 0
            bookmark_str = '0'
        write_bm.close()
    elif os.path.exists(bookmark_file):
        with open(bookmark_file, 'r') as read_bm:
            for line in read_bm:
                bookmark = int(line)
                bookmark_str = str(line)
    print('bookmark:', bookmark)


config()
createGetBookmark()
mainFunction()
