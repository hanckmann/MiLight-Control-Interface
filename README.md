# MiLight-Control-Interface

The MiLight Control Interface is a powerful Python API to control MiLight LED bulbs and strips (White and RGBW).

The interface is an implementation of the LimitlessLED v4.0 Wifi Bridge Control Commandset which can be found in the documentation at http://www.limitlessled.com/dev/.

The MiLight Control Interface is accompanied by a simple commandline utility which demonstrates the API.

MiLight products are also known under the name LimitlessLED, and EasyBulb Lamps.

## mci.py

In this file three API's are defined:
- DiscoverBridge
- ColorGroup
- WhiteGroup

### DiscoverBridge

The DiscoverBridge class can be used to discover Wifi Bridges in the local network. It's interface and usage is:

    # Find the Wifi Bridges
    dg = mci.DiscoverBridge(port=48899).discover()
    # Display the found Wifi Bridges
    for (addr, mac) in dg:
        print(' - ip address :' + addr + '\tmac: ' + mac)

Note that the port number should not be changed in normal operation.

### ColorGroup and WhiteGroup

The ColorGroup and WhiteGroup classes can be used to control groups of RGBW and White light bulbs and strips. It's interface is:

- ColorGroup and WhiteGroup
    + Group(ip_address, port=8899, pause=0.1, group_number=None)
    + on()
    + off()
- ColorGroup
    + white()
    + brightness(value=10)
    + disco(mode='')
    + increase_disco_speed(steps=1)
    + decrease_disco_speed(steps=1)
    + color(value)
- WhiteGroup
    + increase_brightness(steps=1)
    + decrease_brightness(steps=1)
    + increase_warmth(steps=1)
    + decrease_warmth(steps=1)
    + brightmode()
    + nightmode()

Note that when creating a group (__init__) the optional arguments 'port' and 'pause' should not be changed in normal operation.

The interface names should be self explanatory, except for:

*brightness(value=10):* sets the brightness of an RGBW lamp to a value between 0 and 25. Input values are rounded to the value closest within the range 0 to 25.

*disco(mode=''):* if no (valid) mode is selected: start the (next) preset disco mode of an RGBW lamp. A number of disco-modes can be started specifically by providing the mode name as argument.
Disco mode can be stopped by providing a color or setting the lamp into white mode.

- supported disco-modes:
    + color change
    + color fade
    + color blink
    + white blink
    + green blink
    + blue blink
    + red blink
    + rainbow
    + disco

*color(value):* sets the color of an RGBW lamp. The following are valid inputs:

- b'\x00' <= value <= b'\xFF', where type(value) == bytes
- 0 <= value <= 255, where type(value) == int
- a color name which can be found in the list below, where type(value) == str
    + violet
    + royalblue
    + lightskyblue
    + aqua
    + aquamarine
    + seagreen
    + green
    + limegreen
    + yellow
    + goldenrod
    + orange
    + red
    + pink
    + fuchsia
    + orchid
    + lavender

## milight.py

Is the commandline utility which shows the MCI API. It can  be used as follows:

    milight.py [-h] [-s] [-i [ADDRESS]] [-p [PORT]] [-c RGBW] [-w WHITE]
               [-a ACTION] [--on] [--off] [--ew] [--br [ACTION_BR]]
               [--cc [ACTION_CC]] [--d] [--id] [--dd] [--ib] [--db] [--iw]
               [--dw] [--b] [--n]
    .
    optional arguments:
      -h, --help            show this help message and exit
      -s, --scan            Search wifi bridges.
      -i [ADDRESS], --ip_address [ADDRESS]
                            IP address.
      -p [PORT], --port [PORT]
                            Port number.
      -c RGBW, --rgbw RGBW  Set RGBW target group, default: None (1, 2, 3, 4, ALL)
      -w WHITE, --white WHITE
                            Set White target group, default: None (1, 2, 3, 4,
                            ALL)
      -a ACTION, --action ACTION
                            The desired action, default: None
                            (for white bulbs/strips: ON, OFF,
                                INC_BRIGHTNESS, DEC_BRIGHTNESS,
                                INC_WARMTH, DEC_WARMTH,
                                BRIGHT_MODE, NIGHT_MODE
                            for rgbw bulbs/strips: ON, OFF,
                                DISCO_MODE, INC_DISCO_SPEED, DEC_DISCO_SPEED)
      --on                  Action: ON
      --off                 Action: OFF
      --ew                  Action (rgbw bulbs/strips only): WHITE
      --br [ACTION_BR]      Action (rgbw bulbs/strips only): set brightness
                             (0<= value <= 25)
      --cc [ACTION_CC]      Action (rgbw bulbs/strips only): set color
                             (int: 0 <=value <= 255)
      --d                   Action (rgbw bulbs/strips only): DISCO_MODE
      --id                  Action (rgbw bulbs/strips only): INC_DISCO_SPEED
      --dd                  Action (rgbw bulbs/strips only): DEC_DISCO_SPEED
      --ib                  Action (white bulbs/strips only): INC_BRIGHTNESS
      --db                  Action (white bulbs/strips only): DEC_BRIGHTNESS
      --iw                  Action (white bulbs/strips only): INC_WARMTH
      --dw                  Action (white bulbs/strips only): DEC_WARMTH
      --b                   Action (white bulbs/strips only): BRIGHT_MODE
      --n                   Action (white bulbs/strips only): NIGHT_MODE

## Finally

It would be great if you can use this for any of your projects, and I would be happy to hear how you used it.

Also feel free to bug me with update/bugfix/feature requests. I will add those if possible.

~~ Patrick