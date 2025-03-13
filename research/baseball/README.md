# Baseball ToE Meta-Model
## A 100% Declarative Framework for the Sport's Structures and Rules

A unified meta-model capturing the entire domain of baseball—teams, players, games, innings, stats, and rules—within a purely declarative structure. All domain logic—like scoring, outs, pitch outcomes, lineups, or statistics—are expressed using lookups, aggregations, constraints, and event-based facts—no imperative instructions.

**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Baseball

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
The Baseball extension of the CMCC (Conceptual Model Completeness Conjecture) systematically represents baseball’s core objects—Teams, Players, Games, Innings, At-Bats—under a single Snapshot-Consistent schema. We’ve rewritten the entire specification to be 100% declarative, replacing stepwise imperative logic with event-based or aggregator-based facts. Everything from run scoring, outs, pitch results, and roster assignments is specified as constraints, lookups, aggregator fields, or derived booleans—ensuring that the model is purely descriptive. No domain logic is expressed as do-this-then-do-that instructions.

![Baseball ToE Meta-Model Entity Diagram](baseball.png)


### Key Points
- Models baseball’s entire rule structure—teams, rosters, innings, batting orders, stats—declaratively with aggregator formulas, event-based facts, and constraints.
- Eliminates the need for any imperative code blocks or specialized DSL instructions.
- Demonstrates flexibility for advanced sabermetrics, tying directly into this purely factual data structure.
- Seamlessly integrates with other CMCC domains (e.g., economics or sociology) for cross-domain synergy.

### Implications
- Provides a universal environment for capturing baseball rules in a purely fact-based manner.
- Greatly simplifies or eliminates stateful code, since all logic is derived from the presence/absence of events or stated data.
- Supports advanced analytics—once in the data, aggregator fields can unify everything from pitch-level detail to multi-season advanced metrics.

### Narrative
#### Purely Declarative Baseball Extension
In this version, we removed all imperative instructions (e.g., 'increment outs', 'set status') and replaced them with aggregator fields or constraints referencing new event entities or pre-existing relationships. For instance, an InningHalf’s outs are now simply the count of 'OutEvent' records referencing that half-inning. A game is 'in progress' if certain conditions in the data hold (status='IN_PROGRESS' AND we haven't reached final conditions). No procedure calls are needed to change states; the data itself drives the logic. This architecture helps ensure the system remains consistent and transparent: any change to the data is automatically reflected in the aggregator fields, with no hidden or procedural steps to update them.


---

# Schema Overview

## Entity: League

**Description**: Represents an organized group of baseball teams playing under the same rule set. Could be MLB, minor leagues, or an amateur league.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **leagueName**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **teams**  
  *Target Entity:* Team, *Type:* one_to_many  
    
  (Join condition: **Team.league_id = this.id**)  
  *Description:* Collection of Teams belonging to this league.

### Aggregations
- **teamCount**  
  *Description:* Number of teams in this league.  
  *Formula:* `COUNT(teams)`
- **totalGamesPlayed**  
  *Description:* Sum of all Games completed by all Teams in the league. Implementation conceptual, scanning each team's 'gamesPlayed'.  
  *Formula:* `SUM(teams.gamesPlayed)`
- **bestTeam**  
  *Description:* The team with the highest win percentage in this league (declarative aggregator).  
  *Formula:* `MAXBY(teams, t => t.winPercentage)`
- **worstTeam**  
  *Description:* The team with the lowest win percentage in this league (declarative aggregator).  
  *Formula:* `MINBY(teams, t => t.winPercentage)`
- **averageTeamERA**  
  *Description:* The average ERA across all teams in this league. Implementation conceptual, could sum or average pitchers’ ERA or overall team ERA.  
  *Formula:* `AVG(teams -> eachTeamERA)`
- **totalLeagueHomeRuns**  
  *Description:* The sum of all home runs hit by players on all teams in this league, purely data-based aggregator.  
  *Formula:* `SUM(teams.roster -> careerHomeRuns)`
- **totalLeagueStolenBases**  
  *Description:* The sum of all stolen bases by players on all teams in this league.  
  *Formula:* `SUM(teams.roster -> careerStolenBases)`

### Lambdas
- **scheduleMatchups**
    
  *Formula:* `ALL_PAIRINGS(teams) => SHOULD_HAVE_ScheduledMatchup`


---

## Entity: Team

**Description**: A baseball team. Belongs to one League, has a roster of Players, and competes in Games.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **teamName**  
  *Type:* scalar, *Datatype:* string  
  
- **league_id**  
  *Type:* lookup, *Datatype:*   
  

### Lookups
- **roster**  
  *Target Entity:* Player, *Type:* one_to_many  
    
  (Join condition: **Player.team_id = this.id**)  
  *Description:* All players currently on the team.

### Aggregations
- **rosterSize**  
  *Description:* Number of players on the team's active roster.  
  *Formula:* `COUNT(roster)`
- **gamesPlayed**  
  *Description:* Number of Games in which this team has participated (data-based aggregator).  
  *Formula:* `COUNT(Game where (homeTeamId=this.id OR awayTeamId=this.id))`
- **wins**  
  *Description:* Count of Games this team has won (pure aggregator, no imperative updates).  
  *Formula:* `COUNT(Game where (winnerId=this.id))`
- **losses**  
  *Description:* Count of Games this team has lost.  
  *Formula:* `COUNT(Game where (loserId=this.id))`
- **winPercentage**  
  *Description:* wins / (wins + losses), if any games played. Null otherwise.  
  *Formula:* `IF (gamesPlayed>0) THEN (wins / gamesPlayed) ELSE null`
- **averageTeamBattingAverage**  
  *Description:* The average batting average among all players on the roster, purely aggregator.  
  *Formula:* `AVG(roster.careerBattingAverage)`
- **totalTeamRuns**  
  *Description:* Total runs scored by this team (across all games). Implementation conceptual.  
  *Formula:* `SUM(GameInnings where offense=this.id => runsScored )`
- **totalTeamHomeRuns**  
  *Description:* Sum of home runs hit by all players on this team.  
  *Formula:* `SUM(roster -> careerHomeRuns)`
- **totalTeamStolenBases**  
  *Description:* Sum of stolen bases by all players on this team.  
  *Formula:* `SUM(roster -> careerStolenBases)`
- **averageFieldingPercentage**  
  *Description:* The team’s overall fielding percentage, averaging all players’ fielding percentages who actively field.  
  *Formula:* `AVG(roster -> careerFieldingPercentage )`
- **winningPercentageInStadium**  
  *Description:* Team’s historical winning percentage in a given stadium—pure aggregator referencing stadium-based game data.  
  *Formula:* `WIN_PCT_BY_STADIUM_FUNCTION(this.id)`

### Lambdas
- **addPlayerToRoster**
  (Parameters: player_id)  
  *Formula:* `Player(team_id=player_id).team_id == this.id`
- **removePlayerFromRoster**
  (Parameters: player_id)  
  *Formula:* `Player(player_id).team_id == null`


---

## Entity: Player

**Description**: An individual who participates in baseball games, either as a position player, pitcher, or both.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **fullName**  
  *Type:* scalar, *Datatype:* string  
  
- **battingHand**  
  *Type:* scalar, *Datatype:* string  
  
- **throwingHand**  
  *Type:* scalar, *Datatype:* string  
  
- **team_id**  
  *Type:* lookup, *Datatype:*   
  

### Lookups
- **defensivePositions**  
  *Target Entity:* DefensivePosition, *Type:* many_to_many  
    
    
  *Description:* All possible defensive positions the player can handle. Implementation: PlayerPosition join table or similar.

### Aggregations
- **careerAtBats**  
  *Description:* How many official at-bats the player has had across all games.  
  *Formula:* `COUNT( AtBat where (batterId=this.id) )`
- **careerHits**  
  *Description:* How many hits the player has recorded across all at-bats.  
  *Formula:* `COUNT( AtBat where (batterId=this.id AND result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN']) )`
- **careerBattingAverage**  
  *Description:* (careerHits / careerAtBats). Null if no at-bats.  
  *Formula:* `IF (careerAtBats>0) THEN (careerHits / careerAtBats) ELSE null`
- **careerPitchCount**  
  *Description:* Total number of pitches thrown by this player, if a pitcher.  
  *Formula:* `COUNT( Pitch where (pitcherId=this.id) )`
- **careerStrikeoutsPitched**  
  *Description:* How many strikeouts the player (as pitcher) has recorded.  
  *Formula:* `COUNT( AtBat where (pitcherId=this.id AND result='STRIKEOUT') )`
- **careerInningsPitched**  
  *Description:* Summation of partial innings if the player is a pitcher. Implementation conceptual.  
  *Formula:* `AccumulateInningsFromOuts( sum_of_outs_where_pitcherId=this.id )`
- **onBasePercentage**  
  *Description:* OBP = (H + BB + HBP) / (AB + BB + HBP + SF). Implementation conceptual if advanced data is tracked.  
  *Formula:* `IF (plateAppearances>0) THEN ((careerHits + careerWalks + careerHitByPitch) / (careerAtBats + careerWalks + careerHitByPitch + careerSacFlies)) ELSE null`
- **sluggingPercentage**  
  *Description:* Total bases / at-bats. Implementation conceptual if we track 2B,3B,HR, etc.  
  *Formula:* `IF (careerAtBats>0) THEN (sumOfTotalBases / careerAtBats) ELSE null`
- **ops**  
  *Description:* On-base plus slugging, purely aggregator of the OBP + SLG fields.  
  *Formula:* `onBasePercentage + sluggingPercentage`
- **stolenBasePercentage**  
  *Description:* stolenBases / (stolenBases + caughtStealing). Implementation conceptual if we track that data.  
  *Formula:* `IF ((careerStolenBases + careerCaughtStealing) > 0) THEN (careerStolenBases / (careerStolenBases + careerCaughtStealing)) ELSE null`
- **isTwoWayPlayer**  
  *Description:* Boolean indicating if the player has pitched and also batted as a regular hitter. Implementation conceptual.  
  *Formula:* `IF (careerInningsPitched > 0 AND careerAtBats > 0) THEN true ELSE false`

### Lambdas
- **adjustBattingHand**
  (Parameters: newHand)  
  *Formula:* `this.battingHand == newHand`


---

## Entity: DefensivePosition

**Description**: A position on the baseball field, e.g. pitcher (1), catcher (2), shortstop (6), etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **positionName**  
  *Type:* scalar, *Datatype:* string  
  





---

## Entity: Game

**Description**: Represents a single baseball game between two Teams, split into innings (top & bottom).

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **homeTeamId**  
  *Type:* lookup, *Datatype:*   
  
- **awayTeamId**  
  *Type:* lookup, *Datatype:*   
  
- **status**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **innings**  
  *Target Entity:* Inning, *Type:* one_to_many  
    
  (Join condition: **Inning.gameId = this.id**)  
  *Description:* All Inning records associated with this Game.

### Aggregations
- **currentInningNumber**  
  *Description:* Highest inningNumber in innings that have started or are in progress.  
  *Formula:* `IF innings != null THEN MAX(innings.inningNumber) ELSE null`
- **runsHome**  
  *Description:* Total runs scored by the home team, summing relevant half-innings for the home offense.  
  *Formula:* `SUM( InningHalf.runsScored for all bottomHalves with offensiveTeamId=homeTeamId )`
- **runsAway**  
  *Description:* Total runs scored by the away team, summing relevant half-innings for the away offense.  
  *Formula:* `SUM( InningHalf.runsScored for all topHalves with offensiveTeamId=awayTeamId )`
- **winnerId**  
  *Description:* If status='FINAL', whichever team has more runs. Null if tie or incomplete.  
  *Formula:* `IF (status='FINAL') THEN (IF runsHome>runsAway THEN homeTeamId ELSE IF runsAway>runsHome THEN awayTeamId ELSE null) ELSE null`
- **loserId**  
  *Description:* Symmetric aggregator to winnerId; identifies losing team if final and not tied.  
  *Formula:* `IF status='FINAL' AND runsHome!=runsAway THEN (IF winnerId=homeTeamId THEN awayTeamId ELSE homeTeamId) ELSE null`
- **totalPitchesInGame**  
  *Description:* Total number of pitches thrown in this game (pure aggregator across all at-bats).  
  *Formula:* `COUNT( Pitch where pitch.atBatId.inningHalfId.inningId.gameId=this.id )`
- **hasWalkOffOpportunity**  
  *Description:* True if it's bottom of 9th+ with the home team trailing/tied so a scoring play could end the game. Implementation conceptual, purely declarative.  
  *Formula:* `EVALUATE_WALKOFF_CONDITION(this.id)`

### Lambdas
- **startGame**
    
  *Formula:* `IF (EXISTS(any pitch or any top inning started)) THEN (this.status == 'IN_PROGRESS')`
- **endGame**
    
  *Formula:* `IF (CONDITIONS_FOR_GAME_COMPLETION) THEN (this.status == 'FINAL')`

### Constraints
- **teamMismatch**  
  *Formula:* `homeTeamId != awayTeamId`  
  *Error Message:* Home and away team cannot be the same.

---

## Entity: Inning

**Description**: A single inning in the game, typically has a top and bottom half unless extras are needed.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **gameId**  
  *Type:* lookup, *Datatype:*   
  
- **inningNumber**  
  *Type:* scalar, *Datatype:* integer  
  

### Lookups
- **top**  
  *Target Entity:* InningHalf, *Type:* one_to_one  
    
    
  *Description:* The top half of this inning, if defined.
- **bottom**  
  *Target Entity:* InningHalf, *Type:* one_to_one  
    
    
  *Description:* The bottom half of this inning, if defined.

### Aggregations
- **isComplete**  
  *Description:* True if top and bottom half are both complete, or if there's a walk-off scenario that ends the inning early.  
  *Formula:* `top.isComplete AND (bottom==null OR bottom.isComplete)`



---

## Entity: InningHalf

**Description**: Represents either top or bottom portion of an inning, with outs, runs, at-bats, etc. All purely event/aggregator based.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **halfType**  
  *Type:* scalar, *Datatype:* string  
  
- **offensiveTeamId**  
  *Type:* lookup, *Datatype:*   
  
- **defensiveTeamId**  
  *Type:* lookup, *Datatype:*   
  
- **outs**  
  *Type:* scalar, *Datatype:* integer  
  
- **runsScored**  
  *Type:* scalar, *Datatype:* integer  
  
- **isComplete**  
  *Type:* scalar, *Datatype:* boolean  
  

### Lookups
- **atBats**  
  *Target Entity:* AtBat, *Type:* one_to_many  
    
  (Join condition: **AtBat.inningHalfId = this.id**)  
  *Description:* All plate appearances in this half-inning.

### Aggregations
- **battersFaced**  
  *Description:* Number of batters who came up to the plate (size of atBats).  
  *Formula:* `COUNT(atBats)`
- **hitsInHalf**  
  *Description:* How many hits (1B,2B,3B,HR) occurred in this half.  
  *Formula:* `COUNT( AtBat where (inningHalfId=this.id AND result in ['SINGLE','DOUBLE','TRIPLE','HOMERUN']) )`
- **leftOnBase**  
  *Description:* How many baserunners remained stranded when the half-inning ended. Implementation conceptual, purely aggregator over base-runner state.  
  *Formula:* `CALCULATE_STRANDED_RUNNERS(this.id)`

### Lambdas
- **recordOut**
    
  *Formula:* `InningHalf.outs = COUNT(OutEvent where outEvent.inningHalfId=this.id)`
- **scoreRun**
  (Parameters: count)  
  *Formula:* `InningHalf.runsScored = SUM(RunEvent where runEvent.inningHalfId=this.id => runEvent.runCount)`

### Constraints
- **validOutCount**  
  *Formula:* `outs >= 0 AND outs <= 3`  
  *Error Message:* Outs must be between 0 and 3 inclusive.
- **isCompleteWhen3OutsOrWalkoff**  
  *Formula:* `isComplete == ((outs >= 3) OR (CHECK_WALKOFF_CONDITION(this.id)))`  
  *Error Message:* Half-inning completes with 3 outs or a declared walk-off event.

---

## Entity: AtBat

**Description**: A single plate appearance, from the start of the batter's turn to its final result. All logic is aggregator-based, no step-by-step updates.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **inningHalfId**  
  *Type:* lookup, *Datatype:*   
  
- **batterId**  
  *Type:* lookup, *Datatype:*   
  
- **pitcherId**  
  *Type:* lookup, *Datatype:*   
  
- **result**  
  *Type:* scalar, *Datatype:* string  
  
- **rbi**  
  *Type:* scalar, *Datatype:* integer  
  

### Lookups
- **pitches**  
  *Target Entity:* Pitch, *Type:* one_to_many  
    
  (Join condition: **Pitch.atBatId = this.id**)  
  *Description:* All Pitch records thrown in this at-bat.

### Aggregations
- **pitchCountInAtBat**  
  *Description:* Number of pitches thrown in this at-bat.  
  *Formula:* `COUNT(pitches)`
- **fouls**  
  *Description:* Number of foul pitches among 'pitches'.  
  *Formula:* `COUNT( Pitch where (atBatId=this.id AND pitchResult='FOUL') )`
- **expectedBattingAverage**  
  *Description:* A sabermetric measure (xBA) based on exit velocity, launch angle, etc. Implementation conceptual, purely aggregator.  
  *Formula:* `SABERMETRIC_xBA_FORMULA(this.id)`

### Lambdas
- **addPitch**
  (Parameters: pitchData)  
  *Formula:* `Pitch.atBatId == this.id => belongs to 'pitches' collection`
- **finalizeAtBat**
    
  *Formula:* `AtBatIsComplete(this.id) == (this.result != null)`


---

## Entity: Pitch

**Description**: Represents a single pitch thrown in an at-bat. Tracks velocity, location, outcome, etc., with no imperative instructions.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **atBatId**  
  *Type:* lookup, *Datatype:*   
  
- **pitchResult**  
  *Type:* scalar, *Datatype:* string  
  
- **pitchVelocity**  
  *Type:* scalar, *Datatype:* number  
  
- **pitchSpinRate**  
  *Type:* scalar, *Datatype:* number  
  





---

## Entity: Statistic

**Description**: Generic or specialized statistical measures referencing a Player, Team, or entire league. Could store advanced sabermetrics or simpler metrics.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **entityType**  
  *Type:* scalar, *Datatype:* string  
  
- **entityId**  
  *Type:* lookup, *Datatype:*   
  
- **statName**  
  *Type:* scalar, *Datatype:* string  
  
- **statValue**  
  *Type:* scalar, *Datatype:* number  
  
- **season**  
  *Type:* scalar, *Datatype:* string  
  
- **lastUpdated**  
  *Type:* scalar, *Datatype:* datetime  
  





---

## Entity: Stadium

**Description**: Represents a ballpark or stadium where games are played. Purely declarative references to capacity, location, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **stadiumName**  
  *Type:* scalar, *Datatype:* string  
  
- **capacity**  
  *Type:* scalar, *Datatype:* integer  
  


### Aggregations
- **gamesPlayedInStadium**  
  *Description:* Number of games that have taken place in this stadium. Implementation conceptual, would require a link from Game to Stadium.  
  *Formula:* `COUNT(Game where Game.stadiumId = this.id)`
- **averageAttendance**  
  *Description:* Average attendance across all games played here. Implementation conceptual.  
  *Formula:* `AVG(GameAttendanceRecords where stadiumId=this.id)`



---

## Entity: OutEvent

**Description**: // NEW: Fact-based approach for recording outs. Each OutEvent references which half-inning or at-bat triggered the out. Eliminates imperative increments.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **inningHalfId**  
  *Type:* lookup, *Datatype:*   
  
- **atBatId**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: RunEvent

**Description**: // NEW: Fact-based approach for runs. Each RunEvent references which half-inning or at-bat triggered a run, ensuring no imperative 'scoreRun()'.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **inningHalfId**  
  *Type:* lookup, *Datatype:*   
  
- **atBatId**  
  *Type:* lookup, *Datatype:*   
  
- **runCount**  
  *Type:* scalar, *Datatype:* integer  
  





---