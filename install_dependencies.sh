echo "installing python3.5 if neccessary"
sudo apt-get -y install python3.5
echo "installing python3-pip"
sudo apt-get -y install python3-pip
sudo -H python3.5 -m pip install --upgrade pip
echo "installing python3.5 requirements for Information Control System..."
sudo -H python3.5 -m pip install requests
sudo -H python3.5 -m pip install bs4
sudo -H python3.5 -m pip install gtts
sudo -H python3.5 -m pip install SpeechRecognition
sudo -H python3.5 -m pip install PyQt5
sudo -H python3.5 -m pip install webbrowser
sudo -H python3.5 -m pip install awake
sudo -H python3.5 -m pip install wol
sudo -H python3.5 -m pip install wakeonlan
sudo apt-get -y install python-pyaudio python3-pyaudio
sudo apt-get -y install portaudio19-dev python-all-dev python3-all-dev && sudo python3.5 -m pip install pyaudio
python3.5 -m pip install --upgrade pyaudio
sudo apt-get -y install nmap
sudo apt-get -y install mpg321

echo "DONE."
echo
echo "run 'python3.5 -m speech_recognition' to make sure sr is working properly."
echo "run 'python3.5 Information-Control-System.py when your ready'."
