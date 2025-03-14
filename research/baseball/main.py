#!/usr/bin/env python3

import json
import argparse
import math
import re
import textwrap
import os
import baseball_cmcc_sdk

"""
A CLI tool (main.py) that demonstrates using a hypothetical baseball CMCC SDK.
We assume there's a sibling file named baseball-cmcc-sdk.py that exposes
classes/functions like 'Game', 'Inning', 'Player' with declarative logic.

This script:
1) Creates a new game.
2) Starts the first inning.
3) Gets the first player at bat.
4) Simulates a strikeout.
5) Moves to the next batter.
"""

# We import our imaginary baseball CMCC SDK module.
from baseball_cmcc_sdk import *

def main():
    game = Game()  # create a Game object
    firstInning = Inning()
    firstInning.inningNumber = 1
    firstInning.gameId = game.id # this should be firstInning.game = game; (which should automatically add the inning to the game.innings.  All of the ids should be transparent.
    game.innings.add(firstInning)  #if this is what's done, then the innings for the game will already be updated, but the inning will need to have it's "game" pointed back at the main game.

    new_atbat = AtBat(inningHalfId=firstInning.id, batterId=..., pitcherId=...)

    
    new_atbat.pitches.add(Pitch(pitchResult='SWINGING_STRIKE'))
    if new_atbat.batterHasStruckOut:
        print("Batter struck out.")


if __name__ == "__main__":
    main()
