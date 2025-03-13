# zlang/rosetta_stone.py
#
# Holds the fixed mapping of digits (0-9) and operators (+ - * / = ^ #)
# to their alien equivalents. These must remain constant.

ROSETTA_ENGLISH_TO_ALIEN = {
    '0': 'ç',
    '1': 'ª',
    '2': 'ö',
    '3': '£',
    '4': '¤',
    '5': 'Ð',
    '6': '¥',
    '7': 'À',
    '8': '©',
    '9': '§',
    '+': '²',
    '-': 'ø',
    '*': 'ð',
    '/': '¶',
    '=': 'å',
    '#': 'æ',
    '^': 'ß'
}

ROSETTA_ALIEN_TO_ENGLISH = {
    'ç': '0',
    'ª': '1',
    'ö': '2',
    '£': '3',
    '¤': '4',
    'Ð': '5',
    '¥': '6',
    'À': '7',
    '©': '8',
    '§': '9',
    '²': '+',
    'ø': '-',
    'ð': '*',
    '¶': '/',
    'å': '=',
    'æ': '#',
    'ß': '^'
}
