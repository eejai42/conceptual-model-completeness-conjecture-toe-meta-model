import uuid

# A tiny helper so we can do object.some_collection.add(item).
# In normal Python you'd just use a list and call .append(...).
# We'll keep this for convenience, but it contains no aggregator logic.
class CollectionWrapper:
    def __init__(self, parent_object, attr_name):
        self.parent_object = parent_object
        self.attr_name = attr_name
        if not hasattr(parent_object, '_collections'):
            parent_object._collections = {}
        if attr_name not in parent_object._collections:
            parent_object._collections[attr_name] = []

    def add(self, item):
        self.parent_object._collections[self.attr_name].append(item)

    def __iter__(self):
        return iter(self.parent_object._collections[self.attr_name])

    def __len__(self):
        return len(self.parent_object._collections[self.attr_name])

    def __getitem__(self, index):
        return self.parent_object._collections[self.attr_name][index]

def _auto_id():
    """Simple helper to generate an ID if none is provided."""
    return str(uuid.uuid4())


class League:
    """Plain data container for League entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.leagueName = kwargs.get('leagueName')


class Team:
    """Plain data container for Team entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.teamName = kwargs.get('teamName')
        self.league_id = kwargs.get('league_id')


class Player:
    """Plain data container for Player entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.fullName = kwargs.get('fullName')
        self.battingHand = kwargs.get('battingHand')
        self.throwingHand = kwargs.get('throwingHand')
        self.team_id = kwargs.get('team_id')


class DefensivePosition:
    """Plain data container for DefensivePosition entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.positionName = kwargs.get('positionName')


class Game:
    """Plain data container for Game entities. Has a collection for innings."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.homeTeamId = kwargs.get('homeTeamId')
        self.awayTeamId = kwargs.get('awayTeamId')
        self.status = kwargs.get('status')
        self.ruleSetId = kwargs.get('ruleSetId')

        # Just storing child objects in a CollectionWrapper if you want 'game.innings.add(inning)'
        self.innings = CollectionWrapper(self, 'innings')


class Inning:
    """Plain data container for Inning entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.gameId = kwargs.get('gameId')
        self.inningNumber = kwargs.get('inningNumber')


class InningHalf:
    """Plain data container for InningHalf entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.halfType = kwargs.get('halfType')
        self.offensiveTeamId = kwargs.get('offensiveTeamId')
        self.defensiveTeamId = kwargs.get('defensiveTeamId')
        self.outs = kwargs.get('outs')
        self.runsScored = kwargs.get('runsScored')
        self.isComplete = kwargs.get('isComplete')

        # If you want to keep track of atBats in a collection, define it here:
        self.atBats = CollectionWrapper(self, 'atBats')


class AtBat:
    """Plain data container for AtBat entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.inningHalfId = kwargs.get('inningHalfId')
        self.batterId = kwargs.get('batterId')
        self.pitcherId = kwargs.get('pitcherId')
        self.result = kwargs.get('result')
        self.rbi = kwargs.get('rbi')
        self.exitVelocity = kwargs.get('exitVelocity')
        self.launchAngle = kwargs.get('launchAngle')

        self.pitches = CollectionWrapper(self, 'pitches')


class Pitch:
    """Plain data container for Pitch entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.atBatId = kwargs.get('atBatId')
        self.pitchResult = kwargs.get('pitchResult')
        self.pitchVelocity = kwargs.get('pitchVelocity')
        self.pitchSpinRate = kwargs.get('pitchSpinRate')


class Statistic:
    """Plain data container for Statistic entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.entityType = kwargs.get('entityType')
        self.entityId = kwargs.get('entityId')
        self.statName = kwargs.get('statName')
        self.statValue = kwargs.get('statValue')
        self.season = kwargs.get('season')
        self.lastUpdated = kwargs.get('lastUpdated')


class Stadium:
    """Plain data container for Stadium entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.stadiumName = kwargs.get('stadiumName')
        self.capacity = kwargs.get('capacity')


class OutEvent:
    """Plain data container for OutEvent entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.inningHalfId = kwargs.get('inningHalfId')
        self.atBatId = kwargs.get('atBatId')
        # You can store outType or fielderId here if needed.


class RunEvent:
    """Plain data container for RunEvent entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.inningHalfId = kwargs.get('inningHalfId')
        self.atBatId = kwargs.get('atBatId')
        self.runCount = kwargs.get('runCount')


class Season:
    """Plain data container for Season entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.seasonName = kwargs.get('seasonName')
        self.startDate = kwargs.get('startDate')
        self.endDate = kwargs.get('endDate')


class SeasonTeamStats:
    """Plain data container for SeasonTeamStats entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
        self.seasonId = kwargs.get('seasonId')
        self.teamId = kwargs.get('teamId')


class RuleSet:
    """Plain data container for RuleSet entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or _auto_id()
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
