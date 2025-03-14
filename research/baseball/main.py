#!/usr/bin/env python3

import baseball_cmcc_sdk

def main():
    # 1) Create a new game
    game = baseball_cmcc_sdk.Game()
    game.status = "IN_PROGRESS"

    # 2) Create the first inning record
    first_inning = baseball_cmcc_sdk.Inning(inningNumber=1)
    # Add it to the game
    game.innings.add(first_inning)

    # 3) Create an AtBat in that inning
    atbat = baseball_cmcc_sdk.AtBat(inningHalfId=first_inning.id, batterId="player_101", pitcherId="player_102")

    # 4) Add a few pitches
    atbat.pitches.add(baseball_cmcc_sdk.Pitch(pitchResult='SWINGING_STRIKE'))
    # atbat.pitches.add(baseball_cmcc_sdk.Pitch(pitchResult='FOUL'))
    atbat.pitches.add(baseball_cmcc_sdk.Pitch(pitchResult='SWINGING_STRIKE'))

    # Now let's do our aggregator logic right here in main:
    # "If the pitchResult is in ['CALLED_STRIKE','SWINGING_STRIKE','FOUL'], it's a strike."
    # We'll count them up:
    strike_count = sum(
        1
        for pitch in atbat.pitches
        if pitch.pitchResult in ['CALLED_STRIKE','SWINGING_STRIKE','FOUL']
    )

    # 5) Check if the batter struck out
    if strike_count >= 3:
        print("Batter has struck out!")
    else:
        print("Batter is still up.")

if __name__ == "__main__":
    main()
