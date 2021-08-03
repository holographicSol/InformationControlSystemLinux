##                GNU General Public License version 3                          ##
##    Sony Bravia Remote by Benjamin Jack Cullen Copyright (C) 2017             ##
##                                                                              ##
##    This program is free software: you can redistribute it and/or modify      ##
##    it under the terms of the GNU General Public License as published by      ##
##    the Free Software Foundation, either version 3 of the License, or         ##
##    (at your option) any later version.                                       ##
##                                                                              ##
##    This program is distributed in the hope that it will be useful,           ##
##    but WITHOUT ANY WARRANTY; without even the implied warranty of            ##
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              ##
##    GNU General Public License for more details.                              ##
##                                                                              ##
##    You should have received a copy of the GNU General Public License         ##
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.     ##

import os
import sys
import requests
import time
import distutils.dir_util
import subprocess
import re
import codecs
from pathlib import Path
from awake import wol
from subprocess import Popen, CREATE_NEW_CONSOLE
import shutil
import fileinput

cur_dir = os.getcwd()
list_dir = os.listdir(os.getcwd())

#Path to Configuration Files
ip_addr_file = 'sony_bravia.conf'

#Subprocess Arguments
info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0

#IP address to displaed on print_menu()
def ip_address():
    if os.path.isfile(ip_addr_file):
        fip = codecs.open(ip_addr_file, 'r', encoding="utf-8")
        for line in fip:
            if line.startswith('IP: '):
                line = line.replace('IP: ', '')
                url = ("http://"+line+"/sony/IRCC")
                print(url)
    else:
        print("TV IPv4: Unconfigured")

#MAC address to print_menu()
def mac_address():
    if os.path.isfile(ip_addr_file):
        fmac = open(ip_addr_file, 'r')
        for line in fmac:
            if line.startswith('MAC: '):
                line = line.replace('MAC: ', '')
                print(line)
                mac = line.split()

    else:
        print("TV MAC: Unconfigured")

#Help Menu
def help_menu():
    print("")
    print(28 * "-", "HELP", 28 * "-")
    print("")
    print("Welcome to Sony Bravia CLI/Voice WiFi Remote!")
    print("")
    print("This is a wifi remote for the Sony Bravia Smart Tv.")
    print("You can control the sonybravia via this CLI application & by voice command.")
    print("")
    print("Select a menu number between 1-37 in the main menu.")
    print("")
    print("Volume Control increments of 1 to 10 Example: 3 5\nincreases the volume by 5.")
    print("")
    print("Cursor Control increments of 1 to 5 Example: 3 5\nmoves cursor 5 spaces.")
    print("")
    print("You can activate Voice Control by pressing V at any time.")
    print("")
    print("Sony Bravia CLI/Voice Remote written by Benjamin Jack Cullen 2017.")
    print("Beta 1.1")
    print("")
    goBack = input("Press B to go back: ")
    if goBack == "b":
        print_menu()
    else:
        help_menu()


#Print_Menu_Config
def print_config_menu():
    print(62 * "-")
    print(21 * " ", "Configuration Options", 21 * " ")
    print("")
    print("1. Enter Sony Bravia IP Address.")
    print("2. Enter Sony Bravia MAC Address.")
    print("3. Enter Sony Bravia Broadcast Address.")
    print("")
    print("4. Create A New Profile.")
    print("")
    print("3. Press B to Go Back")
    print("")
    selection = input("Select option: ")
    if selection == "1":
        config_1()
    if selection == "2":
        config_2()
    if selection=="3":
        config_3()
    if selection=="4":
        config_4()
    elif selection=="b":
        print_menu()
    else:
        print("INVALID OPTION")
        print_config_menu()

#Configuration Option 1. IP
def config_1():
    print(21 * " ", "SET IP OF TV", 21 * " ")
    print("")
    print("Please enter the IPv4 address of the\nSony Bravia Smart TV you wish to control.")
    print("")
    ip = input("Enter IP: ")
    print(ip)
    if len(ip) in range(7, 15):
        if re.match("[A-Za-z0-9.]*$", ip):
            f = open(ip_addr_file, 'w')
            f.write(ip)
            f.close()
            print("TV IP Address Set To:", ip)
        else:
            print("INVALID")
            config_1()
    else:
        print("INVALID")
        config_1()

#Configuration Option 2. MAC
def config_2():
    print(21 * " ", "SET MAC OF TV", 21 * " ")
    print("")
    print("Please enter the MAC address of the\nSony Bravia Smart TV you wish to control.")
    print("")
    mac = input("Enter MAC: ")
    print(mac)
    if len(mac) == 17:
        if re.match("[A-Za-z0-9:]*$", mac):
            f = open(ip_addr_file, 'a')
            x = f.write('"'+mac+'"')
            f.close()
            print("TV MAC Set To:", mac)
        else:
            print("INVALID")
            config_2()
    else:
        print("INVALID")
        config_2()

#Configuration Option 3. Broadcast Address
def config_3():
    print(21 * " ", "SET BROADCAST ADDRESS OF TV", 21 * " ")
    print("")
    print("Please enter the broadcast address of the\nSony Bravia Smart TV you wish to control.")
    print("This is usually 192.168.0.255.")
    print("")
    print("")
    broadcast_address = input("Enter Broadcast Address: ")
    print(broadcast_address)
    if len(broadcast_address) in range(7, 15):
        if re.match("[A-Za-z0-9.]*$", broadcast_address):
            f = open(ip_addr_file, 'a')
            x = f.write(broadcast_address)
            f.close()
            print("TV BROADCAST ADDRESS Set To:", broadcast_address)
        else:
            print("INVALID")
            config_3()
    else:
        print("INVALID")
        config_3()

#Configuration Option 4. Create A New Profile (Remote Creation allows for infinite remotes to be used simultaniously).
def config_4():
    print(21 * " ", "Nickname Your TV", 21 * " ")
    print("")

    #Nick Name
    nick_name = input("Enter Nickname: ")
    if len(nick_name) in range(1, 50):
        if re.match("[A-Za-z0-9]*$", nick_name):

            #Check if profile dir exists
            cur_dir = os.getcwd()
            if os.path.exists(cur_dir+'\\'+nick_name):
                print("Profile Name Already Exists")
                config_4()
            else:
                distutils.dir_util.mkpath(nick_name)
                print("New Profile Name Set To:", nick_name)

                #IP
                ip = input("Enter IP: ")
                if len(ip) in range(7, 15):
                    if re.match("[A-Za-z0-9.]*$", ip):
                        fname = (nick_name+'.conf')
                        custom_conf = fname
                        f = open(cur_dir+'\\'+nick_name+'\\'+fname, 'w')
                        f.write('IP: '+ip+'\n')
                        f.close()
                        print("TV IP Address Set To:", ip)

                        #MAC
                        print(21 * " ", "SET MAC OF TV", 21 * " ")
                        print("")
                        print("Please enter the MAC address of the\nSony Bravia Smart TV you wish to control.")
                        print("")
                        mac = input("Enter MAC: ")
                        print(mac)
                        if len(mac) == 17:
                            if re.match("[A-Za-z0-9:]*$", mac):
                                fname = (custom_conf)
                                f = open(cur_dir+'\\'+nick_name+'\\'+fname, 'a')
                                x = f.write('MAC: '+mac+'\n')
                                f.close()
                                print("TV MAC Set To:", mac)

                                #Broadcast
                                print(21 * " ", "SET BROADCAST ADDRESS OF TV", 21 * " ")
                                print("")
                                print("Please enter the broadcast address of the\nSony Bravia Smart TV you wish to control.")
                                print("This is usually 192.168.0.255.")
                                print("")
                                print("")
                                broadcast_address = input("Enter Broadcast Address: ")
                                print(broadcast_address)
                                if len(broadcast_address) in range(7, 15):
                                    if re.match("[A-Za-z0-9.]*$", broadcast_address):
                                        fname = (custom_conf)
                                        f = open(cur_dir+'\\'+nick_name+'\\'+fname, 'a')
                                        x = f.write('BA: '+broadcast_address+'\n')
                                        f.close()
                                        print("TV BROADCAST ADDRESS Set To:", broadcast_address)

                                        #Copy files to new Profile Directory
                                        for root, dirs, files in os.walk('.', topdown=True):
                                            dirs.clear()
                                            for file in files:
                                                x = "sonybravia"
                                                if file.startswith(x):
                                                    shutil.copy(file, nick_name)
                                                    time.sleep(0.1)
                                                else:
                                                    pass

                                        #Change dir to new profile dir and preappend file names with Unique Nickname
                                        for root, dirs, files in os.walk(nick_name, topdown=True):
                                            for file in files:
                                                x = "sonybravia"
                                                if file.startswith(x):
                                                    new_name = (nick_name+file)
                                                    new_name = new_name.replace('sonybravia', '')
                                                    os.chdir(cur_dir+'\\'+nick_name)
                                                    os.rename(file, new_name)
                                                else:
                                                    pass

                                        # Refactor each new file to point at new custom config file
                                        cur_dir = os.getcwd()
                                        print('current working dir:',cur_dir)
                                        for dirName, subdirList, fileList in os.walk('./'):
                                            for fname in fileList:
                                                print(fname)
                                                filein = (fname)
                                                for line in fileinput.input(filein, inplace=True):
                                                    print (line.rstrip().replace('sony_bravia', nick_name)),
                                                    
                                        # Refactor each command file to point at new command files
                                        cur_dir = os.getcwd()
                                        print('current working dir:',cur_dir)
                                        for dirName, subdirList, fileList in os.walk('./'):
                                            for fname in fileList:
                                                print(fname)
                                                filein = (fname)
                                                for line in fileinput.input(filein, inplace=True):
                                                    print (line.rstrip().replace('sonybravia', nick_name)),
                                                    
                                    else:
                                        print("INVALID")
                                        config_4()
                                else:
                                    print("INVALID")
                                    config_4()

                            else:
                                print("INVALID")
                                config_4()
                        else:
                            print("INVALID")
                            config_4()

                    else:
                        print("INVALID")
                        config_4()
                else:
                    print("INVALID")
                    config_4()

        else:
            print("INVALID")
            config_4()
    else:
        print("INVALID")
        config_4()

#Turn on
def turn_on():
    cmd = ("python "+"sonybraviaturnon.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Turn off
def turn_off():
    cmd = ("python "+"sonybraviaturnoff.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Volume Up
def volume_up_1():
    cmd = ("python "+"sonybraviavolumeupone.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_2():
    cmd = ("python "+"sonybraviavolumeuptwo.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_3():
    cmd = ("python "+"sonybraviavolumeupthree.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_4():
    cmd = ("python "+"sonybraviavolumeupfour.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_5():
    cmd = ("python "+"sonybraviavolumeupfive.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_6():
    cmd = ("python "+"sonybraviavolumeupsix.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_7():
    cmd = ("python "+"sonybraviavolumeupseven.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_8():
    cmd = ("python "+"sonybraviavolumeupeight.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_9():
    cmd = ("python "+"sonybraviavolumeupnine.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_up_10():
    cmd = ("python "+"sonybraviavolumeupten.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Volume Down
def volume_down_1():
    cmd = ("python "+"sonybraviavolumedownone.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_2():
    cmd = ("python "+"sonybraviavolumedowntwo.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_3():
    cmd = ("python "+"sonybraviavolumedownthree.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_4():
    cmd = ("python "+"sonybraviavolumedownfour.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_5():
    cmd = ("python "+"sonybraviavolumedownfive.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_6():
    cmd = ("python "+"sonybraviavolumedownsix.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_7():
    cmd = ("python "+"sonybraviavolumedownseven.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_8():
    cmd = ("python "+"sonybraviavolumedowneight.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_9():
    cmd = ("python "+"sonybraviavolumedownnine.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def volume_down_10():
    cmd = ("python "+"sonybraviavolumedownten.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Mute
def mute():
    cmd = ("python "+"sonybraviamute.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Movement Left
def move_left_1():
    cmd = ("python "+"sonybraviacursorleftone.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_left_2():
    cmd = ("python "+"sonybraviacursorlefttwo.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_left_3():
    cmd = ("python "+"sonybraviacursorleftthree.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_left_4():
    cmd = ("python "+"sonybraviacursorleftfour.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_left_5():
    cmd = ("python "+"sonybraviacursorleftfive.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Movement Down
def move_down_1():
    cmd = ("python "+"sonybraviacursordownone.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_down_2():
    cmd = ("python "+"sonybraviacursordowntwo.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_down_3():
    cmd = ("python "+"sonybraviacursordownthree.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_down_4():
    cmd = ("python "+"sonybraviacursordownfour.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_down_5():
    cmd = ("python "+"sonybraviacursordownfive.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Movement Right
def move_right_1():
    cmd = ("python "+"sonybraviacursorrightone.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_right_2():
    cmd = ("python "+"sonybraviacursorrighttwo.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_right_3():
    cmd = ("python "+"sonybraviacursorrightthree.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_right_4():
    cmd = ("python "+"sonybraviacursorrightfour.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_right_5():
    cmd = ("python "+"sonybraviacursorrightfive.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Movement Up
def move_up_1():
    cmd = ("python "+"sonybraviacursorupone.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_up_2():
    cmd = ("python "+"sonybraviacursoruptwo.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_up_3():
    cmd = ("python "+"sonybraviacursorupthree.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_up_4():
    cmd = ("python "+"sonybraviacursorupfour.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def move_up_5():
    cmd = ("python "+"sonybraviacursorupfive.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Channel
def channel_down_1():
    cmd = ("python "+"sonybraviachanneldown.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def channel_up_1():
    cmd = ("python "+"sonybraviachannelup.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def previous_channel():
    cmd = ("python "+"sonybraviapreviouschannel.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Options
def display():
    cmd = ("python "+"sonybraviadisplay.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def guide():
    cmd = ("python "+"sonybraviaguide.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def pop_up_menu():
    cmd = ("python "+"sonybraviapoppmenu.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def func_red():
    cmd = ("python "+"sonybraviafunctionred.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def func_yellow():
    cmd = ("python "+"sonybraviafunctionyellow.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def func_green():
    cmd = ("python "+"sonybraviafunctiongreen.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def func_blue():
    cmd = ("python "+"sonybraviafunctionblue.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def go_3d():
    cmd = ("python "+"sonybravia3d.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def subtitles():
    cmd = ("python "+"sonybraviasubtitles.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def sonybravia_help_menu():
    cmd = ("python "+"sonybraviahelp.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def options():
    cmd = ("python "+"sonybraviaoptions.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def toggle_input():
    cmd = ("python "+"sonybraviainput.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def go_wide():
    cmd = ("python "+"sonybraviawideScreen.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def sony_entertainment_network():
    cmd = ("python "+"sonybraviasonyentertainmentnetwork.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def sync_menu():
    cmd = ("python "+"sonybraviasyncmenu.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Play/Pause
def play():
    cmd = ("python "+"sonybraviaplay.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def stop():
    cmd = ("python "+"sonybraviastop.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def pause():
    cmd = ("python "+"sonybraviapause.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def forward():
    cmd = ("python "+"sonybraviaforward.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def reverse():
    cmd = ("python "+"sonybraviareverse.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def previous():
    cmd = ("python "+"sonybraviaprevious.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def go_next():
    cmd = ("python "+"sonybravianext.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def forward():
    cmd = ("python "+"sonybraviaforward.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def select():
    cmd = ("python "+"sonybraviaselect.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def menu_home():
    cmd = ("python "+"sonybraviamenu.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def sonybravia_exit():
    cmd = ("python "+"sonybraviaexit.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)
def sonybravia_return():
    cmd = ("python "+"sonybraviareturn.py")
    print(cmd)
    subprocess.Popen(cmd, shell=True, creationflags=subprocess.SW_HIDE)

#Text menu in Python
def print_menu():
    print (21 * "-" , "Sony Bravia Remote" , 21 * "-")
    print("")
    print("TV Configuration:")
    ip_address()
    mac_address()
    print("")
    print ("1. Turn On             11. Left 1-5          21. Func. Green")
    print ("2. Turn Off            12. Select            22. Func.Blue")
    print ("3. Volume Up 1-10      13. Menu Home         23. Go 3D")
    print ("4. Volume Down 1-10    14. Exit              24. Subtitles")
    print ("5. Toggle Mute         15. Return            25. Previous Ch.")
    print ("6. Ch. Down            16. Display           26. Show Help")
    print ("7. Ch. Up              17. Show Guide        27. Options")
    print ("8. Move Up 1-5         18. Pop Up menu       28. Toggle Input")
    print ("9. Move Down 1-5       19. Func. Red         29. Go Wide")
    print ("10.Move Right 1-5      20. Func. Yelllow")
    print("")
    print("30. Sony Entertainment Network")
    print("")
    print ("31. Pause           32. Play             33. Stop")
    print ("34. Forward         35. Reverse          36. Next")
    print("37. Sync Menu")
    print("")
    print("")
    print("Press V To activate Voice Remote.")
    print("Press S To Switch To Another Remote.")
    print("Press C for configuration options.")
    print("Press Q to exit.                          Press H For Manual.")
    print (62 * "-")

#Select Profile Menu
def profile_menu():
    print("")
    print("")
    print("")
    profile = input("Please select a Profile :")
    print_menu()


loop=True
#Loop until loop = Fasle
while loop:
    print_menu()
    choice = input("Select [1-37]: ")

    #On & Off
    if choice==("1"):
        turn_on()
    if choice=="2":
        turn_off()

    #Volume & Mute
    if choice=="3":
        volume_up_1()
    if choice=="3 2":
        volume_up_2()
    if choice=="3 3":
        volume_up_3()
    if choice=="3 4":
        volume_up_4()
    if choice=="3 5":
        volume_up_5()
    if choice=="3 6":
        volume_up_6()
    if choice=="3 7":
        volume_up_7()
    if choice=="3 8":
        volume_up_8()
    if choice=="3 9":
        volume_up_9()
    if choice=="3 10":
        volume_up_10()
    if choice=="4":
        volume_down_1()
    if choice=="4 2":
        volume_down_2()
    if choice=="4 3":
        volume_down_3()
    if choice=="4 4":
        volume_down_4()
    if choice=="4 5":
        volume_down_5()
    if choice=="4 6":
        volume_down_6()
    if choice=="4 7":
        volume_down_7()
    if choice=="4 8":
        volume_down_8()
    if choice=="4 9":
        volume_down_9()
    if choice=="4 10":
        volume_down_10()
    if choice=="5":
        mute()

    #Channel
    if choice=="6":
        channel_down_1()
    if choice=="7":
        channel_up_1()

    #Move Up Increments
    if "8" == choice:
        move_up_1()
    if "8 2" == choice:
        move_up_2()
    if "8 3" == choice:
        move_up_3()
    if "8 4" == choice:
        move_up_4()
    if "8 5" == choice:
        move_up_5()

    #Move Down Increments
    if "9" == choice:
        move_down_1()
    if "9 2" == choice:
        move_down_2()
    if "9 3" == choice:
        move_down_3()
    if "9 4" == choice:
        move_down_4()
    if "9 5" == choice:
        move_down_5()

    #Move Right in Increments
    if "10" == choice:
        move_right_1()
    if "10 2" == choice:
        move_right_2()
    if "10 3" == choice:
        move_right_3()
    if "10 4" == choice:
        move_right_4()
    if "10 5" == choice:
        move_right_5()

    #Move Left in Increments.
    if "11" == choice:
        move_left_1()
    if "11 2" == choice:
        move_left_2()
    if "11 3" == choice:
        move_left_3()
    if "11 4" == choice:
        move_left_4()
    if "11 5" == choice:
        move_left_5()

    #Select
    if choice=="12":
        select()

    #Menu Home
    if choice=="13":
        menu_home()

    #TV Exit
    if choice=="14":
        sonybravia_exit()

    #Return ##########
    if choice=="15":
        sonybravia_return()

    #Display
    if choice=="16":
        display()

    #Show Guide
    if choice=="17":
        show_guide()

    #Pop Up Menu
    if choice=="18":
        pop_up_menu()

    #Function Buttons
    if choice=="19":
        func_red()
    if choice=="20":
        func_yellow()
    if choice=="21":
        func_green()
    if choice=="22":
        func_blue()

    #Go 3D
    if choice=="23":
        go_3d()

    #Subtitles
    if choice=="24":
        subtitles()

    #Previous Channel
    if choice=="25":
        previous_channel()

    #Help
    if choice=="26":
        sonybravia_help_menu()

    #Options
    if choice=="27":
        options()

    #Input
    if choice=="28":
        toggle_input()

    #Go Wide
    if choice=="29":
        go_wide()

    #Sony Entertainment Network
    if choice=="30":
        sony_entertainment_network()

    #Pause
    if choice=="31":
        pause()

    #Play
    if choice=="32":
        play()

    #Stop
    if choice=="33":
        stop()

    #Forward
    if choice=="34":
        forward()

    #Reverse
    if choice=="35":
        reverse()

    #Next
    if choice=="36":
        go_next()

    #Previous
    if choice=="36":
        previous()

    #Sync Menu
    if choice=="37":
        sync_menu()

    #Start Sony Bravia Smart TV Voice Control
    if choice==("v"):
        activate_voice_control()

    #Configuration Menu
    if choice==("c"):
        print_config_menu()

    #Help Menu & Credits
    if choice=="h":
        help_menu()
    #Quit
    if choice==("q"):
        loop=False
    #Else Invalid Option. Re-print menu
    else:
        print(choice)
        print_menu()
