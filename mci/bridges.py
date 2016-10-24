# -*- coding: utf-8 -*-
""" MiLight Control Interface - Discover Bridge

A powerful Python API to control your MiLight LED bulbs and strips (White and RGBW).
Based on the documentation from http://www.limitlessled.com/dev/
"""

import socket


class DiscoverBridge(object):
    """ WIFI Bridge Auto Discovery

    - Step 1:Send UDP message to the LAN broadcast IP address and port 48899 => "Link_Wi-Fi"
    - All Wifi bridges on the LAN will respond with their details. Response is "10.10.100.254, ACCF232483E8"
    """

    def __init__(self, port=48899, wait_time=5):
        """ init """
        self.port = port
        self.wait_time = wait_time

    def discover(self):
        """ Start discovery """
        bufferSize = 1024
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        sock.settimeout(self.wait_time)
        sock.sendto(b"Link_Wi-Fi", ("<broadcast>", self.port))
        found = list()
        try:
            message = sock.recv(bufferSize)
            lst = message.decode('utf-8').split(',')
            if not len(lst) % 2:  # should be odd since the string ends with a ','
                print('return values false')
            for i in range(0, int(len(lst)/2)):
                index = i*2
                found.append((lst[index], lst[index + 1]))
        except socket.timeout:
            print("No server found")
        sock.close()
        return found
