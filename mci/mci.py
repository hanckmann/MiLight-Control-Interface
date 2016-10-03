# -*- coding: utf-8 -*-
""" MiLight Control Interface

A powerful Python API to control your MiLight LED bulbs and strips (White and RGBW).
Based on the documentation from http://www.limitlessled.com/dev/
"""

import socket
import time


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


class Group(object):
    """ Common functions for bulb/strip groups """

    def ___init___(self, ip_address, port=8899, pause=0.1, group_number=None):
        """ init """
        self.ip_address = ip_address
        self.port = port
        if pause <= 0:
            pause = 0.1
        self.pause = pause
        if str(group_number) in ['1', '2', '3', '4']:
            self.group = str(group_number)
        else:
            self.group = 'ALL'
        self._brightness = None
        self._warmth = None
        self.last_command_time = time.time()

    def send_command(self, command, byte2=b"\x00", byte3=b"\x55"):
        """ Send command to the wifi-bridge """
        if command is None:
            return
        current_pause = time.time() - self.last_command_time
        if current_pause < self.pause:
            # Lights require time between commands, 100ms is recommended by the documentation
            time.sleep(self.pause - current_pause)
        self.last_command_time = time.time()
        command += byte2
        command += byte3

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(command, (self.ip_address, self.port))
        sock.close()
        return command

    def on(self):
        """ Switch group on """
        self.send_command(self.GROUP_ON[self.group])

    def off(self):
        """ Switch group off """
        self.send_command(self.GROUP_OFF[self.group])


class ColorGroup(Group):
    """ A group of RGBW color bulbs/strips """

    # Standard ON/OFF
    RGBW_ALL_ON = (66).to_bytes(1, byteorder='big')
    RGBW_ALL_OFF = (65).to_bytes(1, byteorder='big')
    GROUP_1_ON = (69).to_bytes(1, byteorder='big')
    GROUP_1_OFF = (70).to_bytes(1, byteorder='big')
    GROUP_2_ON = (71).to_bytes(1, byteorder='big')
    GROUP_2_OFF = (72).to_bytes(1, byteorder='big')
    GROUP_3_ON = (73).to_bytes(1, byteorder='big')
    GROUP_3_OFF = (74).to_bytes(1, byteorder='big')
    GROUP_4_ON = (75).to_bytes(1, byteorder='big')
    GROUP_4_OFF = (76).to_bytes(1, byteorder='big')

    GROUP_ON = {
        'ALL': RGBW_ALL_ON,
        '1': GROUP_1_ON,
        '2': GROUP_2_ON,
        '3': GROUP_3_ON,
        '4': GROUP_4_ON
    }
    GROUP_OFF = {
        'ALL': RGBW_ALL_OFF,
        '1': GROUP_1_OFF,
        '2': GROUP_2_OFF,
        '3': GROUP_3_OFF,
        '4': GROUP_4_OFF
    }

    # Set to WHITE
    RGBW_ALL_TO_WHITE = (194).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    GROUP_1_TO_WHITE = (197).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    GROUP_2_TO_WHITE = (199).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    GROUP_3_TO_WHITE = (201).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    GROUP_4_TO_WHITE = (203).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON

    GROUP_WHITE = {
        'ALL': RGBW_ALL_TO_WHITE,
        '1': GROUP_1_TO_WHITE,
        '2': GROUP_2_TO_WHITE,
        '3': GROUP_3_TO_WHITE,
        '4': GROUP_4_TO_WHITE
    }

    # Set BRIGHTNESS
    # Byte2: 0×02 to 0x1B (decimal range: 2 to 27) full brightness 0x1B (decimal 27)
    BRIGHTNESS = (78).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON

    # Set to DISCO
    DISCO_MODE = (77).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    DISCO_SPEED_SLOWER = (67).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    DISCO_SPEED_FASTER = (68).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON

    # Specials disco
    DISCO_CODE = b"\x42\x00\x40\x40\x42\x00\x4e\x02"
    DISCO_CODES = {
        "RAINBOW": b"\x4d\x00" * 1,
        "WHITE BLINK": b"\x4d\x00" * 2,
        "COLOR FADE": b"\x4d\x00" * 3,
        "COLOR CHANGE": b"\x4d\x00" * 4,
        "COLOR BLINK": b"\x4d\x00" * 5,
        "RED BLINK": b"\x4d\x00" * 6,
        "GREEN BLINK": b"\x4d\x00" * 7,
        "BLUE BLINK": b"\x4d\x00" * 8,
        "DISCO": b"\x4d\x00" * 9
    }

    # Set COLOR
    # Byte2: 0×00 to 0xFF (255 colors) = COLOR_CODE
    COLOR = (64).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    COLOR_CODES = {
        "VIOLET": b"\x00",
        "ROYALBLUE": b"\x10",
        "LIGHTSKYBLUE": b"\x20",
        "AQUA": b"\x30",
        "AQUAMARINE": b"\x40",
        "SEAGREEN": b"\x50",
        "GREEN": b"\x60",
        "LIMEGREEN": b"\x70",
        "YELLOW": b"\x80",
        "GOLDENROD": b"\x90",
        "ORANGE": b"\xA0",
        "RED": b"\xB0",
        "PINK": b"\xC0",
        "FUCHSIA": b"\xD0",
        "ORCHID": b"\xE0",
        "LAVENDER": b"\xF0"
    }

    def __init__(self, ip_address, port=8899, pause=0.1, group_number=None):
        """ init """
        super().___init___(ip_address, port, pause, group_number)

    def white(self):
        """ Switch to white """
        self.send_command(self.GROUP_WHITE[self.group])

    def brightness(self, value=10):
        """ Set brightness level (0 <= value <= 25) """
        value += 2                      # value should be between 0 and 25
        value = max(2, min(27, value))  # value should be between 2 and 27
        self.on()
        self.send_command(self.BRIGHTNESS, (value).to_bytes(1, byteorder='big'))

    def disco(self, mode=''):
        """ Enable disco mode, if no valid mode is provided the default disco mode is started """
        self.on()
        if mode.upper() in self.DISCO_CODES:
            command = self.DISCO_CODE + self.DISCO_CODES[mode.upper()]
            self.send_command(command, byte2=b"", byte3=b"")
        else:
            self.send_command(self.DISCO_MODE)

    def increase_disco_speed(self, steps=1):
        """ Increase disco_speed (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.DISCO_SPEED_FASTER)

    def decrease_disco_speed(self, steps=1):
        """ Decrease disco_speed (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.DISCO_SPEED_SLOWER)

    def color(self, value):
        """ Set color """
        self.on()
        colorcode = None
        try:
            cvalue = int(value)
            value = cvalue
        except:
            pass
        if type(value) is bytes:
            if len(value) == 1:
                colorcode = value
            else:
                ValueError('The requested color value in bytes should be between x00 and xFF (= 1 byte), received ' + len(value) + ' bytes')
        elif type(value) is int:
            value = max(0, min(255, value))  # value should be between 0 and 255
            colorcode = (value).to_bytes(1, byteorder='big')
        elif type(value) is str:
            if value.upper() in self.COLOR_CODES:
                colorcode = self.COLOR_CODES[value.upper()]
            else:
                ValueError('The requested color as string should be valid (see self.COLOR_CODES)')
        else:
            raise ValueError('Invalid color requested (supported types: byte, integer, string)')
        if colorcode is not None:
            self.send_command(self.COLOR, colorcode)
        else:
            raise ValueError('Invalid color requested (unspecified error, value-type: ' + str(type(value)) + ')')

    def disco_codes(self):
        """ return the disco-codes """
        return [c for c in self.DISCO_CODES.keys()]

    def color_codes(self):
        """ return the color-codes """
        return [c for c in self.COLOR_CODES.keys()]


class WhiteGroup(Group):
    """ A group of white bulbs/strips """

    # Standard ON/OFF
    WHITE_ALL_ON = (53).to_bytes(1, byteorder='big')
    WHITE_ALL_OFF = (57).to_bytes(1, byteorder='big')
    GROUP_1_ON = (56).to_bytes(1, byteorder='big')
    GROUP_1_OFF = (59).to_bytes(1, byteorder='big')
    GROUP_2_ON = (61).to_bytes(1, byteorder='big')
    GROUP_2_OFF = (51).to_bytes(1, byteorder='big')
    GROUP_3_ON = (55).to_bytes(1, byteorder='big')
    GROUP_3_OFF = (58).to_bytes(1, byteorder='big')
    GROUP_4_ON = (50).to_bytes(1, byteorder='big')
    GROUP_4_OFF = (54).to_bytes(1, byteorder='big')

    GROUP_ON = {
        'ALL': WHITE_ALL_ON,
        '1': GROUP_1_ON,
        '2': GROUP_2_ON,
        '3': GROUP_3_ON,
        '4': GROUP_4_ON
    }
    GROUP_OFF = {
        'ALL': WHITE_ALL_OFF,
        '1': GROUP_1_OFF,
        '2': GROUP_2_OFF,
        '3': GROUP_3_OFF,
        '4': GROUP_4_OFF
    }

    # Standard BRIGHTNESS/WHITE-COLOR
    BRIGHTNESS_UP = (60).to_bytes(1, byteorder='big')
    BRIGHTNESS_DOWN = (52).to_bytes(1, byteorder='big')
    WARM_WHITE_INCREASE = (62).to_bytes(1, byteorder='big')
    COOL_WHITE_INCREASE = (63).to_bytes(1, byteorder='big')

    # Specials FULL_BRIGHTNESS/NIGHT_MODE
    FULL_BRIGHTNESS_ALL = (181).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    FULL_BRIGHTNESS_GROUP_1 = (184).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    FULL_BRIGHTNESS_GROUP_2 = (189).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    FULL_BRIGHTNESS_GROUP_3 = (183).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    FULL_BRIGHTNESS_GROUP_4 = (178).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
    # send 100ms after GROUP_OFF
    NIGHT_MODE_ALL = (185).to_bytes(1, byteorder='big')
    NIGHT_MODE_GROUP_1 = (187).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF
    NIGHT_MODE_GROUP_2 = (179).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF
    NIGHT_MODE_GROUP_3 = (186).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF
    NIGHT_MODE_GROUP_4 = (182).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF

    FULL_BRIGHTNESS = {  # send 100ms after GROUP_ON
        'ALL': FULL_BRIGHTNESS_ALL,
        '1': FULL_BRIGHTNESS_GROUP_1,
        '2': FULL_BRIGHTNESS_GROUP_2,
        '3': FULL_BRIGHTNESS_GROUP_3,
        '4': FULL_BRIGHTNESS_GROUP_4
    }
    NIGHT_MODE = {  # send 100ms after GROUP_OFF
        'ALL': NIGHT_MODE_ALL,
        '1': NIGHT_MODE_GROUP_1,
        '2': NIGHT_MODE_GROUP_2,
        '3': NIGHT_MODE_GROUP_3,
        '4': NIGHT_MODE_GROUP_4
    }

    def __init__(self, ip_address, port=8899, pause=0.1, group_number=None):
        """ init """
        super().___init___(ip_address, port, pause, group_number)

    def increase_brightness(self, steps=1):
        """ Increase brightness (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.BRIGHTNESS_UP)

    def decrease_brightness(self, steps=1):
        """ Decrease brightness (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.BRIGHTNESS_DOWN)

    def increase_warmth(self, steps=1):
        """ Increase warmth (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.WARM_WHITE_INCREASE)

    def decrease_warmth(self, steps=1):
        """ Decrease warmth (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.COOL_WHITE_INCREASE)

    def brightmode(self):
        """ Enable full brightness """
        self.on()
        self.send_command(self.FULL_BRIGHTNESS[self.group])

    def nightmode(self):
        """ Enable nightmode """
        self.off()
        self.send_command(self.NIGHT_MODE[self.group])
