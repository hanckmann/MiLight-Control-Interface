#!/usr/bin/python
# -*- coding: utf-8 -*-
""" MiLight Commandline Interface """

import argparse
import mci.bridges
import mci.bulbs
import mci.mci_parser


def main():
    """ Main. """
    # Parse commandline arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--scan', action='store_true', dest='scan',
                           help='Search wifi bridges.', default=False, required=False)

    argparser.add_argument('-i', '--ip_address', action='store', nargs=1, dest='address',
                           help='IP address.', default='192.168.0.230', required=False, type=str)
    argparser.add_argument('-p', '--port', action='store', nargs=1, dest='port',
                           help='Port number.', default=8899, required=False, type=int)

    argparser.add_argument('-c', '--rgbw', action='store', nargs=1, dest='rgbw',
                           help='Set RGBW target group, default: None (1, 2, 3, 4, ALL)', default=None, required=False)
    argparser.add_argument('-w', '--white', action='store', nargs=1, dest='white',
                           help='Set White target group, default: None (1, 2, 3, 4, ALL)', default=None, required=False)

    argparser.add_argument('-a', '--action', action='store', nargs='*', dest='action',
                           help='The desired action, default: None (for white bulbs/strips: ON, OFF, INC_BRIGHTNESS, DEC_BRIGHTNESS, INC_WARMTH, DEC_WARMTH, BRIGHT_MODE, NIGHT_MODE | for rgbw bulbs/strips: ON, OFF, DISCO_MODE, INC_DISCO_SPEED, DEC_DISCO_SPEED, as arguments )', default=None, required=False)

    argparser.add_argument('--colors', action='store_true', dest='show_colors',
                           help='Show supported colors', default=False, required=False)
    argparser.add_argument('--disco_modes', action='store_true', dest='show_disco_modes',
                           help='Show supported disco modes', default=False, required=False)
    argparser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                           help='Show some (more) details of what is happening', default=False, required=False)

    args = argparser.parse_args()

    # Set the bridge ip address and port
    bridge = args.address[0]
    # port = args.port

    # Scan for wifi bridges (to find the ip address)
    if args.scan:
        print('Discovering bridges')
        dg = mci.bridges.DiscoverBridge(port=48899).discover()
        for (addr, mac) in dg:
            print(' - ip address :' + addr + '\tmac: ' + mac)

    if args.show_colors:
        print('Supported colors:')
        for cc in mci.bulbs.ColorGroup.COLOR_CODES.keys():
            print(' - ' + str(cc))

    if args.show_disco_modes:
        print('Supported disco modes:')
        for dc in mci.bulbs.ColorGroup.DISCO_CODES.keys():
            print(' - ' + str(dc))

    # Set the bulb-type and group
    bulb = None
    group = None
    if args.rgbw is not None:
        bulb = 'RGBW'
        group = args.rgbw[0]
    elif args.white is not None:
        bulb = 'WHITE'
        group = args.white[0]

    # Set action
    action = None
    value = None
    if len(args.action) > 0:
        action = args.action[0]
    if len(args.action) > 1:
        args.action.pop(0)
        value = " ".join(args.action)

    if args.verbose:
        print('Details:')
        print(' bridge: ' + str(bridge))
        print(' bulb: ' + str(bulb))
        print(' group: ' + str(group))
        print(' action: ' + str(action))
        print(' value: ' + str(value))

    # Parse, validate, and execute the requested command
    mci.mci_parser.execute_command(bridge, bulb, group, action, value)


if __name__ == '__main__':
    main()
