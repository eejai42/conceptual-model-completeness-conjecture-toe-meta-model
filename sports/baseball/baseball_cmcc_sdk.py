"""
Auto-generated Python code from your domain model.
Now with advanced aggregator rewriting to reduce syntax errors.
"""
import math
import numpy as np
import statistics

import uuid

# A tiny helper so we can do object.some_collection.add(item).
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
    return str(uuid.uuid4())

# aggregator placeholders:
def _COUNT(expr):
    # We'll guess if there's a 'WHERE' in expr, it was already replaced. 
    # In practice we'd parse it properly, but let's fallback:
    return f"/* _COUNT({expr}) not fully implemented */"

def _SUM(expr):
    return f"/* _SUM({expr}) not fully implemented */"

def _AVG(expr):
    return f"/* _AVG({expr}) not fully implemented */"

def _MINBY(expr):
    return f"/* _MINBY({expr}) not fully implemented */"

def _MAXBY(expr):
    return f"/* _MAXBY({expr}) not fully implemented */"

def _MODE(expr):
    return f"/* _MODE({expr}) not fully implemented */"

def _TOPN(expr):
    return f"/* _TOPN({expr}) not fully implemented */"

def _EXISTS(expr):
    return f"/* _EXISTS({expr}) not fully implemented */"


# ----- Generated classes below -----

class League:
    """Plain data container for League entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.leagueName = kwargs.get('leagueName')

        self.teams = CollectionWrapper(self, 'teams')

    @property
    def teamCount(self):
        """Number of teams in this league.
        Original formula: COUNT(teams)
        """
        return _COUNT(teams)

    @property
    def totalGamesPlayed(self):
        """Sum of all Games completed by all Teams in the league. Implementation conceptual, scanning each team's 'gamesPlayed'.
        Original formula: SUM(teams.gamesPlayed)
        """
        return _SUM(teams.gamesPlayed)

    @property
    def bestTeam(self):
        """The team with the highest win percentage in this league (declarative aggregator).
        Original formula: MAXBY(teams, t => t.winPercentage)
        """
        return _MAXBY(teams, t => t.winPercentage)

    @property
    def worstTeam(self):
        """The team with the lowest win percentage in this league (declarative aggregator).
        Original formula: MINBY(teams, t => t.winPercentage)
        """
        return _MINBY(teams, t => t.winPercentage)

    @property
    def averageTeamERA(self):
        """The average ERA across all teams in this league. Implementation conceptual, could sum or average pitchers’ ERA or overall team ERA.
        Original formula: AVG(teams -> eachTeamERA)
        """
        return _AVG(teams -> eachTeamERA)

    @property
    def totalLeagueHomeRuns(self):
        """The sum of all home runs hit by players on all teams in this league, purely data-based aggregator.
        Original formula: SUM(teams.roster -> careerHomeRuns)
        """
        return _SUM(teams.roster -> careerHomeRuns)

    @property
    def totalLeagueStolenBases(self):
        """The sum of all stolen bases by players on all teams in this league.
        Original formula: SUM(teams.roster -> careerStolenBases)
        """
        return _SUM(teams.roster -> careerStolenBases)

    @property
    def leagueOPSLeaders(self):
        """Top 3 players in the league by OPS. Implementation conceptual using all rosters in this league.
        Original formula: TOPN(3, teams.roster, p => p.ops)
        """
        return _TOPN(3, teams.roster, p => p.ops)

    @property
    def leagueMinERA(self):
        """Identifies the single pitcher in the league with the lowest ERA. Implementation conceptual—filters for pitchers only.
        Original formula: MINBY(teams.roster where playerIsPitcher=true, p => p.careerERA)
        """
        return _MINBY(teams.roster where playerIsPitcher==True, p => p.careerERA)

    @property
    def mostCommonBattingHand(self):
        """Identifies the batting hand (L, R, or S) that is most common among all players in the league's teams.
        Original formula: MODE(teams.roster.battingHand)
        """
        return _MODE(teams.roster.battingHand)

    @property
    def leagueWalkToStrikeoutRatio(self):
        """Computes total walks / total strikeouts across all players in the league. Conceptual aggregator.
        Original formula: SUM(teams.roster => careerWalks) / SUM(teams.roster => careerStrikeouts)
        """
        return _SUM(teams.roster => careerWalks) / _SUM(teams.roster => careerStrikeouts)

class Team:
    """Plain data container for Team entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.teamName = kwargs.get('teamName')
        self.league_id = kwargs.get('league_id')

        self.roster = CollectionWrapper(self, 'roster')

    @property
    def rosterSize(self):
        """Number of players on the team's active roster.
        Original formula: COUNT(roster)
        """
        return _COUNT(roster)

    @property
    def gamesPlayed(self):
        """Number of Games in which this team has participated (data-based aggregator).
        Original formula: COUNT(Game where (homeTeamId=this.id OR awayTeamId=this.id))
        """
        return _COUNT(Game where (homeTeamId==self.id  or  awayTeamId==self.id))

    @property
    def wins(self):
        """Count of Games this team has won (pure aggregator, no imperative updates).
        Original formula: COUNT(Game where (winnerId=this.id))
        """
        return _COUNT(Game where (winnerId==self.id))

    @property
    def losses(self):
        """Count of Games this team has lost.
        Original formula: COUNT(Game where (loserId=this.id))
        """
        return _COUNT(Game where (loserId==self.id))

    @property
    def winPercentage(self):
        """wins / (wins + losses), if any games played. Null otherwise.
        Original formula: IF (gamesPlayed>0) THEN (wins / gamesPlayed) ELSE null
        """
        return IF (gamesPlayed>0) THEN (wins / gamesPlayed) ELSE None

    @property
    def averageTeamBattingAverage(self):
        """The average batting average among all players on the roster, purely aggregator.
        Original formula: AVG(roster.careerBattingAverage)
        """
        return _AVG(roster.careerBattingAverage)

    @property
    def totalTeamRuns(self):
        """Total runs scored by this team (across all games). Implementation conceptual.
        Original formula: SUM(GameInnings where offense=this.id => runsScored )
        """
        return _SUM(GameInnings where offense==self.id => runsScored)

    @property
    def totalTeamHomeRuns(self):
        """Sum of home runs hit by all players on this team.
        Original formula: SUM(roster -> careerHomeRuns)
        """
        return _SUM(roster -> careerHomeRuns)

    @property
    def totalTeamStolenBases(self):
        """Sum of stolen bases by all players on this team.
        Original formula: SUM(roster -> careerStolenBases)
        """
        return _SUM(roster -> careerStolenBases)

    @property
    def averageFieldingPercentage(self):
        """The team’s overall fielding percentage, averaging all players’ fielding percentages who actively field.
        Original formula: AVG(roster -> careerFieldingPercentage )
        """
        return _AVG(roster -> careerFieldingPercentage)

    @property
    def winningPercentageInStadium(self):
        """Team’s historical winning percentage in a given stadium—pure aggregator referencing stadium-based game data.
        Original formula: WIN_PCT_BY_STADIUM_FUNCTION(this.id)
        """
        return win_pct_by_stadium_function(self.id)

    @property
    def bestPitcher(self):
        """Finds the pitcher on this team with the lowest ERA (pure aggregator).
        Original formula: MINBY(roster where playerIsPitcher=true, p => p.careerERA)
        """
        return _MINBY(roster where playerIsPitcher==True, p => p.careerERA)

    @property
    def totalWalks(self):
        """Sums all walks drawn by players on this team.
        Original formula: SUM(roster => careerWalks)
        """
        return _SUM(roster => careerWalks)

    @property
    def totalHitByPitch(self):
        """Sums all HBP events for players on this team.
        Original formula: SUM(roster => careerHitByPitch)
        """
        return _SUM(roster => careerHitByPitch)

    @property
    def teamSluggingPct(self):
        """Overall slugging percentage for the team, computed by summing total bases across all players and dividing by total at-bats.
        Original formula: (SUM(roster => totalBases) / SUM(roster => careerAtBats))
        """
        return (_SUM(roster => totalBases) / _SUM(roster => careerAtBats))

    @property
    def homeRunsPerGame(self):
        """Team’s home runs divided by the total games played, if gamesPlayed>0.
        Original formula: IF(gamesPlayed>0) THEN (totalTeamHomeRuns / gamesPlayed) ELSE null
        """
        return IF(gamesPlayed>0) THEN (totalTeamHomeRuns / gamesPlayed) ELSE None

    @property
    def pitcherCount(self):
        """Number of players on the roster who are pitchers (or have pitched). Implementation conceptual if 'playerIsPitcher' is known.
        Original formula: COUNT(roster WHERE playerIsPitcher=true)
        """
        return _COUNT(roster WHERE playerIsPitcher==True)

    @property
    def shutoutsAchieved(self):
        """Count how many shutout wins this team has recorded. Conceptual aggregator scanning final games where runsAllowed=0.
        Original formula: COUNT(Game WHERE winnerId=this.id AND (IF homeTeamId=this.id THEN runsAway=0 ELSE runsHome=0))
        """
        return _COUNT(Game WHERE winnerId==self.id  and  (IF homeTeamId==self.id THEN runsAway==0 ELSE runsHome==0))

    @property
    def currentWinStreak(self):
        """How many consecutive games (starting with the most recent) the team has won. Implementation conceptual, purely aggregator-based.
        Original formula: CALC_CURRENT_WIN_STREAK(this.id)
        """
        return CALC_CURRENT_WIN_STREAK(self.id)

    @property
    def pythagWinPct(self):
        """Estimates winning percentage from runs scored vs. runs allowed (Pythagorean expectation).
        Original formula: IF(totalTeamRuns>0 OR runsAllowed>0) THEN (POWER(totalTeamRuns,2)/(POWER(totalTeamRuns,2)+POWER(runsAllowed,2))) ELSE null
        """
        return IF(totalTeamRuns>0  or  runsAllowed>0) THEN ((totalTeamRuns**2)/((totalTeamRuns**2)+(runsAllowed**2))) ELSE None

    @property
    def teamWalkRate(self):
        """Walks drawn per plate appearance by the entire team.
        Original formula: totalWalks / totalPlateAppearances
        """
        return totalWalks / totalPlateAppearances

    @property
    def teamStrikeoutRate(self):
        """Team-wide ratio of strikeouts to total plate appearances.
        Original formula: (COUNT(AtBat WHERE offenseTeam=this.id AND result='STRIKEOUT')) / totalPlateAppearances
        """
        return (_COUNT(AtBat WHERE offenseTeam==self.id  and  result=='STRIKEOUT')) / totalPlateAppearances

    @property
    def runsAllowed(self):
        """Total runs allowed by this team across all games (aggregator from the defensive perspective).
        Original formula: SUM(GameInnings WHERE defenseTeamId=this.id => runsScored)
        """
        return _SUM(GameInnings WHERE defenseTeamId==self.id => runsScored)

    @property
    def hasExceededPitcherRosterLimit(self):
        """
        Original formula: pitcherCount > 13
        """
        return pitcherCount > 13

    @property
    def currentlyHasDHAvailable(self):
        """
        Original formula: NOT allDesignatedHittersUsedUp( this.id )
        """
        return not  all_designated_hitters_used_up( self.id )

    @property
    def teamErrorCount(self):
        """
        Original formula: COUNT( ErrorEvent WHERE ErrorEvent.teamId = this.id )
        """
        return _COUNT(ErrorEvent WHERE ErrorEvent.teamId == self.id)

    @property
    def isOverLuxuryTaxCap(self):
        """
        Original formula: TEAM_PAYROLL( this.id ) > LUXURY_TAX_THRESHOLD
        """
        return team_payroll( self.id ) > LUXURY_TAX_THRESHOLD

    @property
    def hasActiveChickenDancer(self):
        """
        Original formula: EXISTS( Player WHERE Player.team_id = this.id AND Player.chickenStanceIndicator = true )
        """
        return _EXISTS( Player WHERE Player.team_id == self.id  and  Player.chickenStanceIndicator == True )

    @property
    def dhSlotInUse(self):
        """If the rule set has DH enabled and the team has at least one pitcher, a DH slot may be in use. This aggregator references the team's league's rule set for demonstration.
        Original formula: IF (this.league_id.ruleSetId.dhEnabled = true AND pitcherCount > 0) THEN 'DH Slot Active' ELSE 'No DH Slot'
        """
        return IF (self.league_id.ruleSetId.dhEnabled == True  and  pitcherCount > 0) THEN 'DH Slot Active' ELSE 'No DH Slot'

    @property
    def maxRosterSize(self):
        """Specifies maximum roster size allowed by the rule set. Some leagues limit rosters to fewer players.
        Original formula: IF (this.league_id.ruleSetId.ruleSetName='LittleLeague_2025') THEN 14 ELSE 26
        """
        return IF (self.league_id.ruleSetId.ruleSetName=='LittleLeague_2025') THEN 14 ELSE 26

    @property
    def extendedRosterAllowed(self):
        """Indicates if additional players are permitted on the roster temporarily (some leagues allow expanded rosters in certain months).
        Original formula: IF (this.league_id.ruleSetId.ruleSetName='September_Expansions') THEN true ELSE false
        """
        return IF (self.league_id.ruleSetId.ruleSetName=='September_Expansions') THEN True ELSE False

class Player:
    """Plain data container for Player entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.fullName = kwargs.get('fullName')
        self.battingHand = kwargs.get('battingHand')
        self.throwingHand = kwargs.get('throwingHand')
        self.team_id = kwargs.get('team_id')

        self.defensivePositions = CollectionWrapper(self, 'defensivePositions')

    @property
    def careerAtBats(self):
        """How many official at-bats the player has had across all games.
        Original formula: COUNT( AtBat where (batterId=this.id) )
        """
        return _COUNT(AtBat where (batterId==self.id) )

    @property
    def careerHits(self):
        """How many hits the player has recorded across all at-bats.
        Original formula: COUNT( AtBat where (batterId=this.id AND result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN']) )
        """
        return _COUNT(AtBat where (batterId==self.id  and  result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN']) )

    @property
    def careerBattingAverage(self):
        """(careerHits / careerAtBats). Null if no at-bats.
        Original formula: IF (careerAtBats>0) THEN (careerHits / careerAtBats) ELSE null
        """
        return IF (careerAtBats>0) THEN (careerHits / careerAtBats) ELSE None

    @property
    def careerPitchCount(self):
        """Total number of pitches thrown by this player, if a pitcher.
        Original formula: COUNT( Pitch where (pitcherId=this.id) )
        """
        return _COUNT(Pitch where (pitcherId==self.id) )

    @property
    def careerStrikeoutsPitched(self):
        """How many strikeouts the player (as pitcher) has recorded.
        Original formula: COUNT( AtBat where (pitcherId=this.id AND result='STRIKEOUT') )
        """
        return _COUNT(AtBat where (pitcherId==self.id  and  result=='STRIKEOUT') )

    @property
    def careerInningsPitched(self):
        """Summation of partial innings if the player is a pitcher. Implementation conceptual.
        Original formula: AccumulateInningsFromOuts( sum_of_outs_where_pitcherId=this.id )
        """
        return AccumulateInningsFromOuts( sum_of_outs_where_pitcherId==self.id )

    @property
    def onBasePercentage(self):
        """OBP = (H + BB + HBP) / (AB + BB + HBP + SF). Implementation conceptual if advanced data is tracked.
        Original formula: IF (plateAppearances>0) THEN ((careerHits + careerWalks + careerHitByPitch) / (careerAtBats + careerWalks + careerHitByPitch + careerSacFlies)) ELSE null
        """
        return IF (plateAppearances>0) THEN ((careerHits + careerWalks + careerHitByPitch) / (careerAtBats + careerWalks + careerHitByPitch + careerSacFlies)) ELSE None

    @property
    def sluggingPercentage(self):
        """Total bases / at-bats. Implementation conceptual if we track 2B,3B,HR, etc.
        Original formula: IF (careerAtBats>0) THEN (sumOfTotalBases / careerAtBats) ELSE null
        """
        return IF (careerAtBats>0) THEN (sumOfTotalBases / careerAtBats) ELSE None

    @property
    def ops(self):
        """On-base plus slugging, purely aggregator of the OBP + SLG fields.
        Original formula: onBasePercentage + sluggingPercentage
        """
        return onBasePercentage + sluggingPercentage

    @property
    def stolenBasePercentage(self):
        """stolenBases / (stolenBases + caughtStealing). Implementation conceptual if we track that data.
        Original formula: IF ((careerStolenBases + careerCaughtStealing) > 0) THEN (careerStolenBases / (careerStolenBases + careerCaughtStealing)) ELSE null
        """
        return IF ((careerStolenBases + careerCaughtStealing) > 0) THEN (careerStolenBases / (careerStolenBases + careerCaughtStealing)) ELSE None

    @property
    def isTwoWayPlayer(self):
        """Boolean indicating if the player has pitched and also batted as a regular hitter. Implementation conceptual.
        Original formula: IF (careerInningsPitched > 0 AND careerAtBats > 0) THEN true ELSE false
        """
        return IF (careerInningsPitched > 0  and  careerAtBats > 0) THEN True ELSE False

    @property
    def careerWalks(self):
        """Count of times the player reached base via walk (BB).
        Original formula: COUNT( AtBat where batterId=this.id AND result='WALK' )
        """
        return _COUNT(AtBat where batterId==self.id  and  result=='WALK')

    @property
    def careerHitByPitch(self):
        """Count of times the player was hit by a pitch (HBP).
        Original formula: COUNT( AtBat where batterId=this.id AND result='HIT_BY_PITCH' )
        """
        return _COUNT(AtBat where batterId==self.id  and  result=='HIT_BY_PITCH')

    @property
    def careerSacFlies(self):
        """Count of official at-bats with a sac fly result.
        Original formula: COUNT( AtBat where batterId=this.id AND result='SAC_FLY')
        """
        return _COUNT(AtBat where batterId==self.id  and  result=='SAC_FLY')

    @property
    def careerDoublePlaysGroundedInto(self):
        """Number of times the player has grounded into a double play.
        Original formula: COUNT( AtBat where batterId=this.id AND result='GROUNDED_INTO_DOUBLE_PLAY')
        """
        return _COUNT(AtBat where batterId==self.id  and  result=='GROUNDED_INTO_DOUBLE_PLAY')

    @property
    def highestExitVelocity(self):
        """Max exit velocity recorded for batted balls by this player (across all relevant at-bats).
        Original formula: MAX( AtBat where batterId=this.id => exitVelocity )
        """
        return max( AtBat where batterId==self.id => exitVelocity )

    @property
    def lowestExitVelocity(self):
        """Min exit velocity recorded for batted balls by this player.
        Original formula: MIN( AtBat where batterId=this.id => exitVelocity )
        """
        return min( AtBat where batterId==self.id => exitVelocity )

    @property
    def careerSluggingPct(self):
        """Slugging percentage across all at-bats in the player's career (total bases / careerAtBats). Implementation conceptual.
        Original formula: IF(careerAtBats>0) THEN (SUM_OF_PLAYER_TOTAL_BASES(this.id) / careerAtBats) ELSE null
        """
        return IF(careerAtBats>0) THEN (SUM_OF_PLAYER_TOTAL_BASES(self.id) / careerAtBats) ELSE None

    @property
    def careerOPS(self):
        """Career On-base plus slugging for this player: onBasePercentage + careerSluggingPct.
        Original formula: onBasePercentage + careerSluggingPct
        """
        return onBasePercentage + careerSluggingPct

    @property
    def hitsAbove100ExitVelo(self):
        """Number of hits where the exit velocity exceeded 100 mph.
        Original formula: COUNT( AtBat where batterId=this.id AND exitVelocity>100 AND result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN'])
        """
        return _COUNT(AtBat where batterId==self.id  and  exitVelocity>100  and  result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN'])

    @property
    def outsRecordedAsPitcher(self):
        """How many outs this player has generated in a pitching role. Implementation conceptual—count OutEvents where pitcherId=this.id.
        Original formula: COUNT( OutEvent where (atBatId!=null AND AtBat.pitcherId=this.id) OR (someOtherPitcherOutRef) )
        """
        return _COUNT(OutEvent where (atBatId!=None  and  AtBat.pitcherId==self.id)  or  (someOtherPitcherOutRef) )

    @property
    def totalBases(self):
        """Sum of bases the player has earned via hits (1 for single, 2 for double, etc.). Implementation conceptual scanning all hits.
        Original formula: SUM( AtBat where batterId=this.id => mapHitToBases(result) )
        """
        return _SUM(AtBat where batterId==self.id => mapHitToBases(result) )

    @property
    def hasCycleInAnyGame(self):
        """Indicates whether the player has ever completed a single, double, triple, and home run in the same game.
        Original formula: EXISTS(Game WHERE EXISTS(AtBat[batterId=this.id AND gameId=Game.id AND result='SINGLE']) AND EXISTS(AtBat[batterId=this.id AND gameId=Game.id AND result='DOUBLE']) AND EXISTS(AtBat[batterId=this.id AND gameId=Game.id AND result='TRIPLE']) AND EXISTS(AtBat[batterId=this.id AND gameId=Game.id AND result='HOMERUN']))
        """
        return _EXISTS(Game WHERE EXISTS(AtBat[batterId==self.id  and  gameId==Game.id  and  result=='SINGLE'])  and  _EXISTS(AtBat[batterId==self.id  and  gameId==Game.id  and  result=='DOUBLE'])  and  _EXISTS(AtBat[batterId==self.id  and  gameId==Game.id  and  result=='TRIPLE'])  and  _EXISTS(AtBat[batterId==self.id  and  gameId==Game.id  and  result=='HOMERUN']))

    @property
    def longestHitStreak(self):
        """The maximum consecutive-game hitting streak in the player's career.
        Original formula: CALCULATE_MAX_CONSECUTIVE_HIT_GAMES(playerId=this.id)
        """
        return calculate_max_consecutive_hit_games(playerId==self.id)

    @property
    def longestOnBaseStreak(self):
        """The maximum consecutive-game streak where the player reached base at least once (hit, walk, HBP, etc.).
        Original formula: CALCULATE_MAX_CONSECUTIVE_ONBASE_GAMES(playerId=this.id)
        """
        return calculate_max_consecutive_onbase_games(playerId==self.id)

    @property
    def careerIso(self):
        """Isolated Power = slugging percentage - batting average.
        Original formula: IF(careerSluggingPct!=null AND careerBattingAverage!=null) THEN (careerSluggingPct - careerBattingAverage) ELSE null
        """
        return IF(careerSluggingPct!=None  and  careerBattingAverage!=None) THEN (careerSluggingPct - careerBattingAverage) ELSE None

    @property
    def careerDoublePlaysTurned(self):
        """How many double plays the player has been credited with turning on defense.
        Original formula: COUNT(OutEvent WHERE designation='DOUBLE_PLAY' AND fielderId=this.id)
        """
        return _COUNT(OutEvent WHERE designation=='DOUBLE_PLAY'  and  fielderId==self.id)

    @property
    def careerTriplePlaysTurned(self):
        """How many triple plays the player has been credited with turning on defense.
        Original formula: COUNT(OutEvent WHERE designation='TRIPLE_PLAY' AND fielderId=this.id)
        """
        return _COUNT(OutEvent WHERE designation=='TRIPLE_PLAY'  and  fielderId==self.id)

    @property
    def careerMaxHomeRunDistance(self):
        """Maximum recorded distance of any home run for this player.
        Original formula: MAX(AtBat WHERE batterId=this.id AND result='HOMERUN' => battedBallDistance)
        """
        return max(AtBat WHERE batterId==self.id  and  result=='HOMERUN' => battedBallDistance)

    @property
    def careerGrandSlams(self):
        """Number of home runs with the bases loaded (4 RBI).
        Original formula: COUNT(AtBat WHERE batterId=this.id AND result='HOMERUN' AND baseStateBeforePitch='BASES_LOADED')
        """
        return _COUNT(AtBat WHERE batterId==self.id  and  result=='HOMERUN'  and  baseStateBeforePitch=='BASES_LOADED')

    @property
    def careerWalkOffHits(self):
        """Count of game-ending hits delivered by the player (walk-off singles, doubles, etc.).
        Original formula: COUNT(AtBat WHERE batterId=this.id AND result IN ['SINGLE','DOUBLE','TRIPLE','HOMERUN'] AND AtBatEndsGame=true)
        """
        return _COUNT(AtBat WHERE batterId==self.id  and  result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN']  and  AtBatEndsGame==True)

    @property
    def careerWOBA(self):
        """Weighted On-Base Average, using established wOBA coefficients.
        Original formula: CALCULATE_WOBA(this.id)
        """
        return calculate_woba(self.id)

    @property
    def careerWRCPlus(self):
        """Weighted Runs Created Plus, comparing player to league average = 100.
        Original formula: CALCULATE_WRC_PLUS(this.id, LEAGUE_OFFENSIVE_ENVIRONMENT)
        """
        return calculate_wrc_plus(self.id, LEAGUE_OFFENSIVE_ENVIRONMENT)

    @property
    def careerDefensiveErrors(self):
        """Number of times the player committed an error (tracked via ErrorEvent).
        Original formula: COUNT(ErrorEvent WHERE fielderId=this.id)
        """
        return _COUNT(ErrorEvent WHERE fielderId==self.id)

    @property
    def careerPlateAppearances(self):
        """Comprehensive aggregator for all times the player came to bat, including walks, HBP, sacrifices, etc.
        Original formula: (careerAtBats + careerWalks + careerHitByPitch + careerSacFlies + careerSacBunts)
        """
        return (careerAtBats + careerWalks + careerHitByPitch + careerSacFlies + careerSacBunts)

    @property
    def careerDefensiveChances(self):
        """Sum of outs plus errors for which this player was the fielder (defensive opportunities).
        Original formula: (COUNT(OutEvent WHERE fielderId=this.id) + careerDefensiveErrors)
        """
        return (_COUNT(OutEvent WHERE fielderId==self.id) + careerDefensiveErrors)

    @property
    def careerFieldingPercentage(self):
        """Fielding percentage = (chances - errors) / chances, if chances > 0.
        Original formula: IF(careerDefensiveChances>0) THEN ((careerDefensiveChances - careerDefensiveErrors)/careerDefensiveChances) ELSE null
        """
        return IF(careerDefensiveChances>0) THEN ((careerDefensiveChances - careerDefensiveErrors)/careerDefensiveChances) ELSE None

    @property
    def careerSacBunts(self):
        """Number of successful sacrifice bunts for the player.
        Original formula: COUNT(AtBat WHERE batterId=this.id AND result='SAC_BUNT')
        """
        return _COUNT(AtBat WHERE batterId==self.id  and  result=='SAC_BUNT')

    @property
    def consecutiveGamesPlayedStreak(self):
        """
        Original formula: CALCULATE_CONSECUTIVE_GAMES_PLAYED( this.id )
        """
        return calculate_consecutive_games_played( self.id )

    @property
    def chickenStanceIndicator(self):
        """
        Original formula: EXISTS( WeirdStanceEvent WHERE WeirdStanceEvent.playerId = this.id )
        """
        return _EXISTS( WeirdStanceEvent WHERE WeirdStanceEvent.playerId == self.id )

    @property
    def daysSinceLastRest(self):
        """
        Original formula: CURRENT_DATE - lastRestDate( this.id )
        """
        return CURRENT_DATE - lastRestDate( self.id )

    @property
    def pitchCountLimitReached(self):
        """Check if this player has reached the max pitch count from the rule set, if any.
        Original formula: IF (this.team_id.league_id.ruleSetId.maxPitchCount > 0) THEN (careerPitchCount >= this.team_id.league_id.ruleSetId.maxPitchCount) ELSE false
        """
        return IF (self.team_id.league_id.ruleSetId.maxPitchCount > 0) THEN (careerPitchCount >= self.team_id.league_id.ruleSetId.maxPitchCount) ELSE False

    @property
    def isEligiblePitcher(self):
        """If the player has not exceeded pitch count and is a pitcher, they're still eligible to pitch.
        Original formula: IF ((careerPitchCount < this.team_id.league_id.ruleSetId.maxPitchCount) AND playerIsPitcher=true) THEN true ELSE false
        """
        return IF ((careerPitchCount < self.team_id.league_id.ruleSetId.maxPitchCount)  and  playerIsPitcher==True) THEN True ELSE False

    @property
    def daysRestRequired(self):
        """Some youth leagues require rest days if a pitch limit is reached. Implementation conceptual.
        Original formula: IF (pitchCountLimitReached = true) THEN CALCULATE_REST_DAYS(careerPitchCount, lastTimePitched) ELSE 0
        """
        return IF (pitchCountLimitReached == True) THEN calculate_rest_days(careerPitchCount, lastTimePitched) ELSE 0

    @property
    def isTooOldForLeague(self):
        """Checks if the player is beyond the age limit if the rule set has an overAgeLimit flag. Implementation conceptual.
        Original formula: IF (this.team_id.league_id.ruleSetId.overAgeLimit = true AND BIRTHDATE_CHECK(this.id)) THEN true ELSE false
        """
        return IF (self.team_id.league_id.ruleSetId.overAgeLimit == True  and  BIRTHDATE_CHECK(self.id)) THEN True ELSE False

class DefensivePosition:
    """Plain data container for DefensivePosition entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.positionName = kwargs.get('positionName')

class Game:
    """Plain data container for Game entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.homeTeamId = kwargs.get('homeTeamId')
        self.awayTeamId = kwargs.get('awayTeamId')
        self.status = kwargs.get('status')
        self.ruleSetId = kwargs.get('ruleSetId')

        self.innings = CollectionWrapper(self, 'innings')

    @property
    def currentInningNumber(self):
        """Highest inningNumber in innings that have started or are in progress.
        Original formula: IF innings != null THEN MAX(innings.inningNumber) ELSE null
        """
        return IF innings != None THEN max(innings.inningNumber) ELSE None

    @property
    def runsHome(self):
        """Total runs scored by the home team, summing relevant half-innings for the home offense.
        Original formula: SUM( InningHalf.runsScored for all bottomHalves with offensiveTeamId=homeTeamId )
        """
        return _SUM(InningHalf.runsScored for all bottomHalves with offensiveTeamId==homeTeamId)

    @property
    def runsAway(self):
        """Total runs scored by the away team, summing relevant half-innings for the away offense.
        Original formula: SUM( InningHalf.runsScored for all topHalves with offensiveTeamId=awayTeamId )
        """
        return _SUM(InningHalf.runsScored for all topHalves with offensiveTeamId==awayTeamId)

    @property
    def winnerId(self):
        """If status='FINAL', whichever team has more runs. Null if tie or incomplete.
        Original formula: IF (status='FINAL') THEN (IF runsHome>runsAway THEN homeTeamId ELSE IF runsAway>runsHome THEN awayTeamId ELSE null) ELSE null
        """
        return IF (status=='FINAL') THEN (IF runsHome>runsAway THEN homeTeamId ELSE IF runsAway>runsHome THEN awayTeamId ELSE None) ELSE None

    @property
    def loserId(self):
        """Symmetric aggregator to winnerId; identifies losing team if final and not tied.
        Original formula: IF status='FINAL' AND runsHome!=runsAway THEN (IF winnerId=homeTeamId THEN awayTeamId ELSE homeTeamId) ELSE null
        """
        return IF status=='FINAL'  and  runsHome!=runsAway THEN (IF winnerId==homeTeamId THEN awayTeamId ELSE homeTeamId) ELSE None

    @property
    def totalPitchesInGame(self):
        """Total number of pitches thrown in this game (pure aggregator across all at-bats).
        Original formula: COUNT( Pitch where pitch.atBatId.inningHalfId.inningId.gameId=this.id )
        """
        return _COUNT(Pitch where pitch.atBatId.inningHalfId.inningId.gameId==self.id)

    @property
    def hasWalkOffOpportunity(self):
        """True if it's bottom of 9th+ with the home team trailing/tied so a scoring play could end the game. Implementation conceptual, purely declarative.
        Original formula: EVALUATE_WALKOFF_CONDITION(this.id)
        """
        return EVALUATE_WALKOFF_CONDITION(self.id)

    @property
    def attendance(self):
        """Reference or aggregator for game attendance, e.g., from an external record or data field.
        Original formula: LOOKUP_IN(GameAttendanceRecords, gameId=this.id => attendanceValue)
        """
        return LOOKUP_IN(GameAttendanceRecords, gameId==self.id => attendanceValue)

    @property
    def isExtraInnings(self):
        """Boolean indicating if the game went beyond the 9th inning.
        Original formula: MAX(innings.inningNumber) > 9
        """
        return max(innings.inningNumber) > 9

    @property
    def largestLead(self):
        """Maximum difference in runs between the two teams at any point in this game.
        Original formula: CALCULATE_LARGEST_LEAD(gameId=this.id)
        """
        return calculate_largest_lead(gameId==self.id)

    @property
    def isShutout(self):
        """True if one team finishes with 0 runs (and the game is FINAL).
        Original formula: IF (status='FINAL') THEN ((runsHome==0 AND runsAway>0) OR (runsAway==0 AND runsHome>0)) ELSE false
        """
        return IF (status=='FINAL') THEN ((runsHome==0  and  runsAway>0)  or  (runsAway==0  and  runsHome>0)) ELSE False

    @property
    def shutoutTeamId(self):
        """If the game is a shutout, indicates which team allowed 0 runs. Null if no shutout or tie at 0-0.
        Original formula: IF (isShutout=true) THEN (IF runsHome==0 THEN awayTeamId ELSE IF runsAway==0 THEN homeTeamId ELSE null) ELSE null
        """
        return IF (isShutout==True) THEN (IF runsHome==0 THEN awayTeamId ELSE IF runsAway==0 THEN homeTeamId ELSE None) ELSE None

    @property
    def totalWalksInGame(self):
        """Count of all at-bats with 'result=WALK' in both halves across all innings for this game.
        Original formula: COUNT(AtBat WHERE inningHalfId.inningId.gameId=this.id AND result='WALK')
        """
        return _COUNT(AtBat WHERE inningHalfId.inningId.gameId==self.id  and  result=='WALK')

    @property
    def leadChanges(self):
        """How many times the lead switched from one team to another during this game.
        Original formula: CALCULATE_LEAD_CHANGES(gameId=this.id)
        """
        return calculate_lead_changes(gameId==self.id)

    @property
    def tieCount(self):
        """How many times the score returned to a tie after first pitch.
        Original formula: CALCULATE_TIE_COUNT(gameId=this.id)
        """
        return calculate_tie_count(gameId==self.id)

    @property
    def isTieGameInProgress(self):
        """
        Original formula: (status = 'IN_PROGRESS') AND (runsHome = runsAway)
        """
        return (status == 'IN_PROGRESS')  and  (runsHome == runsAway)

    @property
    def manfredRunnerInEffect(self):
        """
        Original formula: isExtraInnings = true AND leagueImplementsExtraInningRunnerRule( this.id )
        """
        return isExtraInnings == True  and  leagueImplementsExtraInningRunnerRule( self.id )

    @property
    def gameSuspendedDueToWeather(self):
        """
        Original formula: EXISTS( SuspensionEvent WHERE gameId = this.id AND reason = 'WEATHER' )
        """
        return _EXISTS( SuspensionEvent WHERE gameId == self.id  and  reason == 'WEATHER' )

    @property
    def winningPitcherId(self):
        """
        Original formula: CALC_WINNING_PITCHER( this.id )
        """
        return CALC_WINNING_PITCHER( self.id )

    @property
    def hadCycleAchieved(self):
        """
        Original formula: EXISTS( BatterCycleEvent WHERE gameId = this.id )
        """
        return _EXISTS( BatterCycleEvent WHERE gameId == self.id )

    @property
    def isMercyRuleTriggered(self):
        """Indicates if a mercy rule is triggered based on the rule set. If mercyRuleEnabled is true and run differential >= 10 after the specified inning threshold.
        Original formula: IF (this.ruleSetId.mercyRuleEnabled = true AND currentInningNumber >= this.ruleSetId.mercyRuleInningThreshold AND ABS(runsHome - runsAway) >= 10) THEN true ELSE false
        """
        return IF (self.ruleSetId.mercyRuleEnabled == True  and  currentInningNumber >= self.ruleSetId.mercyRuleInningThreshold  and  abs(runsHome - runsAway) >= 10) THEN True ELSE False

    @property
    def limitedInnings(self):
        """Specifies how many total innings are played in this rule set. Some youth leagues play only 6 or 7 innings.
        Original formula: IF (this.ruleSetId.ruleSetName='LittleLeague_2025') THEN 6 ELSE IF (this.ruleSetId.ruleSetName='HighSchool_2025') THEN 7 ELSE 9
        """
        return IF (self.ruleSetId.ruleSetName=='LittleLeague_2025') THEN 6 ELSE IF (self.ruleSetId.ruleSetName=='HighSchool_2025') THEN 7 ELSE 9

    @property
    def tieAllowed(self):
        """Whether a tie is allowed in this rule set if the game is not resolved by a certain time or innings limit.
        Original formula: IF (this.ruleSetId.ruleSetName='Friendly_Rec_League') THEN true ELSE false
        """
        return IF (self.ruleSetId.ruleSetName=='Friendly_Rec_League') THEN True ELSE False

    @property
    def useReplayReview(self):
        """Whether official replay review is permitted in this rule set.
        Original formula: this.ruleSetId.usesReplayReview
        """
        return self.ruleSetId.usesReplayReview

    @property
    def timeLimit(self):
        """Specifies time limit in minutes if enforced. Some youth leagues have a 120 minute limit.
        Original formula: IF (this.ruleSetId.ruleSetName='LittleLeague_2025') THEN 120 ELSE null
        """
        return IF (self.ruleSetId.ruleSetName=='LittleLeague_2025') THEN 120 ELSE None

    @property
    def homeTeamBatsFirst(self):
        """Some special tournaments might let the home team bat first. Usually false in standard baseball.
        Original formula: IF (this.ruleSetId.ruleSetName='SpecialTournament_2025') THEN true ELSE false
        """
        return IF (self.ruleSetId.ruleSetName=='SpecialTournament_2025') THEN True ELSE False

    @property
    def skipBottomIfLeading(self):
        """If true, skip bottom half if the home team is ahead after top of final inning. This is the standard MLB end condition, but some leagues do it differently.
        Original formula: IF (this.ruleSetId.ruleSetName='College_2025') THEN true ELSE false
        """
        return IF (self.ruleSetId.ruleSetName=='College_2025') THEN True ELSE False

class Inning:
    """Plain data container for Inning entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.gameId = kwargs.get('gameId')
        self.inningNumber = kwargs.get('inningNumber')

    @property
    def isComplete(self):
        """True if top and bottom half are both complete, or if there's a walk-off scenario that ends the inning early.
        Original formula: top.isComplete AND (bottom==null OR bottom.isComplete)
        """
        return top.isComplete  and  (bottom==None  or  bottom.isComplete)

    @property
    def runsThisInning(self):
        """Sum of runs in top and bottom half of this inning.
        Original formula: (IF top!=null THEN top.runsScored ELSE 0) + (IF bottom!=null THEN bottom.runsScored ELSE 0)
        """
        return (IF top!=None THEN top.runsScored ELSE 0) + (IF bottom!=None THEN bottom.runsScored ELSE 0)

    @property
    def averageExitVelocityInInning(self):
        """Mean exit velocity of all batted balls (AtBat.exitVelocity) in top+bottom halves of this inning.
        Original formula: AVG(AtBat where AtBat.inningHalfId.inningId=this.id => exitVelocity)
        """
        return _AVG(AtBat where AtBat.inningHalfId.inningId==self.id => exitVelocity)

    @property
    def totalWalksInInning(self):
        """Count of at-bats with 'result=WALK' in the top and bottom half of this inning combined.
        Original formula: COUNT(AtBat where AtBat.inningHalfId.inningId=this.id AND result='WALK')
        """
        return _COUNT(AtBat where AtBat.inningHalfId.inningId==self.id  and  result=='WALK')

    @property
    def isSeventhInningStretch(self):
        """
        Original formula: inningNumber = 7
        """
        return inningNumber == 7

    @property
    def balksInInning(self):
        """
        Original formula: COUNT( BalkEvent WHERE BalkEvent.inningId = this.id )
        """
        return _COUNT(BalkEvent WHERE BalkEvent.inningId == self.id)

    @property
    def stealAttemptsInInning(self):
        """
        Original formula: COUNT( StealAttemptEvent WHERE StealAttemptEvent.inningId = this.id )
        """
        return _COUNT(StealAttemptEvent WHERE StealAttemptEvent.inningId == self.id)

    @property
    def runnersAdvancedOnWildPitch(self):
        """
        Original formula: COUNT( RunnerAdvanceEvent WHERE reason = 'WILD_PITCH' AND inningId = this.id )
        """
        return _COUNT(RunnerAdvanceEvent WHERE reason == 'WILD_PITCH'  and  inningId == self.id)

    @property
    def largestLeadAtAnyPointThisInning(self):
        """
        Original formula: MAX( leadDifferentialDuringInning( this.id ) )
        """
        return max( leadDifferentialDuringInning( self.id ) )

class InningHalf:
    """Plain data container for InningHalf entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.halfType = kwargs.get('halfType')
        self.offensiveTeamId = kwargs.get('offensiveTeamId')
        self.defensiveTeamId = kwargs.get('defensiveTeamId')
        self.outs = kwargs.get('outs')
        self.runsScored = kwargs.get('runsScored')
        self.isComplete = kwargs.get('isComplete')

        self.atBats = CollectionWrapper(self, 'atBats')

    @property
    def battersFaced(self):
        """Number of batters who came up to the plate (size of atBats).
        Original formula: COUNT(atBats)
        """
        return _COUNT(atBats)

    @property
    def hitsInHalf(self):
        """How many hits (1B,2B,3B,HR) occurred in this half.
        Original formula: COUNT( AtBat where (inningHalfId=this.id AND result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN']) )
        """
        return _COUNT(AtBat where (inningHalfId==self.id  and  result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN']) )

    @property
    def leftOnBase(self):
        """How many baserunners remained stranded when the half-inning ended. Implementation conceptual, purely aggregator over base-runner state.
        Original formula: CALCULATE_STRANDED_RUNNERS(this.id)
        """
        return calculate_stranded_runners(self.id)

    @property
    def walksInHalf(self):
        """Count of at-bats with 'result= WALK' in this half-inning.
        Original formula: COUNT(AtBat where inningHalfId=this.id AND result='WALK')
        """
        return _COUNT(AtBat where inningHalfId==self.id  and  result=='WALK')

    @property
    def hitByPitchInHalf(self):
        """Count of at-bats with 'result=HIT_BY_PITCH' in this half-inning.
        Original formula: COUNT(AtBat where inningHalfId=this.id AND result='HIT_BY_PITCH')
        """
        return _COUNT(AtBat where inningHalfId==self.id  and  result=='HIT_BY_PITCH')

    @property
    def mostPitchesFacedBySingleBatter(self):
        """The maximum pitch count in any single AtBat within this half-inning.
        Original formula: MAX(atBats.pitchCountInAtBat)
        """
        return max(atBats.pitchCountInAtBat)

    @property
    def hitsWithExitVelocityAbove90(self):
        """Number of hits in this half-inning that had exitVelocity > 90 mph.
        Original formula: COUNT(AtBat where inningHalfId=this.id AND exitVelocity>90 AND result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN'])
        """
        return _COUNT(AtBat where inningHalfId==self.id  and  exitVelocity>90  and  result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN'])

    @property
    def catchersInterferenceCalls(self):
        """
        Original formula: COUNT( AtBat WHERE inningHalfId = this.id AND result = 'CATCHER_INTERFERENCE' )
        """
        return _COUNT(AtBat WHERE inningHalfId == self.id  and  result == 'CATCHER_INTERFERENCE')

    @property
    def batterInterferenceCalls(self):
        """
        Original formula: COUNT( AtBat WHERE inningHalfId = this.id AND result = 'BATTER_INTERFERENCE' )
        """
        return _COUNT(AtBat WHERE inningHalfId == self.id  and  result == 'BATTER_INTERFERENCE')

    @property
    def sacrificeBuntsInHalf(self):
        """
        Original formula: COUNT( AtBat WHERE inningHalfId = this.id AND result = 'SAC_BUNT' )
        """
        return _COUNT(AtBat WHERE inningHalfId == self.id  and  result == 'SAC_BUNT')

    @property
    def infieldFlyCallsInHalf(self):
        """
        Original formula: COUNT( AtBat WHERE inningHalfId = this.id AND specialCall = 'INFIELD_FLY' )
        """
        return _COUNT(AtBat WHERE inningHalfId == self.id  and  specialCall == 'INFIELD_FLY')

    @property
    def mustEndDueToMercyRule(self):
        """If the game-level aggregator isMercyRuleTriggered is true, this half-inning must end immediately.
        Original formula: IF (this.inningId.gameId.isMercyRuleTriggered = true) THEN true ELSE false
        """
        return IF (self.inningId.gameId.isMercyRuleTriggered == True) THEN True ELSE False

    @property
    def stealingAllowed(self):
        """Indicates if base stealing is allowed. Some youth leagues restrict leads or steals entirely.
        Original formula: this.inningId.gameId.ruleSetId.allowLeadingOff
        """
        return self.inningId.gameId.ruleSetId.allowLeadingOff

class AtBat:
    """Plain data container for AtBat entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.inningHalfId = kwargs.get('inningHalfId')
        self.batterId = kwargs.get('batterId')
        self.pitcherId = kwargs.get('pitcherId')
        self.result = kwargs.get('result')
        self.rbi = kwargs.get('rbi')
        self.exitVelocity = kwargs.get('exitVelocity')
        self.launchAngle = kwargs.get('launchAngle')

        self.pitches = CollectionWrapper(self, 'pitches')

    @property
    def pitchCountInAtBat(self):
        """Number of pitches thrown in this at-bat.
        Original formula: COUNT(pitches)
        """
        return _COUNT(pitches)

    @property
    def fouls(self):
        """Number of foul pitches among 'pitches'.
        Original formula: COUNT( Pitch where (atBatId=this.id AND pitchResult='FOUL') )
        """
        return _COUNT(Pitch where (atBatId==self.id  and  pitchResult=='FOUL') )

    @property
    def expectedBattingAverage(self):
        """A sabermetric measure (xBA) based on exit velocity, launch angle, etc. Implementation conceptual, purely aggregator.
        Original formula: SABERMETRIC_xBA_FORMULA(this.id)
        """
        return SABERMETRIC_xBA_FORMULA(self.id)

    @property
    def wasWalk(self):
        """Boolean aggregator: true if result='WALK'.
        Original formula: result == 'WALK'
        """
        return result == 'WALK'

    @property
    def plateDisciplineIndex(self):
        """Conceptual measure of a batter's plate discipline for this at-bat, e.g. proportion of 'chases' outside the zone vs. total pitches.
        Original formula: CALC_PLATE_DISCIPLINE(atBatId=this.id)
        """
        return CALC_PLATE_DISCIPLINE(atBatId==self.id)

    @property
    def numberOfBalls(self):
        """Count of pitches in this at-bat where pitchResult='BALL'.
        Original formula: COUNT( Pitch where atBatId=this.id AND pitchResult='BALL')
        """
        return _COUNT(Pitch where atBatId==self.id  and  pitchResult=='BALL')

    @property
    def strikeCount(self):
        """NEW: The count of pitches that are strikes: CALLED_STRIKE, SWINGING_STRIKE, or FOUL.
        Original formula: COUNT(Pitch where atBatId=this.id AND pitchResult IN ['CALLED_STRIKE','SWINGING_STRIKE','FOUL'])
        """
        return _COUNT(Pitch where atBatId==self.id  and  pitchResult in ['CALLED_STRIKE','SWINGING_STRIKE','FOUL'])

    @property
    def ballCount(self):
        """NEW: The count of pitches that are balls.
        Original formula: numberOfBalls
        """
        return numberOfBalls

    @property
    def batterHasStruckOut(self):
        """NEW: True if strikeCount >= 3.
        Original formula: strikeCount >= 3
        """
        return strikeCount >= 3

    @property
    def batterHasWalked(self):
        """NEW: True if ballCount >= 4.
        Original formula: ballCount >= 4
        """
        return ballCount >= 4

class Pitch:
    """Plain data container for Pitch entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.atBatId = kwargs.get('atBatId')
        self.pitchResult = kwargs.get('pitchResult')
        self.pitchVelocity = kwargs.get('pitchVelocity')
        self.pitchSpinRate = kwargs.get('pitchSpinRate')

    @property
    def isStrike(self):
        """Boolean aggregator: true if pitchResult is CALLED_STRIKE or SWINGING_STRIKE. Implementation conceptual.
        Original formula: pitchResult IN ['CALLED_STRIKE','SWINGING_STRIKE']
        """
        return pitchResult in ['CALLED_STRIKE','SWINGING_STRIKE']

    @property
    def isQualityPitch(self):
        """True if pitchVelocity > 95 and pitchSpinRate > 2200, purely an example threshold-based aggregator.
        Original formula: pitchVelocity>95 AND pitchSpinRate>2200
        """
        return pitchVelocity>95  and  pitchSpinRate>2200

    @property
    def adjustedSpinRate(self):
        """Derived spin rate that might account for velocity or environmental factors. Implementation conceptual.
        Original formula: pitchSpinRate * ADJUSTMENT_FACTOR(pitchVelocity)
        """
        return pitchSpinRate * ADJUSTMENT_FACTOR(pitchVelocity)

    @property
    def isWildPitch(self):
        """
        Original formula: pitchResult = 'WILD_PITCH'
        """
        return pitchResult == 'WILD_PITCH'

class Statistic:
    """Plain data container for Statistic entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.entityType = kwargs.get('entityType')
        self.entityId = kwargs.get('entityId')
        self.statName = kwargs.get('statName')
        self.statValue = kwargs.get('statValue')
        self.season = kwargs.get('season')
        self.lastUpdated = kwargs.get('lastUpdated')

class Stadium:
    """Plain data container for Stadium entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.stadiumName = kwargs.get('stadiumName')
        self.capacity = kwargs.get('capacity')

    @property
    def gamesPlayedInStadium(self):
        """Number of games that have taken place in this stadium. Implementation conceptual, would require a link from Game to Stadium.
        Original formula: COUNT(Game where Game.stadiumId = this.id)
        """
        return _COUNT(Game where Game.stadiumId == self.id)

    @property
    def averageAttendance(self):
        """Average attendance across all games played here. Implementation conceptual.
        Original formula: AVG(GameAttendanceRecords where stadiumId=this.id)
        """
        return _AVG(GameAttendanceRecords where stadiumId==self.id)

    @property
    def mostRunsInSingleGame(self):
        """Maximum total runs (home + away) for any game played in this stadium.
        Original formula: MAX( Game where stadiumId=this.id => (runsHome + runsAway) )
        """
        return max( Game where stadiumId==self.id => (runsHome + runsAway) )

    @property
    def averageHRPerGame(self):
        """Average number of home runs per game in this stadium. Implementation conceptual if we track HR data by stadium.
        Original formula: AVG(Game => totalHRsInGame) WHERE stadiumId=this.id
        """
        return _AVG(Game => totalHRsInGame) WHERE stadiumId==self.id

    @property
    def daysSinceLastGame(self):
        """Time (in days) since the most recent game played here. Implementation conceptual—compares current date to the MAX(gameDate).
        Original formula: CURRENT_DATE - MAX(Game where stadiumId=this.id => gameDate)
        """
        return CURRENT_DATE - max(Game where stadiumId==self.id => gameDate)

class OutEvent:
    """Plain data container for OutEvent entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.inningHalfId = kwargs.get('inningHalfId')
        self.atBatId = kwargs.get('atBatId')

class RunEvent:
    """Plain data container for RunEvent entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.inningHalfId = kwargs.get('inningHalfId')
        self.atBatId = kwargs.get('atBatId')
        self.runCount = kwargs.get('runCount')

class Season:
    """Plain data container for Season entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.seasonName = kwargs.get('seasonName')
        self.startDate = kwargs.get('startDate')
        self.endDate = kwargs.get('endDate')

        self.seasonGames = CollectionWrapper(self, 'seasonGames')

    @property
    def gamesInSeason(self):
        """Counts how many games are in this season (pure aggregator).
        Original formula: COUNT(seasonGames)
        """
        return _COUNT(seasonGames)

class SeasonTeamStats:
    """Plain data container for SeasonTeamStats entities."""
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.seasonId = kwargs.get('seasonId')
        self.teamId = kwargs.get('teamId')

    @property
    def teamWinningStreak(self):
        """Longest consecutive wins streak for the team during this season. Implementation conceptual.
        Original formula: CALCULATE_MAX_WIN_STREAK(teamId, seasonId)
        """
        return calculate_max_win_streak(teamId, seasonId)

    @property
    def runDifferential(self):
        """Runs scored minus runs allowed by a team in a given season.
        Original formula: (SUM(Game[seasonId=this.seasonId AND (homeTeamId=this.teamId OR awayTeamId=this.teamId) => runsScoredByTeam]) - SUM(Game[seasonId=this.seasonId AND (homeTeamId=this.teamId OR awayTeamId=this.teamId) => runsAllowedByTeam]))
        """
        return (_SUM(Game[seasonId==self.seasonId  and  (homeTeamId==self.teamId  or  awayTeamId==self.teamId) => runsScoredByTeam]) - _SUM(Game[seasonId==self.seasonId  and  (homeTeamId==self.teamId  or  awayTeamId==self.teamId) => runsAllowedByTeam]))

class RuleSet:
    """Plain data container for RuleSet entities."""
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
