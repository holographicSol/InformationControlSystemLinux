import os
import requests

ip_addr_file = './configuration/sony_bravia.conf'

headers = {  
    'User-Agent': 'TVSideView/2.0.1 CFNetwork/672.0.8 Darwin/14.0.0',
    'Content-Type': 'text/xml; charset=UTF-8',
    'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}
commandNext = """<?xml version="1.0"?>  
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">  
  <s:Body>
    <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
      <IRCCCode>AAAAAgAAAJcAAAA9Aw==</IRCCCode>
    </u:X_SendIRCC>
  </s:Body>
</s:Envelope>"""

ip_addr = ''
if os.path.isfile(ip_addr_file):
    with open(ip_addr_file, 'r') as fo:
        for line in fo:
            if line.startswith('IP:'):
                ip_addr = line.strip('IP: ')
                ip_addr = ip_addr.strip('\n')
        url = ("http://"+ip_addr+"/sony/IRCC")
        response = requests.post(url, data=commandNext, headers=headers)
