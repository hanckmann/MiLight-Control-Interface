# -*- coding: utf-8 -*-
""" MiLight Control Interface Parser

A powerful parser to use the MCI Python API to control your
MiLight LED bulbs and strips (White and RGBW).
"""

import mci


class MCIParserException(Exception):
    pass


def parse_bridge(bridge):
    """ Parser and validator for the bridge information """
    return bridge
    # raise MCIParserException('Provided bridge not available')


def parse_bulb(bulb):
    """ Parser and validator for the bulb information """
    bulb = bulb.upper()
    if bulb in ['COLOR', 'RGBW']:
        return 'RGBW'
    elif bulb in ['WHITE']:
        return 'WHITE'
    else:
        raise MCIParserException('Provided bulb-type not valid')


def parse_group(group):
    """ Parser and validator for the group information """
    group = str(group).upper()
    if group in ['ALL', '0', '*']:
        return 'ALL'
    elif group in ['1', '2', '3', '4']:
        return group
    else:
        raise MCIParserException('Provided group description not valid')


def parse_action(action, bulb):
    """ Parser and validator for the action information (depends on the bulb-type) """
    action = action.upper()
    if action in ['ON', 'OFF']:
        return action
    if parse_bulb(bulb) in ['RGBW']:
        # Check for RBWG actions
        if action in ['WHITE', 'BRIGHTNESS', 'DISCO', 'INCREASE_DISCO_SPEED', 'DECREASE_DISCO_SPEED', 'COLOR']:
            return action
    if parse_bulb(bulb) in ['WHITE']:
        # Check for WHITE actions
        if action in ['INCREASE_BRIGHTNESS', 'DECREASE_BRIGHTNESS', 'INCREASE_WARMTH', 'DECREASE_WARMTH', 'BRIGHTMODE', 'NIGHTMODE']:
            return action
    MCIParserException('Provided action not supported')


def parse_value(value, action):
    """ Parser and validator for the value information (depends on the action) """
    # For RGBW bulbs
    if action == 'BRIGHTNESS':
        value = int(value)
        if value >= 0 and value <= 25:
            return value
        else:
            raise MCIParserException('Provided value not valid')
    if action == 'DISCO':
        value = value.upper()
        if value in mci.ColorGroup.DISCO_CODES.keys():
            return value
        else:
            raise MCIParserException('Provided value not valid')
    if action in ['INCREASE_DISCO_SPEED', 'DECREASE_DISCO_SPEED']:
        if not value:
            value = 1
        value = int(value)
        if value >= 1 and value <= 30:
            return value
        else:
            raise MCIParserException('Provided value not valid')
    if action == 'COLOR':
        value = value.upper()
        if value in mci.ColorGroup.COLOR_CODES.keys():
            return value
        else:
            raise MCIParserException('Provided value not valid')
    # For WHITE bulbs
    if action in ['INCREASE_BRIGHTNESS', 'DECREASE_BRIGHTNESS', 'INCREASE_WARMTH', 'DECREASE_WARMTH']:
        if not value:
            value = 1
        value = int(value)
        if value >= 1 and value <= 30:
            return value
        else:
            raise MCIParserException('Provided value not valid')
    return None


def validate_command(bridge, bulb, group, action, value):
    """ Parses, and validates the requested command """
    bridge = parse_bridge(bridge)
    bulb = parse_bulb(bulb)
    group = parse_group(group)
    action = parse_action(action, bulb)
    value = parse_value(value, action)
    return (True, bridge, bulb, group, action, value)


def execute_command(bridge, bulb, group, action, value):
    """ Parses, validates, and executes the requested command """
    (valid, bridge, bulb, group, action, value) = validate_command(bridge, bulb, group, action, value)
    if not valid:
        MCIParserException('Invalid command provided')

    if bulb is 'RGBW':
        lc = mci.ColorGroup(ip_address=bridge, group_number=group)
        if action == 'ON':
            lc.on()
        elif action == 'OFF':
            lc.off()
        elif action == 'WHITE':
            lc.white()
        elif action == 'BRIGHTNESS':
            lc.brightness(value)
        elif action == 'DISCO':
            lc.disco()
        elif action == 'INCREASE_DISCO_SPEED':
            lc.increase_disco_speed()
        elif action == 'DECREASE_DISCO_SPEED':
            lc.decrease_disco_speed()
        elif action == 'COLOR':
            lc.color(value)
    elif bulb is 'WHITE':
        lc = mci.WhiteGroup(ip_address=bridge, group_number=group)
        if action == 'ON':
            lc.on()
        if action == 'OFF':
            lc.off()
        if action == 'INCREASE_BRIGHTNESS':
            lc.increase_brightness(value)
        if action == 'DECREASE_BRIGHTNESS':
            lc.decrease_brightness(value)
        if action == 'INCREASE_WARMTH':
            lc.increase_warmth(value)
        if action == 'DECREASE_WARMTH':
            lc.decrease_warmth(value)
        if action == 'BRIGHTMODE':
            lc.brightmode()
        if action == 'NIGHTMODE':
            lc.nightmode()
