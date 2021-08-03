import os
import sys
import time
import codecs
import socket
import os.path
import subprocess
import unicodedata
import distutils.dir_util
import speech_recognition as sr
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QApplication, QLabel

auto_crawler = []
auto_crawler_pid = []
auto_crawler_xcmd = []
plugin_dir = './plugins'
transcripts_dir = './transcripts'
resources_dir = './resources'
tmp_dir = './temporary'
config_dir = './configuration'
log_dir = './log'

distutils.dir_util.mkpath(plugin_dir)
distutils.dir_util.mkpath(resources_dir)
distutils.dir_util.mkpath(transcripts_dir)
distutils.dir_util.mkpath(tmp_dir)
distutils.dir_util.mkpath(config_dir)
distutils.dir_util.mkpath(log_dir)

config_file = './configuration/config.conf'
secondary_key_store = './temporary/secondary-key.tmp'
primary_key_store = './temporary/primary-key.tmp'

incrementalResize = 0

speechRecognitionThread = ()
guiControllerThread = ()
drawMenuThread = ()
openDirectoryThread = ()
findOpenAudioThread = ()
findOpenImageThread = ()
findOpenTextThread = ()
findOpenVideoThread = ()
findOpenProgramThread = ()
configInteractionPermissionThread = ()
symbiotServerThread = ()

value = ''
primary_key = ''
secondary_key = ''

encode = u'\u5E73\u621015\u200e'


def nfd(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return nfd(nfd(text).casefold())


check_allow_symbiot_config = False
check_symbiot_ip_config = False
check_symbiot_mac_config = False
check_symbiot_server_ip_config = False
check_symbiot_server_port_config = False
check_index_audio_config = False
check_index_video_config = False
check_index_image_config = False
check_index_text_config = False
check_index_drive1_config = False
check_index_drive2_config = False
check_index_drive3_config = False
check_index_drive4_config = False
check_index_drive5_config = False
check_index_drive6_config = False
check_index_drive7_config = False
check_index_drive8_config = False
check_wiki_local_server_ip = False
check_wiki_local_server_port = False
symbiot_configuration = ''
symbiot_server_ip_configuration = ''
symbiot_server_port_configuration = ''
symbiot_ip_configuration = ''
symbiot_mac_configuration = ''
symbiot_configuration_bool = False
symbiot_server_ip_configuration_bool = False
symbiot_server_port_configuration_bool = False
symbiot_ip_configuration_bool = False
symbiot_mac_configuration_bool = False
allow_wiki_local_server_configuration = ''
wiki_local_server_ip_configuration = ''
wiki_local_server_port_configuration = ''
wiki_dictate_configuration = ''
wiki_show_browser_configuration = ''
wiki_show_browser_bool = False
wiki_dictate_bool = False
allow_wiki_local_server_bool = False
wiki_local_server_ip_configuration_bool = False
wiki_local_server_port_configuration_bool = False
audio_configuration = ''
video_configuration = ''
image_configuration = ''
text_configuration = ''
drive1_configuration = ''
drive2_configuration = ''
drive3_configuration = ''
drive4_configuration = ''
drive5_configuration = ''
drive6_configuration = ''
drive7_configuration = ''
drive8_configuration = ''
audio_active_config = ''
audio_active_config_bool = ()
video_active_config = ''
video_active_config_bool = ()
image_active_config = ''
image_active_config_bool = ()
text_active_config = ''
text_active_config_bool = ()
drive_1_active_config = ''
drive_1_active_config_bool = ()
drive_2_active_config = ''
drive_2_active_config_bool = ()
drive_3_active_config = ''
drive_3_active_config_bool = ()
drive_4_active_config = ''
drive_4_active_config_bool = ()
drive_5_active_config = ''
drive_5_active_config_bool = ()
drive_6_active_config = ''
drive_6_active_config_bool = ()
drive_7_active_config = ''
drive_7_active_config_bool = ()
drive_8_active_config = ''
drive_8_active_config_bool = ()


def configuration_checks_function():
    global check_allow_symbiot_config
    global symbiot_configuration
    global symbiot_configuration_bool
    global symbiot_server_ip_configuration
    global symbiot_server_port_configuration
    global symbiot_ip_configuration
    global symbiot_mac_configuration
    global symbiot_server_ip_configuration_bool
    global symbiot_server_port_configuration_bool
    global symbiot_ip_configuration_bool
    global symbiot_mac_configuration_bool

    global wiki_local_server_ip_configuration_bool
    global wiki_local_server_port_configuration_bool
    global wiki_local_server_ip_configuration
    global wiki_local_server_port_configuration
    global wiki_dictate_bool
    global wiki_show_browser_bool
    global allow_wiki_local_server_bool
    global wiki_show_browser_configuration
    global wiki_dictate_configuration
    global allow_wiki_local_server_configuration

    global check_index_audio_config
    global audio_configuration
    global audio_active_config
    global audio_active_config_bool

    global check_index_video_config
    global video_configuration
    global video_active_config
    global video_active_config_bool

    global check_index_image_config
    global image_configuration
    global image_active_config
    global image_active_config_bool

    global check_index_text_config
    global text_configuration
    global text_active_config
    global text_active_config_bool

    global check_index_drive1_config
    global drive1_configuration
    global drive_1_active_config
    global drive_1_active_config_bool

    global check_index_drive2_config
    global drive2_configuration
    global drive_2_active_config
    global drive_2_active_config_bool

    global check_index_drive3_config
    global drive3_configuration
    global drive_3_active_config
    global drive_3_active_config_bool

    global check_index_drive4_config
    global drive4_configuration
    global drive_4_active_config
    global drive_4_active_config_bool

    global check_index_drive5_config
    global drive5_configuration
    global drive_5_active_config
    global drive_5_active_config_bool

    global check_index_drive6_config
    global drive6_configuration
    global drive_6_active_config
    global drive_6_active_config_bool

    global check_index_drive7_config
    global drive7_configuration
    global drive_7_active_config
    global drive_7_active_config_bool

    global check_index_drive8_config
    global drive8_configuration
    global drive_8_active_config
    global drive_8_active_config_bool

    global auto_crawler
    global auto_crawler_pid
    global auto_crawler_xcmd

    print('attempting to gather auto crawlers')
    files = [f for f in os.listdir('./autocrawlers/')]
    for f in files:
        if f.startswith('auto_crawler'):
            print('found auto crawler:', f)
            auto_crawler.append(f)
    i = 0
    print('attempting to start auto crawlers')
    for auto_crawlers in auto_crawler:
        cmd = 'python3.5 ./autocrawlers/' + auto_crawler[i]
        print('command:', cmd)
        xcmd = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        auto_crawler_pid_i = xcmd.pid
        print(auto_crawler[i], 'PID:', auto_crawler_pid_i)
        auto_crawler_pid.append(auto_crawler_pid_i)
        auto_crawler_xcmd.append(xcmd)
        i += 1

    with open(config_file, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: disabled':
                wiki_show_browser_bool = False
                wiki_show_browser_configuration = line.replace('WIKI_TRANSCRIPT_SHOW_BROWSER: ', '')
                print('show wiki pages: false')
            if line == 'WIKI_TRANSCRIPT_SHOW_BROWSER: enabled':
                wiki_show_browser_bool = True
                wiki_show_browser_configuration = line.replace('WIKI_TRANSCRIPT_SHOW_BROWSER: ', '')
                print('show wiki pages: true')

            if line == 'WIKI_TRANSCRIPT_DICTATE: enabled':
                wiki_dictate_bool = True
                wiki_dictate_configuration = line.replace('WIKI_TRANSCRIPT_DICTATE: ', '')
                print('dictate wiki pages: true')
            if line == 'WIKI_TRANSCRIPT_DICTATE: disabled':
                wiki_dictate_bool = False
                wiki_dictate_configuration = line.replace('WIKI_TRANSCRIPT_DICTATE: ', '')
                print('dictate wiki pages: false')

            if line == 'ALLOW_WIKI_LOCAL_SERVER: disabled':
                allow_wiki_local_server_bool = False
                allow_wiki_local_server_configuration = line.replace('ALLOW_WIKI_LOCAL_SERVER: ', '')
                print('using local wiki server: false')
            if line == 'ALLOW_WIKI_LOCAL_SERVER: enabled':
                allow_wiki_local_server_bool = True
                allow_wiki_local_server_configuration = line.replace('ALLOW_WIKI_LOCAL_SERVER: ', '')
                print('using local wiki server: true')

            if line.startswith('WIKI_LOCAL_SERVER: '):
                wiki_local_server_ip_configuration = line.replace('WIKI_LOCAL_SERVER: ', '')
                print('local wiki server:', wiki_local_server_ip_configuration)
            if line.startswith('WIKI_LOCAL_SERVER_PORT: '):
                wiki_local_server_port_configuration = line.replace('WIKI_LOCAL_SERVER_PORT: ', '')
                print('local wiki server port:', wiki_local_server_port_configuration)

            if line == 'ALLOW_SYMBIOT: TRUE':
                symbiot_configuration_bool = True
                symbiot_configuration = 'Enabled'
                print('symbiot: enabled')
            if line == 'ALLOW_SYMBIOT: FALSE':
                symbiot_configuration_bool = False
                symbiot_configuration = 'Disabled'
                print('symbiot: disabled')
            if line.startswith('SYMBIOT_SERVER: '):
                if line != 'SYMBIOT_SERVER: ':
                    line = line.replace('SYMBIOT_SERVER: ', '')
                    symbiot_server_ip_configuration = line
                    print('symbiot server ip config:', symbiot_server_ip_configuration)
            if line.startswith('SYMBIOT_SERVER_PORT: '):
                if line != 'SYMBIOT_SERVER_PORT: ':
                    line = line.replace('SYMBIOT_SERVER_PORT: ', '')
                    symbiot_server_port_configuration = line
                    print('symbiot server port config:', symbiot_server_port_configuration)
            if line.startswith('SYMBIOT_IP: '):
                if line != 'SYMBIOT_IP: ':
                    line = line.replace('SYMBIOT_IP: ', '')
                    symbiot_ip_configuration = line
                    print('symbiot ip config:', symbiot_ip_configuration)
            if line.startswith('SYMBIOT_MAC: '):
                if line != 'SYMBIOT_MAC: ':
                    line = line.replace('SYMBIOT_MAC: ', '')
                    symbiot_mac_configuration = line
                    print('symbiot mac config:', symbiot_mac_configuration)

            if line.startswith('DIRAUD: '):
                line2 = line.replace('DIRAUD: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_audio_config = True
                    print('check index audio config: path exists')
                    audio_configuration = line
                elif not os.path.exists(line2):
                    print('audio path in configuration: invalid')
            if line.startswith('INDEXENGINE_AUDIO: '):
                if line.endswith('disabled'):
                    audio_active_config = 'Disabled'
                    audio_active_config_bool = False
                    print('index audio active: disabled')
                elif line.endswith('enabled'):
                    audio_active_config = 'Enabled'
                    audio_active_config_bool = True
                    print('index audio active: enabled')

            if line.startswith('DIRVID: '):
                line2 = line.replace('DIRVID: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_video_config = True
                    print('check index video config: path exists')
                    video_configuration = line
                elif not os.path.exists(line2):
                    print('video path in configuration: invalid')
            if line.startswith('INDEXENGINE_VIDEO: '):
                if line.endswith('disabled'):
                    video_active_config = 'Disabled'
                    video_active_config_bool = False
                    print('index video active: disabled')
                elif line.endswith('enabled'):
                    video_active_config = 'Enabled'
                    video_active_config_bool = True
                    print('index video active: enabled')

            if line.startswith('DIRIMG: '):
                line2 = line.replace('DIRIMG: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_image_config = True
                    print('check index image config: path exists')
                    image_configuration = line
                elif not os.path.exists(line2):
                    print('video path in configuration: invalid')
            if line.startswith('INDEXENGINE_IMAGE: '):
                if line.endswith('disabled'):
                    image_active_config = 'Disabled'
                    image_active_config_bool = False
                    print('index image active: disabled')
                elif line.endswith('enabled'):
                    image_active_config = 'Enabled'
                    image_active_config_bool = True
                    print('index image active: enabled')

            if line.startswith('DIRTXT: '):
                line2 = line.replace('DIRTXT: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_text_config = True
                    print('check index text config: path exists')
                    text_configuration = line
                elif not os.path.exists(line2):
                    print('text path in configuration: invalid')
            if line.startswith('INDEXENGINE_TEXT: '):
                if line.endswith('disabled'):
                    text_active_config = 'Disabled'
                    text_active_config_bool = False
                    print('index text active: disabled')
                elif line.endswith('enabled'):
                    text_active_config = 'Enabled'
                    text_active_config_bool = True
                    print('index text active: enabled')

            if line.startswith('DRIVE1: '):
                line2 = line.replace('DRIVE1: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive1_config = True
                    print('check index drive1 config: path exists')
                    drive1_configuration = line
                elif not os.path.exists(line2):
                    print('drive1 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE1: '):
                if line.endswith('disabled'):
                    drive_1_active_config = 'Disabled'
                    drive_1_active_config_bool = False
                    print('index drive1 active: disabled')
                elif line.endswith('enabled'):
                    drive_1_active_config = 'Enabled'
                    drive_1_active_config_bool = True
                    print('index drive1 active: enabled')

            if line.startswith('DRIVE2: '):
                line2 = line.replace('DRIVE2: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive2_config = True
                    print('check index drive2 config: path exists')
                    drive2_configuration = line
                elif not os.path.exists(line2):
                    print('drive2 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE2: '):
                if line.endswith('disabled'):
                    drive_2_active_config = 'Disabled'
                    drive_2_active_config_bool = False
                    print('index drive2 active: disabled')
                elif line.endswith('enabled'):
                    drive_2_active_config = 'Enabled'
                    drive_2_active_config_bool = True
                    print('index drive2 active: enabled')

            if line.startswith('DRIVE3: '):
                line2 = line.replace('DRIVE3: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive3_config = True
                    print('check index drive3 config: path exists')
                    drive3_configuration = line
                elif not os.path.exists(line2):
                    print('drive3 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE3: '):
                if line.endswith('disabled'):
                    drive_3_active_config = 'Disabled'
                    drive_3_active_config_bool = False
                    print('index drive3 active: disabled')
                elif line.endswith('enabled'):
                    drive_3_active_config = 'Enabled'
                    drive_3_active_config_bool = True
                    print('index drive3 active: enabled')

            if line.startswith('DRIVE4: '):
                line2 = line.replace('DRIVE4: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive4_config = True
                    print('check index drive4 config: path exists')
                    drive4_configuration = line
                elif not os.path.exists(line2):
                    print('drive4 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE4: '):
                if line.endswith('disabled'):
                    drive_4_active_config = 'Disabled'
                    drive_4_active_config_bool = False
                    print('index drive4 active: disabled')
                elif line.endswith('enabled'):
                    drive_4_active_config = 'Enabled'
                    drive_4_active_config_bool = True
                    print('index drive4 active: enabled')

            if line.startswith('DRIVE5: '):
                line2 = line.replace('DRIVE5: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive5_config = True
                    print('check index drive5 config: path exists')
                    drive5_configuration = line
                elif not os.path.exists(line2):
                    print('drive5 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE5: '):
                if line.endswith('disabled'):
                    drive_5_active_config = 'Disabled'
                    drive_5_active_config_bool = False
                    print('index drive5 active: disabled')
                elif line.endswith('enabled'):
                    drive_5_active_config = 'Enabled'
                    drive_5_active_config_bool = True
                    print('index drive5 active: enabled')

            if line.startswith('DRIVE6: '):
                line2 = line.replace('DRIVE6: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive6_config = True
                    print('check index drive6 config: path exists')
                    drive6_configuration = line
                elif not os.path.exists(line2):
                    print('drive6 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE6: '):
                if line.endswith('disabled'):
                    drive_6_active_config = 'Disabled'
                    drive_6_active_config_bool = False
                    print('index drive6 active: disabled')
                elif line.endswith('enabled'):
                    drive_6_active_config = 'Enabled'
                    drive_6_active_config_bool = True
                    print('index drive6 active: enabled')

            if line.startswith('DRIVE7: '):
                line2 = line.replace('DRIVE7: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive7_config = True
                    print('check index drive7 config: path exists')
                    drive7_configuration = line
                elif not os.path.exists(line2):
                    print('drive7 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE7: '):
                if line.endswith('disabled'):
                    drive_7_active_config = 'Disabled'
                    drive_7_active_config_bool = False
                    print('index drive7 active: disabled')
                elif line.endswith('enabled'):
                    drive_7_active_config = 'Enabled'
                    drive_7_active_config_bool = True
                    print('index drive7 active: enabled')

            if line.startswith('DRIVE8: '):
                line2 = line.replace('DRIVE8: ', '')
                line2 = line2.strip()
                if os.path.exists(line2):
                    check_index_drive8_config = True
                    print('check index drive8 config: path exists')
                    drive8_configuration = line
                elif not os.path.exists(line2):
                    print('drive8 path in configuration: invalid')
            if line.startswith('INDEXENGINE_DRIVE8: '):
                if line.endswith('disabled'):
                    drive_8_active_config = 'Disabled'
                    drive_8_active_config_bool = False
                    print('index drive8 active: disabled')
                elif line.endswith('enabled'):
                    drive_8_active_config = 'Enabled'
                    drive_8_active_config_bool = True
                    print('index drive8 active: enabled')

    if check_index_audio_config == False:
        print('check index audio config: missing/malformed data... creating default configuration')
        defaultAudioPath = os.path.join(os.path.expanduser('~'),'Music')
        with open(config_file, 'a') as fo:
            fo.writelines('DIRAUD: '+defaultAudioPath+'\n')
            check_index_audio_config = True
            audio_configuration = defaultAudioPath
        fo.close()
    if check_index_video_config == False:
        print('check index video config: missing/malformed data... creating default configuration')
        defaultVideoPath = os.path.join(os.path.expanduser('~'), 'Videos')
        with open(config_file, 'a') as fo:
            fo.writelines('DIRVID: ' + defaultVideoPath+'\n')
            check_index_video_config = True
            video_configuration = defaultVideoPath
        fo.close()
    if check_index_image_config == False:
        print('check index image config: missing/malformed data... creating default configuration')
        defaultImagePath = os.path.join(os.path.expanduser('~'), 'Pictures')
        with open(config_file, 'a') as fo:
            fo.writelines('DIRIMG: ' + defaultImagePath+'\n')
            check_index_image_config = True
            image_configuration = defaultImagePath
        fo.close()
    if check_index_text_config == False:
        print('check index text config: missing/malformed data... creating default configuration')
        defaultTextPath = os.path.join(os.path.expanduser('~'), 'Documents')
        with open(config_file, 'a') as fo:
            fo.writelines('DIRTXT: ' + defaultTextPath+'\n')
            check_index_text_config = True
            text_configuration = defaultTextPath
        fo.close()
    if check_index_drive1_config == False:
        defaultDrive1Config = 'null'
        drive1_configuration = defaultDrive1Config
    if check_index_drive2_config == False:
        defaultDrive2Config = 'null'
        drive2_configuration = defaultDrive2Config
    if check_index_drive3_config == False:
        defaultDrive3Config = 'null'
        drive3_configuration = defaultDrive3Config
    if check_index_drive4_config == False:
        defaultDrive4Config = 'null'
        drive4_configuration = defaultDrive4Config
    if check_index_drive5_config == False:
        defaultDrive5Config = 'null'
        drive5_configuration = defaultDrive5Config
    if check_index_drive6_config == False:
        defaultDrive6Config = 'null'
        drive6_configuration = defaultDrive6Config
    if check_index_drive7_config == False:
        defaultDrive7Config = 'null'
        drive7_configuration = defaultDrive7Config
    if check_index_drive8_config == False:
        defaultDrive8Config = 'null'
        drive8_configuration = defaultDrive8Config


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


def remove_bookmark_function():
    global speechRecognitionThread
    global secondary_key
    stop_transcription_function()
    print('plugged in: remove bookmark function')
    cmd = 'python3.5 remove_bookmark.py'
    rmbkmrk = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    speechRecognitionThread.stop_sr()


def find_dictate_wikipedia_transcript_function():
    global speechRecognitionThread
    stop_transcription_function()
    cmd = 'python3.5 transcriptor_wikipedia.py'
    print('running command:', cmd)
    stprocess = subprocess.Popen(cmd,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    speechRecognitionThread.stop_sr()


def find_dictate_any_transcript_function():
    global speechRecognitionThread
    stop_transcription_function()
    cmd = 'python3.5 dictator_local_transcript.py'
    print('running command:', cmd)
    atprocess = subprocess.Popen(cmd,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    speechRecognitionThread.stop_sr()


def list_transcripts_function():
    global speechRecognitionThread
    stop_transcription_function()
    cmd = 'python3.5 dictator_list_transcripts.py'
    print('running command:', cmd)
    ltprocess = subprocess.Popen(cmd,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    speechRecognitionThread.stop_sr()


def get_latest_transcript_function():
    global speechRecognitionThread
    stop_transcription_function()
    cmd = 'python3.5 dictator_latest_transcript.py'
    print('running command:', cmd)
    gltprocess = subprocess.Popen(cmd,
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    speechRecognitionThread.stop_sr()


def wiktionary_define_function():
    global speechRecognitionThread
    stop_transcription_function()
    cmd = 'python3.5 transcriptor_wiktionary_define.py'
    print('running command:', cmd)
    defineprocess = subprocess.Popen(cmd,
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    speechRecognitionThread.stop_sr()


def find_open_audio_function():
    findOpenAudioThread.start()


def open_directory_function():
    openDirectoryThread.start()


def find_open_image_function():
    findOpenImageThread.start()


def find_open_text_function():
    findOpenTextThread.start()


def find_open_video_function():
    findOpenVideoThread.start()


def find_open_program_function():
    findOpenProgramThread.start()


def stop_transcription_function():
    global primary_key
    global speechRecognitionThread

    try:
        print('killing transcription process')
        dictate = 'False'
        line_list = []
        with codecs.open('./configuration/system_config.conf', 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('DICTATE_TRANSCRIPT: '):
                line_list[i] = str('DICTATE_TRANSCRIPT: ' + dictate + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open('./configuration/system_config.conf', 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i += 1
        fo.close()
        print('updated: system_config.conf')
        cmd = 'killall mpg321'
        xcmd = subprocess.Popen(cmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        xcmd.wait()
        primary_key = primary_key.strip()
        if 'stop transcription' == primary_key:
            speechRecognitionThread.stop_sr()
    except:
        pass


internal_commands_list = {'stop transcription': stop_transcription_function,
                          'search Wikipedia': find_dictate_wikipedia_transcript_function,
                          'transcripts available for': list_transcripts_function,
                          'latest transcript for': get_latest_transcript_function,
                          'define': wiktionary_define_function,
                          'play audio': find_open_audio_function,
                          'directory': open_directory_function,
                          'open image': find_open_image_function,
                          'open text': find_open_text_function,
                          'play video': find_open_video_function,
                          'run program': find_open_program_function,
                          'transcription': find_dictate_any_transcript_function,
                          'remove bookmark': remove_bookmark_function,
                          }

key_word = ['stop transcription',
            'search Wikipedia',
            'transcripts available for',
            'latest transcript for',
            'define',
            'play audio',
            'directory',
            'open image',
            'open text',
            'play video',
            'run program',
            'transcription',
            'remove bookmark',
            ]


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.index_text_editable = False
        self.index_image_editable = False
        self.index_video_editable = False
        self.index_audio_editable = False
        self.index_drive1_editable = False
        self.index_drive2_editable = False
        self.index_drive3_editable = False
        self.index_drive4_editable = False
        self.index_drive5_editable = False
        self.index_drive6_editable = False
        self.index_drive7_editable = False
        self.index_drive8_editable = False
        self.symbiot_server_ip_editable = False
        self.symbiot_server_port_editable = False
        self.symbiot_ip_editable = False
        self.symbiot_mac_editable = False
        self.wikiServer_ip_editable = False
        self.wiki_server_port_editable = False
        self.title = "Information & Control System'"
        self.left = 570
        self.top = 0
        self.width = 780
        self.height = 185
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.init_ui()

    def init_ui(self):

        global value
        global secondary_key
        global findOpenAudioThread
        global speechRecognitionThread
        global guiControllerThread
        global drawMenuThread
        global openDirectoryThread
        global findOpenImageThread
        global findOpenTextThread
        global findOpenVideoThread
        global findOpenProgramThread
        global configInteractionPermissionThread
        global symbiotServerThread
        global symbiot_configuration_bool
        global wiki_local_server_ip_configuration_bool
        global wiki_local_server_port_configuration_bool

        self.setWindowTitle('Information & Control System')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("./resources/image/main_icon.ico"))

        logo_label = QLabel(self)
        logo_label.move(20, 4)
        logo_label.resize(40, 40)
        pixmap = QPixmap("./resources/image/main_icon.ico")
        logo_label.setPixmap(pixmap)

        dynamic_logo_label = QLabel(self)
        dynamic_logo_label.move(20, 4)
        dynamic_logo_label.resize(40, 40)
        pixmap = QPixmap("./resources/image/main_icon_dynamic.png")
        dynamic_logo_label.setPixmap(pixmap)
        dynamic_logo_label.hide()

        incremental_resize_button = QPushButton(self)
        incremental_resize_button.move(740, 25)
        incremental_resize_button.resize(20, 20)
        incremental_resize_button.clicked.connect(self.incremental_resize_function)
        incremental_resize_button.setIcon(QIcon("./resources/image/main_menu.png"))
        incremental_resize_button.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
           border:1px solid rgb(0, 0, 0);}"""
        )

        def speech_recognition_on_function():
            speechRecognitionThread.start()
            print('speech recognition: on')

        def speech_recognition_off_function():
            speechRecognitionThread.stop_sr()
            gui_controller_off_function()
            print('speech recognition: off')

        def gui_controller_off_function():
            guiControllerThread.stop_gui_controller()
            print('guiController: off')

        def symbiot_enable_disable_function():
            global symbiot_configuration_bool
            if symbiot_configuration_bool == False:
                print('enabling symbiot server')
                symbiotServerThread.start()
                symbiot_configuration_bool = True
                symbiot_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                    color: rgb(100, 255, 0);
                    border:1px solid rgb(0, 0, 0);}"""
                )
            elif symbiot_configuration_bool == True:
                print('disabling symbiot server')
                symbiotServerThread.symbiot_server_off()
                symbiot_configuration_bool = False
                symbiot_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                    color: rgb(255, 0, 0);
                    border:1px solid rgb(0, 0, 0);}"""
                )

        symbiot_button = QPushButton(self)
        symbiot_button.move(680, 50)
        symbiot_button.resize(60, 15)
        symbiot_button.clicked.connect(symbiot_enable_disable_function)
        symbiot_button.setText("Symbiot")
        if symbiot_configuration_bool == True:
            symbiot_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: rgb(100, 255, 0);
               border:1px solid rgb(0, 0, 0);}"""
            )
            symbiot_configuration_bool = False
        elif symbiot_configuration_bool == False:
            symbiot_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: rgb(255, 0, 0);
               border:1px solid rgb(0, 0, 0);}"""
            )

        sr_on_button = QPushButton(self)
        sr_on_button.move(40, 50)
        sr_on_button.resize(40, 15)
        sr_on_button.clicked.connect(speech_recognition_on_function)
        sr_on_button.setText("ON")
        sr_on_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: rgb(0, 150, 0);
           border:1px solid rgb(0, 0, 0);}"""
        )

        sr_off_button = QPushButton(self)
        sr_off_button.move(80, 50)
        sr_off_button.resize(40, 15)
        sr_off_button.clicked.connect(speech_recognition_off_function)
        sr_off_button.setText("OFF")
        sr_off_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: rgb(255, 0, 0);
           border:1px solid rgb(0, 0, 0);}"""
        )

        sr_indicator = QLabel(self)
        sr_indicator.move(20, 48)
        sr_indicator.resize(20, 20)
        pixmap = QPixmap('./resources/image/speech_recognition_led_off.png')
        sr_indicator.setPixmap(pixmap)

        sr_info = QLineEdit(self)
        sr_info.move(40, 65)
        sr_info.resize(700, 20)
        sr_info.setReadOnly(True)
        sr_info.setStyleSheet(
            """QLineEdit {background-color: black;
            border: false;
            selection-color: black;
            selection-background-color: black;
            color: rgb(115, 255, 0);}"""
        )

        text_box_value = QLineEdit(self)
        text_box_value.move(40, 85)
        text_box_value.resize(700, 20)
        text_box_value.setReadOnly(True)
        text_box_value.setStyleSheet(
            """QLineEdit {background-color: black;
            border: false;
            selection-color: black;
            selection-background-color: black;
            color: #00FF00;}"""
        )

        text_box_verbose1 = QLineEdit(self)
        text_box_verbose1.move(40, 105)
        text_box_verbose1.resize(700, 20)
        text_box_verbose1.setReadOnly(True)
        text_box_verbose1.setStyleSheet(
            """QLineEdit {background-color: black;
            border: false;
            selection-color: black;
            selection-background-color: black;
            color: #00FF00;}"""
        )

        text_box_verbose2 = QLineEdit(self)
        text_box_verbose2.move(40, 125)
        text_box_verbose2.resize(700, 20)
        text_box_verbose2.setReadOnly(True)
        text_box_verbose2.setStyleSheet(
            """QLineEdit {background-color: black;
            border: false;
            selection-color: black;
            selection-background-color: black;
            color: #00FF00;}"""
        )

        def config_interaction_permission_function():
            configInteractionPermissionThread.start()
        settings_title = QLabel(self)
        settings_title.move(285, 180)
        settings_title.resize(150, 20)
        f = settings_title.font()
        f.setPointSize(8)
        settings_title.setFont(f)

        settings_title.setText('   File Access Configuration')
        settings_title.setStyleSheet(
            """QLabel {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )

        index_title1 = QLabel(self)
        index_title1.move(130, 180)
        index_title1.resize(110, 20)
        f = index_title1.font()
        f.setPointSize(8)
        index_title1.setFont(f)
        index_title1.setText('User Access Settings')
        index_title1.setStyleSheet(
            """QLabel {
           color: white;
           border: false;}"""
        )

        index_title2 = QLabel(self)
        index_title2.move(520, 180)
        index_title2.resize(150, 20)
        f = index_title2.font()
        f.setPointSize(8)
        index_title2.setFont(f)
        index_title2.setText('Advanced Access Settings')
        index_title2.setStyleSheet(
            """QLabel {
           color: white;
           border: false;}"""
        )

        wiki_settings_label = QLabel(self)
        wiki_settings_label.move(390, 300)
        wiki_settings_label.resize(120, 20)
        f = wiki_settings_label.font()
        f.setPointSize(8)
        wiki_settings_label.setFont(f)
        wiki_settings_label.setText('Information Settings')
        wiki_settings_label.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )

        wiki_show_browser_label = QLabel(self)
        wiki_show_browser_label.move(375, 330)
        wiki_show_browser_label.resize(135, 20)
        f = wiki_show_browser_label.font()
        f.setPointSize(8)
        wiki_show_browser_label.setFont(f)
        wiki_show_browser_label.setText('Wikipedia in Browser?')
        wiki_show_browser_label.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )

        self.wiki_show_browser_button = QPushButton(self)
        self.wiki_show_browser_button.move(510, 330)
        self.wiki_show_browser_button.resize(50, 20)
        f = self.wiki_show_browser_button.font()
        f.setPointSize(8)
        self.wiki_show_browser_button.setFont(f)
        if wiki_show_browser_bool == False:
            self.wiki_show_browser_button.setText('Disabled')
            self.wiki_show_browser_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif wiki_show_browser_bool == True:
            self.wiki_show_browser_button.setText('Enabled')
            self.wiki_show_browser_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
        self.wiki_show_browser_button.clicked.connect(self.wiki_show_browser_function)

        dictate_wiki_label = QLabel(self)
        dictate_wiki_label.move(375, 350)
        dictate_wiki_label.resize(135, 20)
        f = dictate_wiki_label.font()
        f.setPointSize(8)
        dictate_wiki_label.setFont(f)
        dictate_wiki_label.setText('Dictate Wiki Transcripts?')
        dictate_wiki_label.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )

        self.dictate_wiki_button = QPushButton(self)
        self.dictate_wiki_button.move(510, 350)
        self.dictate_wiki_button.resize(50, 20)
        f = self.dictate_wiki_button.font()
        f.setPointSize(8)
        self.dictate_wiki_button.setFont(f)
        if wiki_dictate_bool == False:
            self.dictate_wiki_button.setText('Disabled')
            self.dictate_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif wiki_dictate_bool == True:
            self.dictate_wiki_button.setText('Enabled')
            self.dictate_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
        self.dictate_wiki_button.clicked.connect(self.dictate_wiki_function)

        use_local_wiki_label = QLabel(self)
        use_local_wiki_label.move(375, 370)
        use_local_wiki_label.resize(135, 20)
        f = use_local_wiki_label.font()
        f.setPointSize(8)
        use_local_wiki_label.setFont(f)
        use_local_wiki_label.setText('Use Local Wiki Server?')
        use_local_wiki_label.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )

        self.use_local_wiki_button = QPushButton(self)
        self.use_local_wiki_button.move(510, 370)
        self.use_local_wiki_button.resize(50, 20)
        f = self.use_local_wiki_button.font()
        f.setPointSize(8)
        self.use_local_wiki_button.setFont(f)
        if allow_wiki_local_server_bool == False:
            self.use_local_wiki_button.setText('Disabled')
            self.use_local_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif allow_wiki_local_server_bool == True:
            self.use_local_wiki_button.setText('Enabled')
            self.use_local_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
        self.use_local_wiki_button.clicked.connect(self.use_local_wiki_function)

        wiki_server_ip_button = QPushButton(self)
        wiki_server_ip_button.move(570, 330)
        wiki_server_ip_button.resize(75, 20)
        f = wiki_server_ip_button.font()
        f.setPointSize(8)
        wiki_server_ip_button.setFont(f)
        wiki_server_ip_button.setText('Wiki Server')
        wiki_server_ip_button.clicked.connect(self.wiki_server_ip_function)
        wiki_server_ip_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )

        self.wiki_server_ip_edit = QLineEdit(self)
        self.wiki_server_ip_edit.move(640, 330)
        self.wiki_server_ip_edit.resize(110, 20)
        f = self.wiki_server_ip_edit.font()
        f.setPointSize(8)
        self.wiki_server_ip_edit.setFont(f)
        self.wiki_server_ip_edit.setReadOnly(True)
        self.wiki_server_ip_edit.setText(wiki_local_server_ip_configuration)
        self.wiki_server_ip_edit.returnPressed.connect(self.write_wiki_server_function)
        self.wiki_server_ip_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        wiki_server_port_button = QPushButton(self)
        wiki_server_port_button.move(570, 355)
        wiki_server_port_button.resize(125, 20)
        f = wiki_server_port_button.font()
        f.setPointSize(8)
        wiki_server_port_button.setFont(f)
        wiki_server_port_button.setText('Wiki Server Port')
        wiki_server_port_button.clicked.connect(self.wiki_server_port_function)
        wiki_server_port_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )

        self.wiki_server_port_edit = QLineEdit(self)
        self.wiki_server_port_edit.move(695, 355)
        self.wiki_server_port_edit.resize(55, 20)
        f = self.wiki_server_port_edit.font()
        f.setPointSize(8)
        self.wiki_server_port_edit.setFont(f)
        self.wiki_server_port_edit.setReadOnly(True)
        self.wiki_server_port_edit.setText(wiki_local_server_port_configuration)
        self.wiki_server_port_edit.returnPressed.connect(self.write_wiki_server_port_function)
        self.wiki_server_port_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        symbiot_title = QLabel(self)
        symbiot_title.move(40, 300)
        symbiot_title.resize(100, 20)
        f = symbiot_title.font()
        f.setPointSize(8)
        symbiot_title.setFont(f)
        symbiot_title.setText('Symbiot Settings')
        symbiot_title.setStyleSheet(
            """QLabel {
           color: yellow;
           border: false;}"""
        )

        symbiot_server_ip_button = QPushButton(self)
        symbiot_server_ip_button.move(30, 330)
        symbiot_server_ip_button.resize(80, 20)
        f = symbiot_server_ip_button.font()
        f.setPointSize(8)
        symbiot_server_ip_button.setFont(f)
        symbiot_server_ip_button.setText('Server IP')
        symbiot_server_ip_button.clicked.connect(self.symbiot_server_ip_function)
        symbiot_server_ip_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )

        self.symbiot_server_ip_edit = QLineEdit(self)
        self.symbiot_server_ip_edit.move(110, 330)
        self.symbiot_server_ip_edit.resize(230, 20)
        f = self.symbiot_server_ip_edit.font()
        f.setPointSize(8)
        self.symbiot_server_ip_edit.setFont(f)
        self.symbiot_server_ip_edit.setReadOnly(True)
        self.symbiot_server_ip_edit.setText(symbiot_server_ip_configuration)
        self.symbiot_server_ip_edit.returnPressed.connect(self.write_symbiot_server_ip_function)
        self.symbiot_server_ip_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        symbiot_server_port_button = QPushButton(self)
        symbiot_server_port_button.move(30, 350)
        symbiot_server_port_button.resize(80, 20)
        f = symbiot_server_port_button.font()
        f.setPointSize(8)
        symbiot_server_port_button.setFont(f)
        symbiot_server_port_button.setText('Server Port')
        symbiot_server_port_button.clicked.connect(self.symbiot_server_port_function)
        symbiot_server_port_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )

        self.symbiot_server_port_edit = QLineEdit(self)
        self.symbiot_server_port_edit.move(110, 350)
        self.symbiot_server_port_edit.resize(230, 20)
        f = self.symbiot_server_port_edit.font()
        f.setPointSize(8)
        self.symbiot_server_port_edit.setFont(f)
        self.symbiot_server_port_edit.setReadOnly(True)
        self.symbiot_server_port_edit.setText(symbiot_server_port_configuration)
        self.symbiot_server_port_edit.returnPressed.connect(self.write_symbiot_server_port_function)
        self.symbiot_server_port_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        symbiot_ip_button = QPushButton(self)
        symbiot_ip_button.move(30, 370)
        symbiot_ip_button.resize(80, 20)
        f = symbiot_ip_button.font()
        f.setPointSize(8)
        symbiot_ip_button.setFont(f)
        symbiot_ip_button.setText('Symbiot IP')
        symbiot_ip_button.clicked.connect(self.symbiot_ip_function)
        symbiot_ip_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )

        self.symbiot_ip_edit = QLineEdit(self)
        self.symbiot_ip_edit.move(110, 370)
        self.symbiot_ip_edit.resize(230, 20)
        f = self.symbiot_ip_edit.font()
        f.setPointSize(8)
        self.symbiot_ip_edit.setFont(f)
        self.symbiot_ip_edit.setReadOnly(True)
        self.symbiot_ip_edit.setText(symbiot_ip_configuration)
        self.symbiot_ip_edit.returnPressed.connect(self.write_symbiot_ip_function)
        self.symbiot_ip_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        symbiot_mac_button = QPushButton(self)
        symbiot_mac_button.move(30, 390)
        symbiot_mac_button.resize(80, 20)
        f = symbiot_mac_button.font()
        f.setPointSize(8)
        symbiot_mac_button.setFont(f)
        symbiot_mac_button.setText('Symbiot MAC')
        symbiot_mac_button.clicked.connect(self.symbiot_mac_function)
        symbiot_mac_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )

        self.symbiot_mac_edit = QLineEdit(self)
        self.symbiot_mac_edit.move(110, 390)
        self.symbiot_mac_edit.resize(230, 20)
        f = self.symbiot_mac_edit.font()
        f.setPointSize(8)
        self.symbiot_mac_edit.setFont(f)
        self.symbiot_mac_edit.setReadOnly(True)
        self.symbiot_mac_edit.setText(symbiot_mac_configuration)
        self.symbiot_mac_edit.returnPressed.connect(self.write_symbiot_mac_function)
        self.symbiot_mac_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )

        index_audio_button = QPushButton(self)
        index_audio_button.move(30, 215)
        index_audio_button.resize(45, 20)
        f = index_audio_button.font()
        f.setPointSize(8)
        index_audio_button.setFont(f)
        index_audio_button.setText(' Audio')
        index_audio_button.clicked.connect(self.index_audio_configuration_function)
        index_audio_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.index_audio_edit = QLineEdit(self)
        self.index_audio_edit.move(75, 215)
        self.index_audio_edit.resize(230, 20)
        f = self.index_audio_edit.font()
        f.setPointSize(8)
        self.index_audio_edit.setFont(f)
        self.index_audio_edit.setReadOnly(True)
        self.index_audio_edit.setText(audio_configuration.replace('DIRAUD: ', ''))
        self.index_audio_edit.returnPressed.connect(self.write_audio_path_function)
        self.index_audio_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.index_audio_enable_disable_button = QPushButton(self)
        self.index_audio_enable_disable_button.move(305, 215)
        self.index_audio_enable_disable_button.resize(45, 20)
        f = self.index_audio_enable_disable_button.font()
        f.setPointSize(8)
        self.index_audio_enable_disable_button.setFont(f)
        self.index_audio_enable_disable_button.setText(audio_active_config)
        self.index_audio_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.index_audio_enable_disable_button.clicked.connect(self.audio_index_enable_disable_function)
        if audio_active_config_bool == False:
            self.index_audio_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif audio_active_config_bool == True:
            self.index_audio_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        index_video_button = QPushButton(self)
        index_video_button.move(30, 230)
        index_video_button.resize(45, 20)
        f = index_video_button.font()
        f.setPointSize(8)
        index_video_button.setFont(f)
        index_video_button.setText(' Video')
        index_video_button.clicked.connect(self.index_video_configuration_function)
        index_video_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.index_video_edit = QLineEdit(self)
        self.index_video_edit.move(75, 230)
        self.index_video_edit.resize(230, 20)
        f = self.index_video_edit.font()
        f.setPointSize(8)
        self.index_video_edit.setFont(f)
        self.index_video_edit.setReadOnly(True)
        self.index_video_edit.setText(video_configuration.replace('DIRVID: ', ''))
        self.index_video_edit.returnPressed.connect(self.write_video_path_function)
        self.index_video_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.index_video_enable_disable_button = QPushButton(self)
        self.index_video_enable_disable_button.move(305, 230)
        self.index_video_enable_disable_button.resize(45, 20)
        f = self.index_video_enable_disable_button.font()
        f.setPointSize(8)
        self.index_video_enable_disable_button.setFont(f)
        self.index_video_enable_disable_button.setText(video_active_config)
        self.index_video_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.index_video_enable_disable_button.clicked.connect(self.video_index_enable_disable_function)
        if video_active_config_bool == False:
            self.index_video_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif video_active_config_bool == True:
            self.index_video_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        index_images_button = QPushButton(self)
        index_images_button.move(30, 245)
        index_images_button.resize(45, 20)
        f = index_images_button.font()
        f.setPointSize(8)
        index_images_button.setFont(f)
        index_images_button.setText(' Images')
        index_images_button.clicked.connect(self.index_images_configuration_function)
        index_images_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.index_images_edit = QLineEdit(self)
        self.index_images_edit.move(75, 245)
        self.index_images_edit.resize(230, 20)
        f = self.index_images_edit.font()
        f.setPointSize(8)
        self.index_images_edit.setFont(f)
        self.index_images_edit.setReadOnly(True)
        self.index_images_edit.setText(image_configuration.replace('DIRIMG: ', ''))
        self.index_images_edit.returnPressed.connect(self.write_images_path_function)
        self.index_images_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.index_image_enable_disable_button = QPushButton(self)
        self.index_image_enable_disable_button.move(305, 245)
        self.index_image_enable_disable_button.resize(45, 20)
        f = self.index_image_enable_disable_button.font()
        f.setPointSize(8)
        self.index_image_enable_disable_button.setFont(f)
        self.index_image_enable_disable_button.setText(image_active_config)
        self.index_image_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.index_image_enable_disable_button.clicked.connect(self.image_index_enable_disable_function)
        if image_active_config_bool == False:
            self.index_image_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif image_active_config_bool == True:
            self.index_image_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        index_text_button = QPushButton(self)
        index_text_button.move(30, 260)
        index_text_button.resize(45, 20)
        f = index_text_button.font()
        f.setPointSize(8)
        index_text_button.setFont(f)
        index_text_button.setText('Text')
        index_text_button.clicked.connect(self.index_text_configuration_function)
        index_text_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.index_text_edit = QLineEdit(self)
        self.index_text_edit.move(75, 260)
        self.index_text_edit.resize(230, 20)
        f = self.index_text_edit.font()
        f.setPointSize(8)
        self.index_text_edit.setFont(f)
        self.index_text_edit.setReadOnly(True)
        self.index_text_edit.setText(text_configuration.replace('DIRTXT: ', ''))
        self.index_text_edit.returnPressed.connect(self.write_text_path_function)
        self.index_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.index_text_enable_disable_button = QPushButton(self)
        self.index_text_enable_disable_button.move(305, 260)
        self.index_text_enable_disable_button.resize(45, 20)
        f = self.index_text_enable_disable_button.font()
        f.setPointSize(8)
        self.index_text_enable_disable_button.setFont(f)
        self.index_text_enable_disable_button.setText(text_active_config)
        self.index_text_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.index_text_enable_disable_button.clicked.connect(self.text_index_enable_disable_function)
        if text_active_config_bool == False:
            self.index_text_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif text_active_config_bool == True:
            self.index_text_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive1_button = QPushButton(self)
        drive1_button.move(370, 215)
        drive1_button.resize(45, 20)
        f = drive1_button.font()
        f.setPointSize(8)
        drive1_button.setFont(f)
        drive1_button.setText(' 1')
        drive1_button.clicked.connect(self.index_drive1_configuration_function)
        drive1_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive1_text_edit = QLineEdit(self)
        self.drive1_text_edit.move(415, 215)
        self.drive1_text_edit.resize(100, 20)
        f = self.drive1_text_edit.font()
        f.setPointSize(8)
        self.drive1_text_edit.setFont(f)
        self.drive1_text_edit.setReadOnly(True)
        self.drive1_text_edit.setText(drive1_configuration.replace('DRIVE1: ', ''))
        self.drive1_text_edit.returnPressed.connect(self.write_drive1_path_function)
        self.drive1_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive1_enable_disable_button = QPushButton(self)
        self.drive1_enable_disable_button.move(515, 215)
        self.drive1_enable_disable_button.resize(45, 20)
        f = self.drive1_enable_disable_button.font()
        f.setPointSize(8)
        self.drive1_enable_disable_button.setFont(f)
        self.drive1_enable_disable_button.setText(drive_1_active_config)
        self.drive1_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive1_enable_disable_button.clicked.connect(self.drive1_enable_disable_function)
        if drive_1_active_config_bool == False:
            self.drive1_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_1_active_config_bool == True:
            self.drive1_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive2_button = QPushButton(self)
        drive2_button.move(370, 230)
        drive2_button.resize(45, 20)
        f = drive2_button.font()
        f.setPointSize(8)
        drive2_button.setFont(f)
        drive2_button.setText(' 2')
        drive2_button.clicked.connect(self.index_drive2_configuration_function)
        drive2_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive2_text_edit = QLineEdit(self)
        self.drive2_text_edit.move(415, 230)
        self.drive2_text_edit.resize(100, 20)
        f = self.drive2_text_edit.font()
        f.setPointSize(8)
        self.drive2_text_edit.setFont(f)
        self.drive2_text_edit.setReadOnly(True)
        self.drive2_text_edit.setText(drive2_configuration.replace('DRIVE2: ', ''))
        self.drive2_text_edit.returnPressed.connect(self.write_drive2_path_function)
        self.drive2_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive2_enable_disable_button = QPushButton(self)
        self.drive2_enable_disable_button.move(515, 230)
        self.drive2_enable_disable_button.resize(45, 20)
        f = self.drive2_enable_disable_button.font()
        f.setPointSize(8)
        self.drive2_enable_disable_button.setFont(f)
        self.drive2_enable_disable_button.setText(drive_2_active_config)
        self.drive2_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive2_enable_disable_button.clicked.connect(self.drive2_enable_disable_function)
        if drive_2_active_config_bool == False:
            self.drive2_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_2_active_config_bool == True:
            self.drive2_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive3_button = QPushButton(self)
        drive3_button.move(370, 245)
        drive3_button.resize(45, 20)
        f = drive3_button.font()
        f.setPointSize(8)
        drive3_button.setFont(f)
        drive3_button.setText(' 3')
        drive3_button.clicked.connect(self.index_drive3_configuration_function)
        drive3_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive3_text_edit = QLineEdit(self)
        self.drive3_text_edit.move(415, 245)
        self.drive3_text_edit.resize(100, 20)
        f = self.drive3_text_edit.font()
        f.setPointSize(8)
        self.drive3_text_edit.setFont(f)
        self.drive3_text_edit.setReadOnly(True)
        self.drive3_text_edit.setText(drive3_configuration.replace('DRIVE3: ', ''))
        self.drive3_text_edit.returnPressed.connect(self.write_drive3_path_function)
        self.drive3_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive3_enable_disable_button = QPushButton(self)
        self.drive3_enable_disable_button.move(515, 245)
        self.drive3_enable_disable_button.resize(45, 20)
        f = self.drive3_enable_disable_button.font()
        f.setPointSize(8)
        self.drive3_enable_disable_button.setFont(f)
        self.drive3_enable_disable_button.setText(drive_3_active_config)
        self.drive3_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive3_enable_disable_button.clicked.connect(self.drive3_enable_disable_function)
        if drive_3_active_config_bool == False:
            self.drive3_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_3_active_config_bool == True:
            self.drive3_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive4_button = QPushButton(self)
        drive4_button.move(370, 260)
        drive4_button.resize(45, 20)
        f = drive4_button.font()
        f.setPointSize(8)
        drive4_button.setFont(f)
        drive4_button.setText(' 4')
        drive4_button.clicked.connect(self.index_drive4_configuration_function)
        drive4_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive4_text_edit = QLineEdit(self)
        self.drive4_text_edit.move(415, 260)
        self.drive4_text_edit.resize(100, 20)
        f = self.drive4_text_edit.font()
        f.setPointSize(8)
        self.drive4_text_edit.setFont(f)
        self.drive4_text_edit.setReadOnly(True)
        self.drive4_text_edit.setText(drive4_configuration.replace('DRIVE4: ', ''))
        self.drive4_text_edit.returnPressed.connect(self.write_drive4_path_function)
        self.drive4_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive4_enable_disable_button = QPushButton(self)
        self.drive4_enable_disable_button.move(515, 260)
        self.drive4_enable_disable_button.resize(45, 20)
        f = self.drive4_enable_disable_button.font()
        f.setPointSize(8)
        self.drive4_enable_disable_button.setFont(f)
        self.drive4_enable_disable_button.setText(drive_4_active_config)
        self.drive4_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive4_enable_disable_button.clicked.connect(self.drive4_enable_disable_function)
        if drive_4_active_config_bool == False:
            self.drive4_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_4_active_config_bool == True:
            self.drive4_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive5_button = QPushButton(self)
        drive5_button.move(565, 215)
        drive5_button.resize(45, 20)
        f = drive5_button.font()
        f.setPointSize(8)
        drive5_button.setFont(f)
        drive5_button.setText(' 5')
        drive5_button.clicked.connect(self.index_drive5_configuration_function)
        drive5_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive5_text_edit = QLineEdit(self)
        self.drive5_text_edit.move(610, 215)
        self.drive5_text_edit.resize(100, 20)
        f = self.drive5_text_edit.font()
        f.setPointSize(8)
        self.drive5_text_edit.setFont(f)
        self.drive5_text_edit.setReadOnly(True)
        self.drive5_text_edit.setText(drive5_configuration.replace('DRIVE5: ', ''))
        self.drive5_text_edit.returnPressed.connect(self.write_drive5_path_function)
        self.drive5_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive5_enable_disable_button = QPushButton(self)
        self.drive5_enable_disable_button.move(710, 215)
        self.drive5_enable_disable_button.resize(45, 20)
        f = self.drive5_enable_disable_button.font()
        f.setPointSize(8)
        self.drive5_enable_disable_button.setFont(f)
        self.drive5_enable_disable_button.setText(drive_5_active_config)
        self.drive5_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive5_enable_disable_button.clicked.connect(self.drive5_enable_disable_function)
        if drive_5_active_config_bool == False:
            self.drive5_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_5_active_config_bool == True:
            self.drive5_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive6_button = QPushButton(self)
        drive6_button.move(565, 230)
        drive6_button.resize(45, 20)
        f = drive6_button.font()
        f.setPointSize(8)
        drive6_button.setFont(f)
        drive6_button.setText(' 6')
        drive6_button.clicked.connect(self.index_drive6_configuration_function)
        drive6_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive6_text_edit = QLineEdit(self)
        self.drive6_text_edit.move(610, 230)
        self.drive6_text_edit.resize(100, 20)
        f = self.drive6_text_edit.font()
        f.setPointSize(8)
        self.drive6_text_edit.setFont(f)
        self.drive6_text_edit.setReadOnly(True)
        self.drive6_text_edit.setText(drive6_configuration.replace('DRIVE6: ', ''))
        self.drive6_text_edit.returnPressed.connect(self.write_drive6_path_function)
        self.drive6_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive6_enable_disable_button = QPushButton(self)
        self.drive6_enable_disable_button.move(710, 230)
        self.drive6_enable_disable_button.resize(45, 20)
        f = self.drive6_enable_disable_button.font()
        f.setPointSize(8)
        self.drive6_enable_disable_button.setFont(f)
        self.drive6_enable_disable_button.setText(drive_6_active_config)
        self.drive6_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive6_enable_disable_button.clicked.connect(self.drive6_enable_disable_function)
        if drive_6_active_config_bool == False:
            self.drive6_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_6_active_config_bool == True:
            self.drive6_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive7_button = QPushButton(self)
        drive7_button.move(565, 245)
        drive7_button.resize(45, 20)
        f = drive7_button.font()
        f.setPointSize(8)
        drive7_button.setFont(f)
        drive7_button.setText(' 7')
        drive7_button.clicked.connect(self.index_drive7_configuration_function)
        drive7_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive7_text_edit = QLineEdit(self)
        self.drive7_text_edit.move(610, 245)
        self.drive7_text_edit.resize(100, 20)
        f = self.drive7_text_edit.font()
        f.setPointSize(8)
        self.drive7_text_edit.setFont(f)
        self.drive7_text_edit.setReadOnly(True)
        self.drive7_text_edit.setText(drive7_configuration.replace('DRIVE7: ', ''))
        self.drive7_text_edit.returnPressed.connect(self.write_drive7_path_function)
        self.drive7_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive7_enable_disable_button = QPushButton(self)
        self.drive7_enable_disable_button.move(710, 245)
        self.drive7_enable_disable_button.resize(45, 20)
        f = self.drive7_enable_disable_button.font()
        f.setPointSize(8)
        self.drive7_enable_disable_button.setFont(f)
        self.drive7_enable_disable_button.setText(drive_7_active_config)
        self.drive7_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive7_enable_disable_button.clicked.connect(self.drive7_enable_disable_function)
        if drive_7_active_config_bool == False:
            self.drive7_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_7_active_config_bool == True:
            self.drive7_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        drive8_button = QPushButton(self)
        drive8_button.move(565, 260)
        drive8_button.resize(45, 20)
        f = drive8_button.font()
        f.setPointSize(8)
        drive8_button.setFont(f)
        drive8_button.setText(' 8')
        drive8_button.clicked.connect(self.index_drive8_configuration_function)
        drive8_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
           color: yellow;
           border: false;}"""
        )
        self.drive8_text_edit = QLineEdit(self)
        self.drive8_text_edit.move(610, 260)
        self.drive8_text_edit.resize(100, 20)
        f = self.drive8_text_edit.font()
        f.setPointSize(8)
        self.drive8_text_edit.setFont(f)
        self.drive8_text_edit.setReadOnly(True)
        self.drive8_text_edit.setText(drive8_configuration.replace('DRIVE8: ', ''))
        self.drive8_text_edit.returnPressed.connect(self.write_drive8_path_function)
        self.drive8_text_edit.setStyleSheet(
            """QLineEdit {background-color: rgb(15, 14, 15);
            border:5px solid rgb(0, 0, 0);
            selection-color: black;
            selection-background-color: black;
            color: grey;}"""
        )
        self.drive8_enable_disable_button = QPushButton(self)
        self.drive8_enable_disable_button.move(710, 260)
        self.drive8_enable_disable_button.resize(45, 20)
        f = self.drive8_enable_disable_button.font()
        f.setPointSize(8)
        self.drive8_enable_disable_button.setFont(f)
        self.drive8_enable_disable_button.setText(drive_8_active_config)
        self.drive8_enable_disable_button.clicked.connect(config_interaction_permission_function)
        self.drive8_enable_disable_button.clicked.connect(self.drive8_enable_disable_function)
        if drive_8_active_config_bool == False:
            self.drive8_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
        elif drive_8_active_config_bool == True:
            self.drive8_enable_disable_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )

        findOpenImageThread = FindOpenImageClass()
        findOpenTextThread = FindOpenTextClass()
        findOpenVideoThread = FindOpenVideoClass()
        findOpenProgramThread = FindOpenProgramClass()

        textBoxVerbose2Thread = TextBoxVerbose2Class(text_box_verbose2)
        symbiotServerThread = SymbiotServerClass(speechRecognitionThread,
                                                 symbiot_button,
                                                 speech_recognition_off_function)
        openDirectoryThread = OpenDirectoryClass(text_box_verbose1,
                                                 text_box_verbose2)
        guiControllerThread = GuiControllerClass(sr_info,
                                                 text_box_value,
                                                 text_box_verbose1,
                                                 text_box_verbose2)
        findOpenAudioThread = FindOpenAudioClass(text_box_verbose1)
        commandSearchThread = CommandSearchClass(text_box_verbose1,
                                                 text_box_verbose2,
                                                 textBoxVerbose2Thread)
        speechRecognitionThread = SpeechRecognitionClass(sr_indicator,
                                                         text_box_value,
                                                         text_box_verbose1,
                                                         text_box_verbose2,
                                                         textBoxVerbose2Thread,
                                                         sr_info,
                                                         guiControllerThread,
                                                         commandSearchThread,
                                                         sr_on_button,
                                                         sr_off_button,
                                                         logo_label,
                                                         dynamic_logo_label)
        configInteractionPermissionThread = ConfigInteractionPermissionClass(self.index_audio_enable_disable_button,
                                                                             self.index_video_enable_disable_button,
                                                                             self.index_image_enable_disable_button,
                                                                             self.index_text_enable_disable_button,
                                                                             self.index_audio_edit,
                                                                             self.index_video_edit,
                                                                             self.index_images_edit,
                                                                             self.index_text_edit,
                                                                             index_audio_button,
                                                                             index_video_button,
                                                                             index_images_button,
                                                                             index_text_button,
                                                                             self.drive1_enable_disable_button,
                                                                             self.drive2_enable_disable_button,
                                                                             self.drive3_enable_disable_button,
                                                                             self.drive4_enable_disable_button,
                                                                             self.drive1_text_edit,
                                                                             self.drive2_text_edit,
                                                                             self.drive3_text_edit,
                                                                             self.drive4_text_edit,
                                                                             drive1_button,
                                                                             drive2_button,
                                                                             drive3_button,
                                                                             drive4_button)
        self.show()

    # CloseEvent
    def closeEvent(self, event):
        global auto_crawler_pid
        global auto_crawler_xcmd
        try:
            print('attempting to turn off speech recognition')
            speechRecognitionThread.stop_sr()
            print('speech recognition de-activated')
        except:
            print('failed to deactivate speech recognition')
        try:
            print('attemting to stop any active dictation')
            stop_transcription_function()
            print('dictation de-activated')
        except:
            print('failed to stop dictation')
        try:
            print('attemting to shutdown symbiot server')
            sock_con.close()
            print('symbiot server deactivated')
        except:
            print('failed to shutdown symbiot server')
        try:
            print('attemting to stop auto crawlers')
            i=0
            pid_item = []
            for auto_crawler_pids in auto_crawler_pid:

                # get pid from list
                print('attempting to stop:', auto_crawler_pid[i])
                global_pid = auto_crawler_pid[i]

                # get the name of pid
                p = subprocess.Popen(["ps -o cmd= {}".format(global_pid)], stdout=subprocess.PIPE, shell=True)
                global_pid_name = str(p.communicate()[0])

                # kill global pid
                os.kill(global_pid, 15)

                # each crawler has a twin so we need to kill both instances of each crawler safely
                # use global pid name to find child pid [careful handling]
                search_str = global_pid_name.replace("b'", "")
                search_str = search_str.replace("\\n'", "")
                search_str = search_str.replace("/bin/sh -c ", "")
                print('search string:', search_str)
                cmd = 'pgrep python3.5'
                p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                found_pid = str(p2.communicate()[0])
                found_pid = found_pid.replace("b'", "")
                found_pid = found_pid.split('\\n')

                i_2 = 0
                for found_pids in found_pid:
                    if found_pid[i_2].isdigit():
                        # get the name of suspected second pid [careful handling]
                        p3 = subprocess.Popen(["ps -o cmd= {}".format(found_pid[i_2])], stdout=subprocess.PIPE, shell=True)
                        found_pid_name = str(p3.communicate()[0])
                        found_pid_name = found_pid_name.replace("b'", "")
                        found_pid_name = found_pid_name.replace("\\n'", "")

                        # only kill the twin process if strings match! [careful handling]
                        if found_pid_name == search_str:
                            pid_2 = int(found_pid[i_2])
                            print('killing twin process', found_pid_name)
                            os.kill(pid_2, 15)
                    i_2 += 1
                i += 1

            print('auto crawlers deactivated')
        except:
            print('failed to stop auto crawlers')

    def audio_index_enable_disable_function(self):
        global audio_active_config_bool
        global check_index_audio_config
        enabled_str = 'INDEXENGINE_AUDIO: enabled'
        disabled_str = 'INDEXENGINE_AUDIO: disabled'
        if audio_active_config_bool == False:
            if check_index_audio_config == True:
                print('enabling audio index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_AUDIO: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                audio_active_config_bool = True
                self.index_audio_enable_disable_button.setText('Enabled')
                self.index_audio_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif audio_active_config_bool == True:
            if check_index_audio_config == True:
                print('disabling audio index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_AUDIO: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                audio_active_config_bool = False
                self.index_audio_enable_disable_button.setText('Disabled')
                self.index_audio_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def video_index_enable_disable_function(self):
        global video_active_config_bool
        global check_index_video_config
        enabled_str = 'INDEXENGINE_VIDEO: enabled'
        disabled_str = 'INDEXENGINE_VIDEO: disabled'
        if video_active_config_bool == False:
            if check_index_video_config == True:
                print('enabling video index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_VIDEO: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                video_active_config_bool = True
                self.index_video_enable_disable_button.setText('Enabled')
                self.index_video_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif video_active_config_bool == True:
            if check_index_video_config == True:
                print('disabling video index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_VIDEO: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                video_active_config_bool = False
                self.index_video_enable_disable_button.setText('Disabled')
                self.index_video_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def image_index_enable_disable_function(self):
        global image_active_config_bool
        global check_index_image_config
        enabled_str = 'INDEXENGINE_IMAGE: enabled'
        disabled_str = 'INDEXENGINE_IMAGE: disabled'
        if image_active_config_bool == False:
            if check_index_image_config == True:
                print('enabling image index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_IMAGE: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                image_active_config_bool = True
                self.index_image_enable_disable_button.setText('Enabled')
                self.index_image_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif image_active_config_bool == True:
            if check_index_image_config == True:
                print('disabling image index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_IMAGE: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                image_active_config_bool = False
                self.index_image_enable_disable_button.setText('Disabled')
                self.index_image_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def text_index_enable_disable_function(self):
        global text_active_config_bool
        global check_index_text_config
        enabled_str = 'INDEXENGINE_TEXT: enabled'
        disabled_str = 'INDEXENGINE_TEXT: disabled'
        if text_active_config_bool == False:
            if check_index_text_config == True:
                print('enabling text index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_TEXT: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                text_active_config_bool = True
                self.index_text_enable_disable_button.setText('Enabled')
                self.index_text_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif text_active_config_bool == True:
            if check_index_text_config == True:
                print('disabling text index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_TEXT: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                text_active_config_bool = False
                self.index_text_enable_disable_button.setText('Disabled')
                self.index_text_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
            )

    def drive1_enable_disable_function(self):
        global drive_1_active_config_bool
        global check_index_drive1_config
        enabled_str = 'INDEXENGINE_DRIVE1: enabled'
        disabled_str = 'INDEXENGINE_DRIVE1: disabled'
        if drive_1_active_config_bool == False:
            if check_index_drive1_config == True:
                print('enabling drive1 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE1: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_1_active_config_bool = True
                self.drive1_enable_disable_button.setText('Enabled')
                self.drive1_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_1_active_config_bool == True:
            if check_index_drive1_config == True:
                print('disabling drive1 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE1: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_1_active_config_bool = False
                self.drive1_enable_disable_button.setText('Disabled')
                self.drive1_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive2_enable_disable_function(self):
        global drive_2_active_config_bool
        global check_index_drive2_config
        enabled_str = 'INDEXENGINE_DRIVE2: enabled'
        disabled_str = 'INDEXENGINE_DRIVE2: disabled'
        if drive_2_active_config_bool == False:
            if check_index_drive2_config == True:
                print('enabling drive2 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE2: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_2_active_config_bool = True
                self.drive2_enable_disable_button.setText('Enabled')
                self.drive2_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_2_active_config_bool == True:
            if check_index_drive2_config == True:
                print('disabling drive2 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE2: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_2_active_config_bool = False
                self.drive2_enable_disable_button.setText('Disabled')
                self.drive2_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive3_enable_disable_function(self):
        global drive_3_active_config_bool
        global check_index_drive3_config
        enabled_str = 'INDEXENGINE_DRIVE3: enabled'
        disabled_str = 'INDEXENGINE_DRIVE3: disabled'
        if drive_3_active_config_bool == False:
            if check_index_drive3_config == True:
                print('enabling drive3 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE3: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_3_active_config_bool = True
                self.drive3_enable_disable_button.setText('Enabled')
                self.drive3_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_3_active_config_bool == True:
            if check_index_drive3_config == True:
                print('disabling drive3 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE3: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_3_active_config_bool = False
                self.drive3_enable_disable_button.setText('Disabled')
                self.drive3_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive4_enable_disable_function(self):
        global drive_4_active_config_bool
        global check_index_drive4_config
        enabled_str = 'INDEXENGINE_DRIVE4: enabled'
        disabled_str = 'INDEXENGINE_DRIVE4: disabled'
        if drive_4_active_config_bool == False:
            if check_index_drive4_config == True:
                print('enabling drive4 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE4: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_4_active_config_bool = True
                self.drive4_enable_disable_button.setText('Enabled')
                self.drive4_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_4_active_config_bool == True:
            if check_index_drive4_config == True:
                print('disabling drive4 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE4: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_4_active_config_bool = False
                self.drive4_enable_disable_button.setText('Disabled')
                self.drive4_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive5_enable_disable_function(self):
        global drive_5_active_config_bool
        global check_index_drive5_config
        enabled_str = 'INDEXENGINE_DRIVE5: enabled'
        disabled_str = 'INDEXENGINE_DRIVE5: disabled'
        if drive_5_active_config_bool == False:
            if check_index_drive5_config == True:
                print('enabling drive5 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE5: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_5_active_config_bool = True
                self.drive5_enable_disable_button.setText('Enabled')
                self.drive5_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_5_active_config_bool == True:
            if check_index_drive4_config == True:
                print('disabling drive5 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE5: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_5_active_config_bool = False
                self.drive5_enable_disable_button.setText('Disabled')
                self.drive5_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive6_enable_disable_function(self):
        global drive_6_active_config_bool
        global check_index_drive6_config
        enabled_str = 'INDEXENGINE_DRIVE6: enabled'
        disabled_str = 'INDEXENGINE_DRIVE6: disabled'
        if drive_6_active_config_bool == False:
            if check_index_drive4_config == True:
                print('enabling drive6 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE6: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_6_active_config_bool = True
                self.drive6_enable_disable_button.setText('Enabled')
                self.drive6_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_6_active_config_bool == True:
            if check_index_drive4_config == True:
                print('disabling drive6 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE6: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_6_active_config_bool = False
                self.drive6_enable_disable_button.setText('Disabled')
                self.drive6_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive7_enable_disable_function(self):
        global drive_7_active_config_bool
        global check_index_drive7_config
        enabled_str = 'INDEXENGINE_DRIVE7: enabled'
        disabled_str = 'INDEXENGINE_DRIVE7: disabled'
        if drive_7_active_config_bool == False:
            if check_index_drive7_config == True:
                print('enabling drive7 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE7: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_7_active_config_bool = True
                self.drive7_enable_disable_button.setText('Enabled')
                self.drive7_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_7_active_config_bool == True:
            if check_index_drive7_config == True:
                print('disabling drive7 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE7: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_7_active_config_bool = False
                self.drive7_enable_disable_button.setText('Disabled')
                self.drive7_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def drive8_enable_disable_function(self):
        global drive_8_active_config_bool
        global check_index_drive8_config
        enabled_str = 'INDEXENGINE_DRIVE8: enabled'
        disabled_str = 'INDEXENGINE_DRIVE8: disabled'
        if drive_8_active_config_bool == False:
            if check_index_drive8_config == True:
                print('enabling drive8 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE8: '):
                        line_list[i] = str(enabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_8_active_config_bool = True
                self.drive8_enable_disable_button.setText('Enabled')
                self.drive8_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: green;
                   border: false;}"""
                )
        elif drive_8_active_config_bool == True:
            if check_index_drive8_config == True:
                print('disabling drive8 index engine')
                line_list = []
                with codecs.open(config_file, 'r') as fo:
                    for line in fo:
                        line.strip()
                        line_list.append(line)
                    fo.close()
                i = 0
                for line_lists in line_list:
                    if line_list[i].startswith('INDEXENGINE_DRIVE8: '):
                        line_list[i] = str(disabled_str + '\n')
                    i += 1
                i = 0
                with open(config_file, 'w') as fo:
                    for line_lists in line_list:
                        fo.writelines(line_list[i])
                        i += 1
                    fo.close()
                drive_8_active_config_bool = False
                self.drive8_enable_disable_button.setText('Disabled')
                self.drive8_enable_disable_button.setStyleSheet(
                    """QPushButton {background-color: rgb(0, 0, 0);
                   color: red;
                   border: false;}"""
                )

    def incremental_resize_function(self):
        global incrementalResize
        if incrementalResize == 0:
            incrementalResize = 1
            print('resizing main window: 780.185')
            self.setFixedSize(780, 185)

        elif incrementalResize == 1:
            incrementalResize = 0
            print('resizing main window: 780.455')
            self.setFixedSize(780, 455)

    def use_local_wiki_function(self):
        global allow_wiki_local_server_bool
        global allow_wiki_local_server_configuration
        if allow_wiki_local_server_bool == True:
            self.use_local_wiki_button.setText('Disabled')
            self.use_local_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
            allow_wiki_local_server_bool = False
        elif allow_wiki_local_server_bool == False:
            self.use_local_wiki_button.setText('Enabled')
            self.use_local_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
            allow_wiki_local_server_bool = True
        line_list = []
        path_text = ''
        if allow_wiki_local_server_bool == True:
            path_text = 'enabled'
        elif allow_wiki_local_server_bool == False:
            path_text = 'disabled'
        print('use local wiki server:', path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('ALLOW_WIKI_LOCAL_SERVER: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('ALLOW_WIKI_LOCAL_SERVER: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i += 1
        fo.close()
        print('updated: configuration')
        allow_wiki_local_server_configuration = path_text


    def dictate_wiki_function(self):
        global wiki_dictate_bool
        global wiki_dictate_configuration
        if wiki_dictate_bool == True:
            self.dictate_wiki_button.setText('Disabled')
            self.dictate_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
            wiki_dictate_bool = False
        elif wiki_dictate_bool == False:
            self.dictate_wiki_button.setText('Enabled')
            self.dictate_wiki_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
            wiki_dictate_bool = True
        line_list = []
        path_text = ''
        if wiki_dictate_bool == True:
            path_text = 'enabled'
        elif wiki_dictate_bool == False:
            path_text = 'disabled'
        print('dictate wiki transcripts:', path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_TRANSCRIPT_DICTATE: '):
                print('Replacing list item:', line_list[i], 'with', path_text)
                line_list[i] = str('WIKI_TRANSCRIPT_DICTATE: ' + path_text + '\n')
            i += 1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i += 1
        fo.close()
        print('updated: configuration')
        wiki_dictate_configuration = path_text

    def wiki_show_browser_function(self):
        global wiki_show_browser_bool
        global wiki_show_browser_configuration
        if wiki_show_browser_bool == True:
            self.wiki_show_browser_button.setText('Disabled')
            self.wiki_show_browser_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: red;
               border: false;}"""
            )
            wiki_show_browser_bool = False
        elif wiki_show_browser_bool == False:
            self.wiki_show_browser_button.setText('Enabled')
            self.wiki_show_browser_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
               color: green;
               border: false;}"""
            )
            wiki_show_browser_bool = True
        line_list = []
        path_text = ''
        if wiki_show_browser_bool == True:
            path_text = 'enabled'
        elif wiki_show_browser_bool == False:
            path_text = 'disabled'
        print('show wiki in browser:', path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_TRANSCRIPT_SHOW_BROWSER: '):
                print('Replacing list item:',line_list[i], 'with',path_text)
                line_list[i] = str('WIKI_TRANSCRIPT_SHOW_BROWSER: '+path_text+'\n')
            i+=1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i+=1
        fo.close()
        print('updated: configuration')
        wiki_show_browser_configuration = path_text

    def symbiot_server_ip_function(self):
        global symbiot_server_ip_configuration
        if self.symbiot_server_ip_editable == True:
            print('setting symbiot server ip line edit: false')
            self.symbiot_server_ip_edit.setReadOnly(False)
            self.symbiot_server_ip_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiot_server_ip_editable = False
        elif self.symbiot_server_ip_editable == False:
            print('setting asymbiot server ip line edit: true')
            self.symbiot_server_ip_edit.setReadOnly(True)
            self.symbiot_server_ip_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiot_server_ip_edit.setText(symbiot_server_ip_configuration)
            self.symbiot_server_ip_editable = True

    def write_symbiot_server_ip_function(self):
        global symbiot_server_ip_configuration
        line_list = []
        path_text = self.symbiot_server_ip_edit.text()
        print('IP Entered:',path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_SERVER: '):
                print('Replacing list item:',line_list[i], 'with',path_text)
                line_list[i] = str('SYMBIOT_SERVER: '+path_text+'\n')
            i+=1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i+=1
        fo.close()
        print('updated: symbiot server ip configuration')
        symbiot_server_ip_configuration = path_text
        self.symbiot_server_ip_function()

    def symbiot_server_port_function(self):
        global symbiot_server_port_configuration
        if self.symbiot_server_port_editable == True:
            print('setting symbiot server port line edit: false')
            self.symbiot_server_port_edit.setReadOnly(False)
            self.symbiot_server_port_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiot_server_port_editable = False
        elif self.symbiot_server_port_editable == False:
            print('setting symbiot server port line edit: true')
            self.symbiot_server_port_edit.setReadOnly(True)
            self.symbiot_server_port_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiot_server_port_edit.setText(symbiot_server_port_configuration)
            self.symbiot_server_port_editable = True

    def write_symbiot_server_port_function(self):
        global symbiot_server_port_configuration
        line_list = []
        path_text = self.symbiot_server_port_edit.text()
        print('Port Entered:',path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_SERVER_PORT: '):
                print('Replacing list item:',line_list[i], 'with',path_text)
                line_list[i] = str('SYMBIOT_SERVER_PORT: '+path_text+'\n')
            i+=1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i+=1
        fo.close()
        print('updated: symbiot server port configuration')
        symbiot_server_port_configuration = path_text
        self.symbiot_server_port_function()

    def wiki_server_ip_function(self):
        global wiki_local_server_ip_configuration
        if self.wikiServer_ip_editable == True:
            self.wiki_server_ip_edit.setReadOnly(False)
            self.wiki_server_ip_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.wikiServer_ip_editable = False
        elif self.wikiServer_ip_editable == False:
            print('setting symbiot ip line edit: true')
            self.wiki_server_ip_edit.setReadOnly(True)
            self.wiki_server_ip_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.wiki_server_ip_edit.setText(wiki_local_server_ip_configuration)
            self.wikiServer_ip_editable = True

    def write_wiki_server_function(self):
        global wiki_local_server_ip_configuration
        line_list = []
        path_text = self.wiki_server_ip_edit.text()
        print('wiki ip entered:',path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_LOCAL_SERVER: '):
                print('Replacing list item:',line_list[i], 'with',path_text)
                line_list[i] = str('WIKI_LOCAL_SERVER: '+path_text+'\n')
            i+=1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i+=1
        fo.close()
        print('updated: wiki server ip configuration')
        wiki_local_server_ip_configuration = path_text
        self.wiki_server_ip_function()

    def wiki_server_port_function(self):
        global wiki_local_server_port_configuration
        if self.wiki_server_port_editable == True:
            print('setting symbiot port line edit: false')
            self.wiki_server_port_edit.setReadOnly(False)
            self.wiki_server_port_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.wiki_server_port_editable = False
        elif self.wiki_server_port_editable == False:
            print('setting symbiot ip line edit: true')
            self.wiki_server_port_edit.setReadOnly(True)
            self.wiki_server_port_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.wiki_server_port_edit.setText(wiki_local_server_port_configuration)
            self.wiki_server_port_editable = True

    def write_wiki_server_port_function(self):
        global wiki_local_server_port_configuration
        line_list = []
        path_text = self.wiki_server_port_edit.text()
        print('wiki server port entered:',path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('WIKI_LOCAL_SERVER_PORT: '):
                print('Replacing list item:',line_list[i], 'with',path_text)
                line_list[i] = str('WIKI_LOCAL_SERVER_PORT: '+path_text+'\n')
            i+=1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i+=1
        fo.close()
        print('updated: wiki server port configuration')
        wiki_local_server_port_configuration = path_text
        self.wiki_server_port_function()

    def symbiot_ip_function(self):
        global symbiot_ip_configuration
        if self.symbiot_ip_editable == True:
            print('setting symbiot ip line edit: false')
            self.symbiot_ip_edit.setReadOnly(False)
            self.symbiot_ip_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiot_ip_editable = False
        elif self.symbiot_ip_editable == False:
            print('setting symbiot ip line edit: true')
            self.symbiot_ip_edit.setReadOnly(True)
            self.symbiot_ip_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiot_ip_edit.setText(symbiot_ip_configuration)
            self.symbiot_ip_editable = True

    def write_symbiot_ip_function(self):
        global symbiot_ip_configuration
        line_list = []
        path_text = self.symbiot_ip_edit.text()
        print('symbiot ip entered:',path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_IP: '):
                print('Replacing list item:',line_list[i], 'with',path_text)
                line_list[i] = str('SYMBIOT_IP: '+path_text+'\n')
            i+=1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i+=1
        fo.close()
        print('updated: symbiot ip configuration')
        symbiot_ip_configuration = path_text
        self.symbiot_ip_function()

    def symbiot_mac_function(self):
        global symbiot_mac_configuration
        if self.symbiot_mac_editable == True:
            print('setting symbiot mac line edit: false')
            self.symbiot_mac_edit.setReadOnly(False)
            self.symbiot_mac_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.symbiot_mac_editable = False
        elif self.symbiot_mac_editable == False:
            print('setting symbiot mac line edit: true')
            self.symbiot_mac_edit.setReadOnly(True)
            self.symbiot_mac_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.symbiot_mac_edit.setText(symbiot_mac_configuration)
            self.symbiot_mac_editable = True

    def write_symbiot_mac_function(self):
        global symbiot_mac_configuration
        line_list = []
        path_text = self.symbiot_mac_edit.text()
        print('symbiot mac entered:',path_text)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                line_list.append(line)
        i = 0
        for line_lists in line_list:
            if line_list[i].startswith('SYMBIOT_MAC: '):
                print('Replacing list item:',line_list[i], 'with',path_text)
                line_list[i] = str('SYMBIOT_MAC: '+path_text+'\n')
            i+=1
        fo.close()
        i = 0
        with codecs.open(config_file, 'w', encoding="utf-8") as fo:
            for line_lists in line_list:
                fo.writelines(line_list[i])
                i+=1
        fo.close()
        print('updated: symbiot mac configuration')
        symbiot_mac_configuration = path_text
        self.symbiot_mac_function()

    def index_audio_configuration_function(self):
        global audio_configuration
        if self.index_audio_editable == True:
            print('setting audio index path line edit: false')
            self.index_audio_edit.setReadOnly(False)
            self.index_audio_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_audio_editable = False
        elif self.index_audio_editable == False:
            print('setting audio index path line edit: true')
            self.index_audio_edit.setReadOnly(True)
            self.index_audio_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.index_audio_edit.setText(audio_configuration.replace('DIRAUD: ', ''))
            self.index_audio_editable = True

    def write_audio_path_function(self):
        global check_index_audio_config
        global audio_configuration
        line_list = []
        path_text = self.index_audio_edit.text()
        print('Path Entered:',path_text)
        if os.path.exists(path_text):
            print('Path Exists:',path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRAUD:'):
                    print('Replacing list item:',line_list[i], 'with',path_text)
                    line_list[i] = str('DIRAUD: '+path_text+'\n')
                i+=1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i+=1
            fo.close()
            print('updated: audio path configuration')
            check_index_audio_config = True
            audio_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.index_audio_edit.setText(audio_configuration.replace('DIRAUD: ', ''))
            check_index_audio_config = False
        self.index_audio_configuration_function()

    def index_video_configuration_function(self):
        global video_configuration
        if self.index_video_editable == True:
            print('setting video index path line edit: false')
            self.index_video_edit.setReadOnly(False)
            self.index_video_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_video_editable = False
        elif self.index_video_editable == False:
            print('setting video index path line edit: true')
            self.index_video_edit.setReadOnly(True)
            self.index_video_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.index_video_edit.setText(video_configuration.replace('DIRVID: ', ''))
            self.index_video_editable = True

    def write_video_path_function(self):
        global check_index_video_config
        global video_configuration
        line_list = []
        path_text = self.index_video_edit.text()
        print('Path Entered:',path_text)
        if os.path.exists(path_text):
            print('Path Exists:',path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRVID:'):
                    print('Replacing list item:',line_list[i], 'with',path_text)
                    line_list[i] = str('DIRVID: '+path_text+'\n')
                i+=1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i+=1
            fo.close()
            print('updated: video path configuration')
            check_index_video_config = True
            video_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.index_video_edit.setText(video_configuration.replace('DIRVID: ', ''))
            check_index_video_config = False
        self.index_video_configuration_function()

    def index_images_configuration_function(self):
        global image_configuration
        if self.index_image_editable == True:
            print('setting image index path line edit: false')
            self.index_images_edit.setReadOnly(False)
            self.index_images_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_image_editable = False
        elif self.index_image_editable == False:
            print('setting image index path line edit: true')
            self.index_images_edit.setReadOnly(True)
            self.index_images_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.index_images_edit.setText(image_configuration.replace('DIRIMG: ', ''))
            self.index_image_editable = True

    def write_images_path_function(self):
        global check_index_image_config
        global image_configuration
        line_list = []
        path_text = self.index_images_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRIMG:'):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DIRIMG: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: images path configuration')
            check_index_image_config = True
            image_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.index_images_edit.setText(image_configuration.replace('DIRIMG: ', ''))
            check_index_image_config = False
        self.index_images_configuration_function()

    def index_text_configuration_function(self):
        global text_configuration
        if self.index_text_editable == True:
            print('setting text index path line edit: false')
            self.index_text_edit.setReadOnly(False)
            self.index_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_text_editable = False
        elif self.index_text_editable == False:
            print('setting text index path line edit: true')
            self.index_text_edit.setReadOnly(True)
            self.index_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.index_text_edit.setText(text_configuration.replace('DIRTXT: ', ''))
            self.index_text_editable = True

    def write_text_path_function(self):
        global check_index_text_config
        global text_configuration
        line_list = []
        path_text = self.index_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DIRTXT:'):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DIRTXT: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: text path configuration')
            check_index_text_config = True
            text_configuration = path_text

        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.index_text_edit.setText(text_configuration.replace('DIRTXT: ', ''))
            check_index_text_config = False
        self.index_text_configuration_function()

    def index_drive1_configuration_function(self):
        global drive1_configuration
        if self.index_drive1_editable == False:
            print('setting drive1 index path line edit: true')
            self.drive1_text_edit.setReadOnly(False)
            self.drive1_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive1_editable = True
        elif self.index_drive1_editable == True:
            print('setting drive1 index path line edit: false')
            self.drive1_text_edit.setReadOnly(True)
            self.drive1_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive1_text_edit.setText(drive1_configuration.replace('DRIVE1: ', ''))
            self.index_drive1_editable = False

    def write_drive1_path_function(self):
        global check_index_drive1_config
        global drive1_configuration
        line_list = []
        path_text = self.drive1_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE1: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE1: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 1 path configuration')
            check_index_drive1_config = True
            drive1_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive1_text_edit.setText(drive1_configuration.replace('DRIVE1: ', ''))
            check_index_drive1_config = False
        self.index_drive1_configuration_function()

    def index_drive2_configuration_function(self):
        global drive2_configuration
        if self.index_drive2_editable == False:
            print('setting drive2 index path line edit: true')
            self.drive2_text_edit.setReadOnly(False)
            self.drive2_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive2_editable = True
        elif self.index_drive2_editable == True:
            print('setting drive2 index path line edit: false')
            self.drive2_text_edit.setReadOnly(True)
            self.drive2_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive2_text_edit.setText(drive2_configuration.replace('DRIVE2: ', ''))
            self.index_drive2_editable = False

    def write_drive2_path_function(self):
        global check_index_drive2_config
        global drive2_configuration
        line_list = []
        path_text = self.drive2_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE2: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE2: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 2 path configuration')
            check_index_drive2_config = True
            drive2_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive2_text_edit.setText(drive2_configuration.replace('DRIVE2: ', ''))
            check_index_drive2_config = False
        self.index_drive2_configuration_function()

    def index_drive3_configuration_function(self):
        global drive3_configuration
        if self.index_drive3_editable == False:
            print('setting drive3 index path line edit: true')
            self.drive3_text_edit.setReadOnly(False)
            self.drive3_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive3_editable = True
        elif self.index_drive3_editable == True:
            print('setting drive3 index path line edit: false')
            self.drive3_text_edit.setReadOnly(True)
            self.drive3_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive3_text_edit.setText(drive3_configuration.replace('DRIVE3: ', ''))
            self.index_drive3_editable = False

    def write_drive3_path_function(self):
        global check_index_drive3_config
        global drive3_configuration
        line_list = []
        path_text = self.drive3_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE3: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE3: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 3 path configuration')
            check_index_drive3_config = True
            drive3_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive3_text_edit.setText(drive3_configuration.replace('DRIVE3: ', ''))
            check_index_drive3_config = False
        self.index_drive3_configuration_function()

    def index_drive4_configuration_function(self):
        global drive4_configuration
        if self.index_drive4_editable == False:
            print('setting drive4 index path line edit: true')
            self.drive4_text_edit.setReadOnly(False)
            self.drive4_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive4_editable = True
        elif self.index_drive4_editable == True:
            print('setting drive4 index path line edit: false')
            self.drive4_text_edit.setReadOnly(True)
            self.drive4_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive4_text_edit.setText(drive4_configuration.replace('DRIVE4: ', ''))
            self.index_drive4_editable = False

    def write_drive4_path_function(self):
        global check_index_drive4_config
        global drive4_configuration
        line_list = []
        path_text = self.drive4_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE4: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE4: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 4 path configuration')
            check_index_drive4_config = True
            drive4_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive4_text_edit.setText(drive4_configuration.replace('DRIVE4: ', ''))
            check_index_drive4_config = False
        self.index_drive4_configuration_function()

    def index_drive5_configuration_function(self):
        global drive5_configuration
        if self.index_drive5_editable == False:
            print('setting drive5 index path line edit: true')
            self.drive5_text_edit.setReadOnly(False)
            self.drive5_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive5_editable = True
        elif self.index_drive5_editable == True:
            print('setting drive5 index path line edit: false')
            self.drive5_text_edit.setReadOnly(True)
            self.drive5_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive5_text_edit.setText(drive5_configuration.replace('DRIVE5: ', ''))
            self.index_drive5_editable = False

    def write_drive5_path_function(self):
        global check_index_drive5_config
        global drive5_configuration
        line_list = []
        path_text = self.drive5_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE5: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE5: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 5 path configuration')
            check_index_drive5_config = True
            drive5_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive5_text_edit.setText(drive5_configuration.replace('DRIVE5: ', ''))
            check_index_drive5_config = False
        self.index_drive5_configuration_function()

    def index_drive6_configuration_function(self):
        global drive6_configuration
        if self.index_drive6_editable == False:
            print('setting drive6 index path line edit: true')
            self.drive6_text_edit.setReadOnly(False)
            self.drive6_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive6_editable = True
        elif self.index_drive6_editable == True:
            print('setting drive6 index path line edit: false')
            self.drive6_text_edit.setReadOnly(True)
            self.drive6_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive6_text_edit.setText(drive6_configuration.replace('DRIVE6: ', ''))
            self.index_drive6_editable = False

    def write_drive6_path_function(self):
        global check_index_drive6_config
        global drive6_configuration
        line_list = []
        path_text = self.drive6_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE6: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE6: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 6 path configuration')
            check_index_drive6_config = True
            drive6_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive6_text_edit.setText(drive6_configuration.replace('DRIVE6: ', ''))
            check_index_drive6_config = False
        self.index_drive6_configuration_function()

    def index_drive7_configuration_function(self):
        global drive7_configuration
        if self.index_drive7_editable == False:
            print('setting drive7 index path line edit: true')
            self.drive7_text_edit.setReadOnly(False)
            self.drive7_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive7_editable = True
        elif self.index_drive7_editable == True:
            print('setting drive7 index path line edit: false')
            self.drive7_text_edit.setReadOnly(True)
            self.drive7_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive7_text_edit.setText(drive7_configuration.replace('DRIVE7: ', ''))
            self.index_drive7_editable = False

    def write_drive7_path_function(self):
        global check_index_drive7_config
        global drive7_configuration
        line_list = []
        path_text = self.drive7_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE7: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE7: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 7 path configuration')
            check_index_drive7_config = True
            drive7_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive7_text_edit.setText(drive7_configuration.replace('DRIVE7: ', ''))
            check_index_drive7_config = False
        self.index_drive7_configuration_function()

    def index_drive8_configuration_function(self):
        global drive8_configuration
        if self.index_drive8_editable == False:
            print('setting drive8 index path line edit: true')
            self.drive8_text_edit.setReadOnly(False)
            self.drive8_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(25, 24, 25);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: white;}"""
            )
            self.index_drive8_editable = True
        elif self.index_drive8_editable == True:
            print('setting drive8 index path line edit: false')
            self.drive8_text_edit.setReadOnly(True)
            self.drive8_text_edit.setStyleSheet(
                """QLineEdit {background-color: rgb(15, 14, 15);
                border:5px solid rgb(0, 0, 0);
                selection-color: black;
                selection-background-color: black;
                color: grey;}"""
            )
            self.drive8_text_edit.setText(drive8_configuration.replace('DRIVE8: ', ''))
            self.index_drive8_editable = False

    def write_drive8_path_function(self):
        global check_index_drive8_config
        global drive8_configuration
        line_list = []
        path_text = self.drive8_text_edit.text()
        print('Path Entered:', path_text)
        if os.path.exists(path_text):
            print('Path Exists:', path_text)
            with open(config_file, 'r') as fo:
                for line in fo:
                    line_list.append(line)
            i = 0
            for line_lists in line_list:
                if line_list[i].startswith('DRIVE8: '):
                    print('Replacing list item:', line_list[i], 'with', path_text)
                    line_list[i] = str('DRIVE8: ' + path_text + '\n')
                i += 1
            fo.close()
            i = 0
            with open(config_file, 'w') as fo:
                for line_lists in line_list:
                    fo.writelines(line_list[i])
                    i += 1
            fo.close()
            print('updated: drive 8 path configuration')
            check_index_drive8_config = True
            drive8_configuration = path_text
        elif not os.path.exists(path_text):
            print('Path does not exist')
            self.drive8_text_edit.setText(drive6_configuration.replace('DRIVE8: ', ''))
            check_index_drive8_config = False
        self.index_drive8_configuration_function()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        # Speech Recognition color background
        qp.setBrush(QColor(25, 24, 25))
        # Speech Recognition background dimensions: MOVE: width, height. RECT-SIZE: width height
        qp.drawRect(20, 45, 740, 120)

        # Settings Index Engine Configuration
        qp.setBrush(QColor(25, 24, 25))
        qp.drawRect(20, 200, 740, 90)

        # Settings Top Divider
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(358, 200, 4, 90)

        # Symbiot Settings
        qp.setBrush(QColor(25, 24, 25))
        qp.drawRect(20, 320, 740, 100)

        # Symbiot Top Divider
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(358, 320, 4, 100)


configuration_checks_function()
time.sleep(1)


class GuiControllerClass(QThread):
    def __init__(self, sr_info, text_box_value, text_box_verbose1, text_box_verbose2):
        QThread.__init__(self)
        self.sr_info = sr_info
        self.text_box_value = text_box_value
        self.text_box_verbose1 = text_box_verbose1
        self.text_box_verbose2 = text_box_verbose2
        self.guiControllerCount = 0

    def run(self):
        while self.guiControllerCount <= 1:
            if self.guiControllerCount == 1:
                self.sr_info.setText("")
                self.text_box_value.setText("")
                self.text_box_verbose1.setText("")
                self.text_box_verbose2.setText("")
                self.guiControllerCount = 0
                break
            else:
                time.sleep(4)
                self.guiControllerCount += 1

    def stop_gui_controller(self):
        self.sr_info.setText("")
        self.text_box_value.setText("")
        self.text_box_verbose1.setText("")
        self.text_box_verbose2.setText("")
        self.terminate()


class ConfigInteractionPermissionClass(QThread):
    def __init__(self, index_audio_enable_disable_button,
                 index_video_enable_disable_button,
                 index_image_enable_disable_button,
                 index_text_enable_disable_button,
                 index_audio_edit,
                 index_video_edit,
                 index_images_edit,
                 index_text_edit,
                 index_audio_button,
                 index_video_button,
                 index_image_button,
                 index_text_button,
                 drive1_enable_disable_button,
                 drive2_enable_disable_button,
                 drive3_enable_disable_button,
                 drive4_enable_disable_button,
                 drive1_text_edit,
                 drive2_text_edit,
                 drive3_text_edit,
                 drive4_text_edit,
                 drive1_button,
                 drive2_button,
                 drive3_button,
                 drive4_button):

        QThread.__init__(self)
        self.index_audio_enable_disable_button = index_audio_enable_disable_button
        self.index_video_enable_disable_button = index_video_enable_disable_button
        self.index_text_enable_disable_button = index_text_enable_disable_button
        self.index_image_enable_disable_button = index_image_enable_disable_button
        self.index_audio_edit = index_audio_edit
        self.index_video_edit = index_video_edit
        self.index_images_edit = index_images_edit
        self.index_text_edit = index_text_edit
        self.index_audio_button = index_audio_button
        self.index_video_button = index_video_button
        self.index_image_button = index_image_button
        self.index_text_button = index_text_button

        self.drive1_enable_disable_button = drive1_enable_disable_button
        self.drive2_enable_disable_button = drive2_enable_disable_button
        self.drive3_enable_disable_button = drive3_enable_disable_button
        self.drive4_enable_disable_button = drive4_enable_disable_button
        self.drive1_text_edit = drive1_text_edit
        self.drive2_text_edit = drive2_text_edit
        self.drive3_text_edit = drive3_text_edit
        self.drive4_text_edit = drive4_text_edit
        self.drive1_button = drive1_button
        self.drive2_button = drive2_button
        self.drive3_button = drive3_button
        self.drive4_button = drive4_button

    def run(self):
        # This Class runs on a thread to prevent spamming writes to config via enable/disable button. minus the
        # nice graphics like a loading/waiting spinning circle. (Spamming those writes might crash the program).
        print('plugged in: configInteractionPermissionClass')
        print('temporarily disabling configuration settings: writing to config...')
        index_enable_disable_button_item = [self.index_audio_enable_disable_button,
                                            self.index_video_enable_disable_button,
                                            self.index_image_enable_disable_button,
                                            self.index_text_enable_disable_button,
                                            self.index_audio_edit,
                                            self.index_video_edit,
                                            self.index_images_edit,
                                            self.index_text_edit,
                                            self.index_audio_button,
                                            self.index_video_button,
                                            self.index_image_button,
                                            self.index_text_button,
                                            self.drive1_enable_disable_button,
                                            self.drive2_enable_disable_button,
                                            self.drive3_enable_disable_button,
                                            self.drive4_enable_disable_button,
                                            self.drive1_text_edit,
                                            self.drive2_text_edit,
                                            self.drive3_text_edit,
                                            self.drive4_text_edit,
                                            self.drive1_button,
                                            self.drive2_button,
                                            self.drive3_button,
                                            self.drive4_button
                                            ]
        i = 0
        for index_enable_disable_button_items in index_enable_disable_button_item:
            index_enable_disable_button_item[i].setEnabled(False)
            i += 1
        time.sleep(2)
        print('enabling configuration settings: finished write')
        i = 0
        for index_enable_disable_button_items in index_enable_disable_button_item:
            index_enable_disable_button_item[i].setEnabled(True)
            i += 1


class TextBoxVerbose2Class(QThread):
    def __init__(self, text_box_verbose2):
        QThread.__init__(self)
        self.text_box_verbose2 = text_box_verbose2

    def __del__(self):
        self.wait()

    def run(self):
        global sppid
        sppid_str = str(sppid)
        sppid_str2 = str('subprocess PID: ')
        self.text_box_verbose2.setText(sppid_str2 + sppid_str)


class OpenDirectoryClass(QThread):
    def __init__(self, text_box_verbose,
                 text_box_verbose2):

        QThread.__init__(self)
        self.text_box_verbose = text_box_verbose
        self.text_box_verbose2 = text_box_verbose2

    def __del__(self):
        self.wait()

    def run(self):
        global speechRecognitionThread
        print('plugged in: openDirectoryClass')
        # primed for a bool set in gui (loop sr or run sr once)
        speechRecognitionThread.stop_sr()


class FindOpenAudioClass(QThread):
    def __init__(self,
                 text_box_verbose1):

        QThread.__init__(self)
        self.text_box_verbose1 = text_box_verbose1

    def __del__(self):
        self.wait()

    def run(self):
        print('plugged in thread: findOpenAudioClass')
        global audio_active_config_bool
        global secondary_key
        global audio_configuration
        global speechRecognitionThread

        if audio_active_config_bool == True:
            audio_path = audio_configuration.replace('DIRAUD: ', '')
            target_root_aud = str(audio_path.split('\\')[0] + '\\')
            print('audio directory:', audio_path)

            with open(secondary_key_store, 'r') as fo:
                for line in fo:
                    secondary_key = line.strip()
            print('secondary key:', secondary_key)
            search_str = secondary_key.replace(' ', '')
            search_str = search_str.strip()

            for dirName, subdirList, fileList in os.walk(audio_path):
                for fname in fileList:
                    ext = [".mp3", ".wav"]
                    if fname.endswith(tuple(ext)):
                        fullpath = os.path.join(target_root_aud, dirName, fname)

                        idx = fullpath.rfind('/') + 1
                        linefind = fullpath[idx:].replace(' ', '')
                        i = 0
                        for exts in ext:
                            linefind = linefind.replace(ext[i], '')
                            i += 1

                        index = canonical_caseless(linefind).find(canonical_caseless(search_str))
                        if (index != -1):
                            print('file:', fullpath)
        elif audio_active_config_bool == False:
            print('formulaic access to user audio is disabled')
        # primed for a bool set in gui (loop sr or run sr once)
        speechRecognitionThread.stop_sr()


class FindOpenImageClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('plugged in: fileOpenImageClass')
        global image_active_config_bool
        global secondary_key
        global image_configuration
        global speechRecognitionThread

        if image_active_config_bool == True:
            image_path = image_configuration.replace('DIRIMG: ', '')
            target_root_img = str(image_path.split('\\')[0] + '\\')
            print('image directory:', image_path)

            with open(secondary_key_store, 'r') as fo:
                for line in fo:
                    secondary_key = line.strip()
            print('secondary key:', secondary_key)
            search_str = secondary_key.replace(' ', '')
            search_str = search_str.strip()

            for dirName, subdirList, fileList in os.walk(image_path):
                for fname in fileList:
                    ext = [".png", ".jpg"]
                    if fname.endswith(tuple(ext)):
                        fullpath = os.path.join(target_root_img, dirName, fname)

                        idx = fullpath.rfind('/') + 1
                        linefind = fullpath[idx:].replace(' ', '')
                        i = 0
                        for exts in ext:
                            linefind = linefind.replace(ext[i], '')
                            i += 1

                        index = canonical_caseless(linefind).find(canonical_caseless(search_str))
                        if (index != -1):
                            print('file:', fullpath)
        elif image_active_config_bool == False:
            print('formulaic access to user images is disabled')
        # primed for a bool set in gui (loop sr or run sr once)
        speechRecognitionThread.stop_sr()


class FindOpenTextClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('plugged in: fileOpenTextClass')
        global text_active_config_bool
        global secondary_key
        global text_configuration
        global speechRecognitionThread

        if text_active_config_bool == True:
            text_path = text_configuration.replace('DIRTXT: ', '')
            target_root_txt = str(text_path.split('\\')[0] + '\\')
            print('text directory:', text_path)

            with open(secondary_key_store, 'r') as fo:
                for line in fo:
                    secondary_key = line.strip()
            print('secondary key:', secondary_key)
            search_str = secondary_key.replace(' ', '')
            search_str = search_str.strip()

            for dirName, subdirList, fileList in os.walk(text_path):
                for fname in fileList:
                    ext = [".txt"]
                    if fname.endswith(tuple(ext)):
                        fullpath = os.path.join(target_root_txt, dirName, fname)

                        idx = fullpath.rfind('/') + 1
                        linefind = fullpath[idx:].replace(' ', '')
                        i = 0
                        for exts in ext:
                            linefind = linefind.replace(ext[i], '')
                            i += 1

                        index = canonical_caseless(linefind).find(canonical_caseless(search_str))
                        if (index != -1):
                            print('file:', fullpath)
        elif text_active_config_bool == False:
            print('formulaic access to user audio is disabled')
        # primed for a bool set in gui (loop sr or run sr once)
        speechRecognitionThread.stop_sr()


class FindOpenVideoClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('plugged in: fileOpenVideoClass')
        global video_active_config_bool
        global secondary_key
        global video_configuration
        global speechRecognitionThread

        if video_active_config_bool == True:
            video_path = video_configuration.replace('DIRVID: ', '')
            target_root_vid = str(video_path.split('\\')[0] + '\\')
            print('video directory:', video_path)

            with open(secondary_key_store, 'r') as fo:
                for line in fo:
                    secondary_key = line.strip()
            print('secondary key:', secondary_key)
            search_str = secondary_key.replace(' ', '')
            search_str = search_str.strip()

            for dirName, subdirList, fileList in os.walk(video_path):
                for fname in fileList:
                    ext = [".mp4"]
                    if fname.endswith(tuple(ext)):
                        fullpath = os.path.join(target_root_vid, dirName, fname)

                        idx = fullpath.rfind('/') + 1
                        linefind = fullpath[idx:].replace(' ', '')
                        i = 0
                        for exts in ext:
                            linefind = linefind.replace(ext[i], '')
                            i += 1

                        index = canonical_caseless(linefind).find(canonical_caseless(search_str))
                        if (index != -1):
                            print('file:', fullpath)
        elif video_active_config_bool == False:
            print('formulaic access to user video is disabled')
        # primed for a bool set in gui (loop sr or run sr once)
        speechRecognitionThread.stop_sr()


class FindOpenProgramClass(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('plugged in: findOpenProgramClass')
        global secondary_key
        global speechRecognitionThread

        # primed for a bool set in gui (loop sr or run sr once)
        speechRecognitionThread.stop_sr()


class CommandSearchClass(QThread):
    def __init__(self, text_box_verbose,
                 text_box_verbose2,
                 textBoxVerbose2Thread):

        QThread.__init__(self)
        self.text_box_verbose2 = text_box_verbose2
        self.text_box_verbose = text_box_verbose
        self.textBoxVerbose2Thread = textBoxVerbose2Thread

    def __del__(self):
        self.wait()

    def run(self):
        print('plugged in thread: commandSearch')
        global plugin_dir
        global speechRecognitionThread
        global guiControllerThread

        speechRecognitionThread.stop_sr()

        found_plugin = False
        secondary_key = ''
        cur_dir = os.getcwd()
        print('plugin directory:', plugin_dir)

        with open(secondary_key_store, 'r') as fo:
            for line in fo:
                secondary_key = line.strip()
        print('secondary key:', secondary_key)
        search_str = secondary_key.replace(' ', '')
        search_str = search_str.strip()

        for dirName, subdirList, fileList in os.walk(plugin_dir):
            for fname in fileList:
                lnkext = [".py"]
                if fname.endswith(tuple(lnkext)):
                    full_path = os.path.join(cur_dir, dirName, fname)
                    idx = fname.rfind('/') + 1
                    linefind = fname[idx:].replace('.py"', '')
                    if '_' not in linefind:
                        index = canonical_caseless(linefind).find(canonical_caseless(search_str))
                        if (index != -1):
                            found_plugin = True
                            print('found plugin:', full_path)

                            found_sound()

                            cmd = 'python3.5 '+'"'+full_path+'"'
                            print('command:', cmd)
                            xcmd = subprocess.Popen(cmd,
                                                    shell=True,
                                                    stdin=subprocess.PIPE,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
        if found_plugin == False:
            print('plugin not found:', search_str)
            not_found_sound()


sock_con = ()


class SymbiotServerClass(QThread):
    def __init__(self,
                 speechRecognitionThread,
                 symbiot_button,
                 speech_recognition_off_function):

        QThread.__init__(self)
        self.symbiot_button = symbiot_button
        self.speech_recognition_off_function = speech_recognition_off_function

    def run(self):
        global sock_con
        global symbiot_ip_configuration
        global symbiot_mac_configuration

        symbiot_log = './log/symbiot_server.log'
        if not os.path.exists(symbiot_log):
            open(symbiot_log, 'w').close()
        host = ''
        port = ''
        on = 0
        print('plugged in: symbiotServerClass')
        sr_on_message = str('DSFLJdfsdfknsdfDfsdlfDSLfjLSDFjsdfsdfgSDfgG')
        sr_off_message = str('ADfeFArgDHBtHaGafdGagadfaDfgASDfaaDGfadfa')
        s = socket.socket()
        sock_con = s
        sock_con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        with codecs.open(config_file, 'r', encoding="utf-8") as fo:
            for line in fo:
                if line.startswith('SYMBIOT_SERVER: '):
                    host = line.replace('SYMBIOT_SERVER: ', '')
                    host = host.strip()
                    print('symbiot server ip configuration:', host)
                if line.startswith('SYMBIOT_SERVER_PORT: '):
                    port = line.replace('SYMBIOT_SERVER_PORT: ', '')
                    port = port.strip()
                    port = int(port)
                    if port == 0:
                        print('symbiot server port configuration:', port, '/ any available port')
                    else:
                        print('symbiot server port configuration:',port)
                if line.startswith('SYMBIOT_IP: '):
                    symbiot_ip_configuration = line.replace('SYMBIOT_IP: ', '')
                    symbiot_ip_configuration = symbiot_ip_configuration.strip()
                    print('symbiot client ip configuration:', symbiot_ip_configuration)
                if line.startswith('SYMBIOT_MAC: '):
                    symbiot_mac_configuration = line.replace('SYMBIOT_MAC: ', '')
                    symbiot_mac_configuration = symbiot_mac_configuration.strip()
                    print('symbiot client mac configuration:', symbiot_mac_configuration)
        try:
            s.bind((host, port))
            on = 1
            print('symbiot server successfully binded to', s.getsockname()[1])
        except socket.error as msg:
            print('symbiot server failed to bind to', port, '. Error Code : ', msg)
            sock_con.close()
        while on == 1:
            print('symbiot server enabled')
            print('symbiot server listening:')
            s.listen(5)
            try:
                c, addr = s.accept()
                ip = str(addr[0])
                port = str(addr[1])
                client_info = ('ip=' + ip + '  ' + 'port=' + str(port))
                print('client connected: ', client_info)

                cmd = 'arp -a '+ip
                xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                line = xcmd.stdout.readline()
                line = str(line).replace("b'", "")
                line = line.split(' ')
                arp_hostname = line[0]
                arp_ip = line[1].replace('(', '').replace(')', '')
                arp_mac = str(line[3])

                print('arp hostname:', arp_hostname)
                print('arp ip:', arp_ip)
                print('arp mac:', arp_mac)

                gate_1 = False
                gate_2 = False

                if arp_ip == symbiot_ip_configuration:
                    gate_1 = True
                if arp_mac == symbiot_mac_configuration:
                    gate_2 = True

                if (gate_1 == True) and (gate_2 == True):
                    print('symbiot configuration check: client ' + arp_hostname + ' will be accepted')
                    connection_message = c.recv(1024)
                    connection_message = str(connection_message)
                    connection_message = connection_message.strip('\'b')
                    connection_message = connection_message.strip('"')

                    if connection_message == sr_on_message:
                        print('client', addr[0], 'has command-string')
                        print('starting speech recognition thread...')
                        speechRecognitionThread.start()
                    elif connection_message == sr_off_message:
                        print('client', addr[0], 'has command-string')
                        print('stopping speech recognition thread...')
                        self.speech_recognition_off_function()

                elif (gate_1 == False) or (gate_2 == False):
                    print('symbiot configuration check: client ' + arp_hostname + ' will be dropped')

            except ConnectionRefusedError:
                print('target machine actively refused conection...')
            except ConnectionResetError:
                print('an existing connection was forcibly closed by the remote host')
            except OSError:
                print('a connect request was made on an already connected socket')

    def symbiot_server_off(self):
        global sock_con
        sock_con.close()
        self.terminate()


class SpeechRecognitionClass(QThread):
    def __init__(self, sr_indicator,
                 text_box_value,
                 text_box_verbose1,
                 text_box_verbose2,
                 textBoxVerbose2Thread,
                 sr_info,
                 guiControllerThread,
                 commandSearchThread,
                 sr_on_button,
                 sr_off_button,
                 logo_label,
                 dynamic_logo_label):

        QThread.__init__(self)
        self.sr_info = sr_info
        self.text_box_value = text_box_value
        self.guiControllerThread = guiControllerThread
        self.text_box_verbose1 = text_box_verbose1
        self.text_box_verbose2 = text_box_verbose2
        self.textBoxVerbose2Thread = textBoxVerbose2Thread
        self.commandSearchThread = commandSearchThread
        self.sr_indicator = sr_indicator
        self.sr_on_button = sr_on_button
        self.sr_off_button = sr_off_button
        self.logo_label = logo_label
        self.dynamic_logo_label = dynamic_logo_label

    def run(self):
        print('plugged in thread: speechRecognitionThread')
        global secondary_key
        global primary_key
        global value
        global sppid
        r = sr.Recognizer()
        m = sr.Microphone()
        try:
            self.sr_on_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
                color: rgb(100, 255, 0);
                border:1px solid rgb(0, 0, 0);}""")
            self.sr_off_button.setStyleSheet(
                """QPushButton {background-color: rgb(0, 0, 0);
                color: rgb(230, 0, 0);
                border:1px solid rgb(0, 0, 0);}""")
            pixmap = QPixmap('./resources/image/speech_recognition_led_on.png')
            self.sr_indicator.setPixmap(pixmap)
            sr_on_sound_file = './resources/sound/sr_activated_sound.mp3'
            cmd = 'mpg321 ' + sr_on_sound_file
            subprocess.Popen(cmd,
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            self.sr_info.setText("A moment of silence please...")
            with m as source: r.adjust_for_ambient_noise(source)
            self.sr_info.setText("Set minimum energy threshold to {}".format(r.energy_threshold))
            while True:
                self.sr_info.setText("Waiting for command")
                with m as source: audio = r.listen(source)
                self.sr_info.setText("Attempting to recognize audio...")
                try:

                    self.logo_label.hide()
                    self.dynamic_logo_label.show()

                    sr_processing_sound_file = './resources/sound/sr_processing_sound.mp3'
                    cmd = 'mpg321 ' + sr_processing_sound_file
                    subprocess.Popen(cmd,
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

                    value = r.recognize_google(audio)
                    self.text_box_value.setText('Interpretation: ' + value)
                    self.guiControllerThread.start()
                    with codecs.open(secondary_key_store, 'w', encoding='utf-8') as fo:
                        fo.write(value)
                        fo.close()

                    i = 0
                    key_word_check = False
                    for key_words in key_word:
                        if value.startswith(key_word[i]):
                            key_word_length = len(key_word[i])
                            primary_key = key_word[i][:key_word_length]
                            secondary_key = value[key_word_length:]
                            secondary_key = secondary_key.strip()
                            print('Primary Key: ', primary_key)
                            print('Secondary Key: ', secondary_key)
                            if value != primary_key or value == 'stop transcription':
                                with codecs.open(secondary_key_store, 'w', encoding='utf-8') as fo:
                                    fo.write(secondary_key)
                                    fo.close()
                                if primary_key in internal_commands_list:
                                    with codecs.open(primary_key_store, 'w', encoding='utf-8') as fo2:
                                        fo2.write(primary_key)
                                        fo2.close()
                                    execute_funk = internal_commands_list[primary_key]
                                    key_word_check = True
                                    self.dynamic_logo_label.hide()
                                    self.logo_label.show()
                                    execute_funk()
                                else:
                                    key_word_check = False
                            elif value == primary_key:
                                key_word_check = False
                                print('please specify a query')
                        i += 1

                    if key_word_check == False:
                        self.dynamic_logo_label.hide()
                        self.logo_label.show()
                        self.commandSearchThread.start()

                except sr.UnknownValueError:
                    self.dynamic_logo_label.hide()
                    self.logo_label.show()
                    self.sr_info.setText("ignoring background noise...")
                except sr.RequestError as e:
                    self.dynamic_logo_label.hide()
                    self.logo_label.show()
                    self.sr_info.setText("Google Speech Recognition service unavailable...Offline?")
        except KeyboardInterrupt:
            self.dynamic_logo_label.hide()
            self.logo_label.show()
            pass

    def stop_sr(self):
        self.dynamic_logo_label.hide()
        self.logo_label.show()
        self.sr_on_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
            color: rgb(0, 150, 0);
            border:1px solid rgb(0, 0, 0);}""")
        self.sr_off_button.setStyleSheet(
            """QPushButton {background-color: rgb(0, 0, 0);
            color: rgb(255, 0, 0);
            border:1px solid rgb(0, 0, 0);}""")
        pixmap = QPixmap('./resources/image/speech_recognition_led_off.png')
        self.sr_indicator.setPixmap(pixmap)

        sr_off_sound_file = './resources/sound/sr_deactivated_sound.mp3'
        cmd = 'mpg321 ' + sr_off_sound_file
        xcmd = subprocess.Popen(cmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        xcmd.wait()
        xcmd.terminate()
        xcmd.communicate()
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())