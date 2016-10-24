# -*- coding: utf-8 -*-
""" MiLight Control Interface Parser

A powerful parser to use the MCI Python API to control your
MiLight LED bulbs and strips (White and RGBW).
"""

from . import bridges
from . import bulbs


class MCIParserException(Exception):
    pass


def parse_bridge(bridge):
    """ Parser and validator for the bridge information """
    if not bridge:
        raise MCIParserException('No bridge provided')
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
        raise MCIParserException('Provided bulb-type not valid (' + str(bulb) + ')')


def parse_group(group):
    """ Parser and validator for the group information """
    group = str(group).upper()
    if group in ['ALL', '0', '*']:
        return 'ALL'
    elif group in ['1', '2', '3', '4']:
        return group
    else:
        raise MCIParserException('Provided group description not valid (' + str(group) + ')')


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
    MCIParserException('Provided action not supported (' + str(action) + ' / ' + str(bulb) + ')')


def parse_value(value, action):
    """ Parser and validator for the value information (depends on the action) """
    # For RGBW bulbs
    if action == 'BRIGHTNESS':
        value = int(value)
        if value >= 0 and value <= 25:
            return value
        else:
            raise MCIParserException('Provided BRIGHTNESS value not valid (0 <= value <= 25)')
    if action == 'DISCO':
        if not value:
            return None
        elif isinstance(value, str):
            if value.upper() in bulbs.ColorGroup.DISCO_CODES.keys():
                return value.upper()
            else:
                raise MCIParserException('Provided DISCO value not valid (see: mci.ColorGroup.DISCO_CODES)')
        else:
            raise MCIParserException('Provided DISCO value not valid')
    if action in ['INCREASE_DISCO_SPEED', 'DECREASE_DISCO_SPEED']:
        if not value:
            value = 1
        value = int(value)
        if value >= 1 and value <= 30:
            return value
        else:
            raise MCIParserException('Provided DISCO_SPEED value not valid (1 <= value <= 30)')
    if action == 'COLOR':
        ivalue = None
        try:
            ivalue = int(value)
        except:
            pass
        if ivalue is not None:
            if ivalue >= 0 and ivalue <= 255:
                return ivalue
            else:
                raise MCIParserException('Provided COLOR value not valid (0 <= value <= 255)')
        elif isinstance(value, str):
            if value.upper() in bulbs.ColorGroup.COLOR_CODES.keys():
                return value.upper()
            else:
                raise MCIParserException('Provided COLOR value not valid (see: mci.ColorGroup.COLOR_CODES)')
        else:
            raise MCIParserException('Provided COLOR value not valid')
    # For WHITE bulbs
    if action in ['INCREASE_BRIGHTNESS', 'DECREASE_BRIGHTNESS', 'INCREASE_WARMTH', 'DECREASE_WARMTH']:
        if not value:
            value = 1
        value = int(value)
        if value >= 1 and value <= 30:
            return value
        else:
            raise MCIParserException('Provided BRIGHTNESS/WARMTH value not valid (1 <= value <= 30)')
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
        lc = bulbs.ColorGroup(ip_address=bridge, group_number=group)
        if action == 'ON':
            lc.on()
        elif action == 'OFF':
            lc.off()
        elif action == 'WHITE':
            lc.white()
        elif action == 'BRIGHTNESS':
            lc.brightness(value)
        elif action == 'DISCO':
            lc.disco(value)
        elif action == 'INCREASE_DISCO_SPEED':
            lc.increase_disco_speed(value)
        elif action == 'DECREASE_DISCO_SPEED':
            lc.decrease_disco_speed(value)
        elif action == 'COLOR':
            lc.color(value)
    elif bulb is 'WHITE':
        lc = bulbs.WhiteGroup(ip_address=bridge, group_number=group)
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
