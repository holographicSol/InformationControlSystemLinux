import os
from awake import wol

mac = ''
broadcast_addr = ''
ip_addr_file = './configuration/sony_bravia.conf'

if os.path.isfile(ip_addr_file):
    with open(ip_addr_file, 'r') as fo:
        for line in fo:
            if line.startswith('MAC:'):
                mac = line.strip('MAC: ')
                mac = mac.strip('\n')
            if line.startswith('BA:'):
                broadcast_addr = line.strip('BA: ')
                broadcast_addr = broadcast_addr.strip('\n')
        wol.send_magic_packet(mac, broadcast_addr, port=9)
