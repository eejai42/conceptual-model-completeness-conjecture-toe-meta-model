# Baseball ToE Meta-Model
## A Unified Declarative Framework for the Sport's Structures and Rules

A unified meta-model capturing the entire domain of baseball—teams, players, games, innings, stats, and rules—within a single Snapshot-Consistent, declarative structure. All domain logic—like scoring, outs, pitch outcomes, lineups, or statistics—are expressed using lookups, aggregations, lambdas, and constraints.

**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Baseball

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
The Baseball extension of the CMCC (Conceptual Model Completeness Conjecture) systematically represents baseball’s core objects—Teams, Players, Games, Innings, At-Bats—under a single Snapshot-Consistent schema. Using five foundational primitives (S, D, L, A, F), it encodes rules around scoring, outs, pitching results, roster management, and advanced stats, enabling cross-system synergy and easy maintenance. Everything from ball/strike logic to multi-season aggregated metrics can be modeled and updated as purely declarative data, removing the need for domain-specific baseball DSLs or ad hoc, code-scattered rules.

![Baseball ToE Meta-Model Entity Diagram](baseball.png)


### Key Points
- Models baseball’s entire rule structure—teams, rosters, innings, batting orders, stats—declaratively with aggregator formulas, lambdas, and constraints.
- Eliminates the need for dedicated baseball-simulation languages by storing the 'what' (the game logic) as first-class data relationships.
- Demonstrates flexibility for advanced sabermetrics: from pitch-level detail to advanced team-level analytics.
- Seamlessly integrates with other CMCC domains (e.g., economics or sociology) for cross-domain synergy (financial aspects of baseball, fan demographics, etc.).

### Implications
- Provides a universal environment for capturing the rules of baseball—from simple youth-league style to MLB-level detail.
- Easily extended or internationalized (e.g., minor league variants, overseas leagues) without rewriting core logic.
- Supports advanced analytics and queries—once in the data, any aggregator or custom lambda can examine on-base percentages, fielding metrics, or predicted outcomes.

### Narrative
#### CMCC Baseball Extension
Baseball is a famously data-heavy sport, from the rules around balls and strikes to the infinite array of metrics (batting average, ERA, WAR, etc.). Historically, baseball logic has been scattered through textual rulebooks, custom-coded simulators, or ad hoc spreadsheets. Each approach repeats or re-implements the same concepts—teams, innings, outs, runs, at-bats—in its own way.
By contrast, the CMCC Baseball Model encodes all these domain concepts in a purely declarative fashion, capturing every rule from the simplest (3 strikes = 1 out) to the more subtle (infield fly, balk, defensive shifts, advanced sabermetrics). It becomes the single source of truth for all baseball logic—human-readable, machine-readable, and universally translatable. Whether you’re building a fantasy league platform, a simulation game, or advanced baseball analytics, the same structural definitions serve as the foundation, letting you query, transform, or expand the baseball domain without rewriting business logic in code.


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
  *Formula:* `SUM(teams.gamesPlayed) // or a more direct approach scanning a separate 'Game' entity`

### Lambdas
- **scheduleMatchups**
    
  *Formula:* `CreateScheduledGames(teams)`


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
  *Description:* Number of Games in which this team has participated. Implementation conceptual.  
  *Formula:* `COUNT( Game where (homeTeamId=this.id OR awayTeamId=this.id) )`
- **wins**  
  *Description:* Count of Games this team has won.  
  *Formula:* `COUNT( Game where (winnerId=this.id) )`
- **losses**  
  *Description:* Count of Games this team has lost.  
  *Formula:* `COUNT( Game where (loserId=this.id) )`
- **winPercentage**  
  *Description:* wins / (wins + losses), if any games played. Null otherwise.  
  *Formula:* `IF (gamesPlayed>0) THEN (wins / gamesPlayed) ELSE null`

### Lambdas
- **addPlayerToRoster**
  (Parameters: player_id)  
  *Formula:* `Set Player.team_id = this.id`
- **removePlayerFromRoster**
  (Parameters: player_id)  
  *Formula:* `Set Player.team_id = null`


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
  *Formula:* `AccumulateInningsFromOuts( (sum of outs recorded by pitcherId=this.id) )`

### Lambdas
- **adjustBattingHand**
  (Parameters: newHand)  
  *Formula:* `Set this.battingHand = newHand`


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
  *Description:* Total runs scored by the home team, summing the relevant half-innings if offense=homeTeamId.  
  *Formula:* `SUM( InningHalf.runsScored for all bottomHalves with offensiveTeamId=homeTeamId )`
- **runsAway**  
  *Description:* Total runs scored by the away team, summing the relevant half-innings if offense=awayTeamId.  
  *Formula:* `SUM( InningHalf.runsScored for all topHalves with offensiveTeamId=awayTeamId )`
- **winnerId**  
  *Description:* If status='FINAL', determine which team has more runs. Null if tie or incomplete.  
  *Formula:* `IF status='FINAL' THEN (IF runsHome>runsAway THEN homeTeamId ELSE IF runsAway>runsHome THEN awayTeamId ELSE null) ELSE null`
- **loserId**  
  *Description:* Symmetric aggregator to winnerId; identifies losing team if final and not tied.  
  *Formula:* `IF status='FINAL' AND runsHome!=runsAway THEN (IF winnerId=homeTeamId THEN awayTeamId ELSE homeTeamId) ELSE null`

### Lambdas
- **startGame**
    
  *Formula:* `this.status='IN_PROGRESS'; Create(Inning for inningNumber=1)`
- **endGame**
    
  *Formula:* `this.status='FINAL'`

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
  *Description:* True if top and bottom half are both complete, or if no bottom half needed (walk-off scenario).  
  *Formula:* `top.isComplete AND ( bottom == null OR bottom.isComplete )`



---

## Entity: InningHalf

**Description**: Represents either top or bottom portion of an inning, with outs, runs, at-bats, etc.

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

### Lambdas
- **recordOut**
    
  *Formula:* `outs = outs + 1; IF outs>=3 THEN isComplete=true;`
- **scoreRun**
  (Parameters: count)  
  *Formula:* `runsScored = runsScored + count;`

### Constraints
- **validOutCount**  
  *Formula:* `outs >= 0 AND outs <= 3`  
  *Error Message:* Outs must be between 0 and 3 inclusive.

---

## Entity: AtBat

**Description**: A single plate appearance, from the start of the batter's turn to its final result.

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

### Lambdas
- **addPitch**
  (Parameters: pitchData)  
  *Formula:* `INSERT Pitch { atBatId: this.id, ...pitchData }`
- **finalizeAtBat**
    
  *Formula:* `If (result in [GROUNDOUT,FLYOUT,STRIKEOUT]) => InningHalf.recordOut(); If (result in [SINGLE,DOUBLE,TRIPLE,HOMERUN, etc.]) => maybe InningHalf.scoreRun(x);`


---

## Entity: Pitch

**Description**: Represents a single pitch thrown in an at-bat. Tracks velocity, location, outcome, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **atBatId**  
  *Type:* lookup, *Datatype:*   
  
- **pitchResult**  
  *Type:* scalar, *Datatype:* string  
  
- **pitchVelocity**  
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
  





---