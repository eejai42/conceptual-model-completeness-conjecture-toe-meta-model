"""
Auto-generated Python code from your quantum-walk rulebook.
References SHIFT, APPLY_BARRIER, EVOLVE, etc. from an external python file.
"""
import math
import numpy as np

# ----- Generated classes below -----

class League:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.leagueName = kwargs.get('leagueName')

class Team:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.teamName = kwargs.get('teamName')
        self.league_id = kwargs.get('league_id')

class Player:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.fullName = kwargs.get('fullName')
        self.battingHand = kwargs.get('battingHand')
        self.throwingHand = kwargs.get('throwingHand')
        self.team_id = kwargs.get('team_id')

class DefensivePosition:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.positionName = kwargs.get('positionName')

class Game:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.homeTeamId = kwargs.get('homeTeamId')
        self.awayTeamId = kwargs.get('awayTeamId')
        self.status = kwargs.get('status')
        self.ruleSetId = kwargs.get('ruleSetId')

class Inning:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.gameId = kwargs.get('gameId')
        self.inningNumber = kwargs.get('inningNumber')

class InningHalf:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.halfType = kwargs.get('halfType')
        self.offensiveTeamId = kwargs.get('offensiveTeamId')
        self.defensiveTeamId = kwargs.get('defensiveTeamId')
        self.outs = kwargs.get('outs')
        self.runsScored = kwargs.get('runsScored')
        self.isComplete = kwargs.get('isComplete')

class AtBat:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.inningHalfId = kwargs.get('inningHalfId')
        self.batterId = kwargs.get('batterId')
        self.pitcherId = kwargs.get('pitcherId')
        self.result = kwargs.get('result')
        self.rbi = kwargs.get('rbi')
        self.exitVelocity = kwargs.get('exitVelocity')
        self.launchAngle = kwargs.get('launchAngle')

class Pitch:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.atBatId = kwargs.get('atBatId')
        self.pitchResult = kwargs.get('pitchResult')
        self.pitchVelocity = kwargs.get('pitchVelocity')
        self.pitchSpinRate = kwargs.get('pitchSpinRate')

class Statistic:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.entityType = kwargs.get('entityType')
        self.entityId = kwargs.get('entityId')
        self.statName = kwargs.get('statName')
        self.statValue = kwargs.get('statValue')
        self.season = kwargs.get('season')
        self.lastUpdated = kwargs.get('lastUpdated')

class Stadium:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.stadiumName = kwargs.get('stadiumName')
        self.capacity = kwargs.get('capacity')

class OutEvent:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.inningHalfId = kwargs.get('inningHalfId')
        self.atBatId = kwargs.get('atBatId')

class RunEvent:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.inningHalfId = kwargs.get('inningHalfId')
        self.atBatId = kwargs.get('atBatId')
        self.runCount = kwargs.get('runCount')

class Season:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.seasonName = kwargs.get('seasonName')
        self.startDate = kwargs.get('startDate')
        self.endDate = kwargs.get('endDate')

class SeasonTeamStats:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.seasonId = kwargs.get('seasonId')
        self.teamId = kwargs.get('teamId')

class RuleSet:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.ruleSetName = kwargs.get('ruleSetName')
        self.dhEnabled = kwargs.get('dhEnabled')
        self.mercyRuleEnabled = kwargs.get('mercyRuleEnabled')
        self.mercyRuleInningThreshold = kwargs.get('mercyRuleInningThreshold')
        self.pitchDistance = kwargs.get('pitchDistance')
        self.basePathDistance = kwargs.get('basePathDistance')
        self.maxPitchCount = kwargs.get('maxPitchCount')
        self.extraInningRunnerRuleEnabled = kwargs.get('extraInningRunnerRuleEnabled')
        self.overAgeLimit = kwargs.get('overAgeLimit')
        self.usesReplayReview = kwargs.get('usesReplayReview')
        self.allowLeadingOff = kwargs.get('allowLeadingOff')
