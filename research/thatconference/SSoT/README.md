# Conference ToE Meta-Model (Extended)
## A 100% Declarative Framework for Multi-day Events

A unified meta-model capturing the domain of conferences—days, rooms, sessions, speakers, schedules, real-time event logic—now extended with 25 new inferences expressed as purely declarative fields, lookups, and aggregator definitions.

**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Conferencing

### Authors

### Abstract
This model extends the original conference schema to illustrate 25 new inferences, each implemented via aggregator fields, constraints, or new event entities. We adhere strictly to the CMCC principle of data-driven domain logic, adding features like day-level check-ins, sponsor policy checks, advanced concurrency detection, and more—still purely declarative.

![Conference ToE Meta-Model (Extended) Entity Diagram](conferencing.png)


### Key Points
- Maintains a purely declarative logic style for session concurrency, capacity, sponsor, and time-based calculations.
- Introduces new aggregator fields for real-time analysis (peak usage, average durations, overlapping speaker checks).
- Adds a new event entity (AttendeeDayCheckInEvent) for daily presence tracking.
- Demonstrates how to expand the domain model by simply defining new aggregator or constraint logic—no imperative code.

### Implications
- Enhances real-time data insights without rewriting any procedural code.
- Shows the ease of domain model growth: new rules, new event types, new aggregator fields, all purely data-based.

### Narrative
#### Extended Declarative Features
This extended version of the Conference ToE Meta Model introduces a wide variety of aggregator fields—some measure daily usage (peak capacity, most-attended session), some track advanced speaker or attendee behaviors (overlapping sessions, day-level check-ins). The entire domain remains purely declarative: everything from forced early session endings to sponsor policies is expressed as constraints, aggregator formulas, or event records.


---

# Schema Overview

## Entity: Conference

**Description**: Represents a multi-day event. Tracks overall name, location, included days, sponsor assignments, and aggregator fields (e.g., total sessions).

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **conferenceName**  
  *Type:* scalar, *Datatype:* string  
  
- **location**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **days**  
  *Target Entity:* ConferenceDay, *Type:* one_to_many  
    
  (Join condition: **ConferenceDay.conferenceId = this.id**)  
  *Description:* All days that belong to this conference.
- **sponsors**  
  *Target Entity:* Sponsor, *Type:* one_to_many  
    
  (Join condition: **Sponsor.conferenceId = this.id**)  
  *Description:* All sponsors officially participating in this conference.
- **speakers**  
  *Target Entity:* Speaker, *Type:* one_to_many  
    
  (Join condition: **Speaker.conferenceId = this.id**)  
  *Description:* All speakers registered for this conference.
- **rooms**  
  *Target Entity:* Room, *Type:* one_to_many  
    
  (Join condition: **Room.conferenceId = this.id**)  
  *Description:* All rooms used by this conference.

### Aggregations
- **totalSessions**  
  *Description:* Counts the total number of scheduled sessions across all days in the conference.  
  *Formula:* `SUM(days.sessionCount)`
- **totalAttendeeCapacity**  
  *Description:* Sum of all room capacities, an approximate upper bound if every room was used at once.  
  *Formula:* `SUM(rooms.capacity)`
- **runningNowSessions**  
  *Description:* How many sessions are currently in progress across the entire conference.  
  *Formula:* `COUNT(Session WHERE isInProgress=true AND dayId in days)`
- **maxConcurrentSessions**  
  *Description:* The maximum number of sessions that are simultaneously running at any point in time. Implementation conceptual.  
  *Formula:* `CALCULATE_MAX_OVERLAPPING_SESSIONS(all sessions in this conference)`
- **activeDayCount**  
  *Description:* Number of days that are still active or upcoming (based on the schedule).  
  *Formula:* `COUNT(days WHERE dayIsComplete=false)`
- **isConferenceComplete**  
  *Description:* True if all days in the conference are complete.  
  *Formula:* `NOT EXISTS(ConferenceDay WHERE conferenceId=this.id AND isDayComplete=false)`
- **peakDailyCapacityUsed**  
  *Description:* // NEW INFERENCE: The maximum of capacityUsed among all days in this conference.  
  *Formula:* `MAX(days.capacityUsed)`
- **averageSessionDurationMinutes**  
  *Description:* // NEW INFERENCE: The average scheduled duration (in minutes) of all sessions in this conference.  
  *Formula:* `AVERAGE(Session.sessionDurationMinutes WHERE dayId in days)`
- **conferenceHasKeynotes**  
  *Description:* // NEW INFERENCE: True if at least one session is a KEYNOTE.  
  *Formula:* `EXISTS(Session WHERE sessionType='KEYNOTE' AND dayId in days)`
- **totalUniqueAttendees**  
  *Description:* // NEW INFERENCE: Distinct count of attendee IDs across all SessionAttendanceEvents within this conference.  
  *Formula:* `COUNT(DISTINCT(SessionAttendanceEvent.attendeeId) WHERE sessionId.dayId.conferenceId = this.id)`
- **isConferenceActiveNow**  
  *Description:* // NEW INFERENCE: True if any session isInProgress=true or any day isDayActive=true for this conference.  
  *Formula:* `EXISTS(ConferenceDay WHERE conferenceId=this.id AND isDayActive=true)`

### Lambdas
- **closeConference**
    
  *Formula:* `IF (isConferenceComplete=true) THEN (Conference.status='CLOSED')`


---

## Entity: ConferenceDay

**Description**: Represents a single day in the conference schedule. Tied to date(s), references sessions, breaks, or special events.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **conferenceId**  
  *Type:* lookup, *Datatype:*   
  
- **dayDate**  
  *Type:* scalar, *Datatype:* date  
  
- **startTime**  
  *Type:* scalar, *Datatype:* datetime  
  
- **endTime**  
  *Type:* scalar, *Datatype:* datetime  
  

### Lookups
- **sessions**  
  *Target Entity:* Session, *Type:* one_to_many  
    
  (Join condition: **Session.dayId = this.id**)  
  *Description:* All sessions taking place on this day.

### Aggregations
- **sessionCount**  
  *Description:* Number of sessions scheduled for this day.  
  *Formula:* `COUNT(sessions)`
- **runningSessionsNow**  
  *Description:* How many sessions are currently in progress on this day.  
  *Formula:* `COUNT(sessions WHERE isInProgress=true)`
- **isDayActive**  
  *Description:* True if current time is between day start/end or if any session is still running.  
  *Formula:* `(CURRENT_TIME >= startTime AND CURRENT_TIME <= endTime) OR runningSessionsNow>0`
- **isDayComplete**  
  *Description:* True if all sessions are finished and the endTime has passed.  
  *Formula:* `(NOT EXISTS(sessions WHERE isCompleted=false)) AND (CURRENT_TIME > endTime)`
- **capacityUsed**  
  *Description:* Approx. aggregator for how many total seats are in use across currently running sessions.  
  *Formula:* `SUM(sessions.sessionAttendeeCount WHERE isInProgress=true)`
- **hasScheduledBreaks**  
  *Description:* Indicates if any session is flagged as a break/meal on this day.  
  *Formula:* `EXISTS(sessions WHERE sessionType='BREAK' OR sessionType='MEAL')`
- **occupiedRoomCount**  
  *Description:* // NEW INFERENCE: How many rooms are currently occupied (i.e., have an in-progress session) on this day.  
  *Formula:* `COUNT(DISTINCT sessions.roomId WHERE sessions.isInProgress=true)`
- **mostAttendedSession**  
  *Description:* // NEW INFERENCE: The ID of the session with the highest sessionAttendeeCount on this day. Implementation conceptual if ties exist.  
  *Formula:* `FIND_MAX(sessions, sessionAttendeeCount)`
- **dayLongestSession**  
  *Description:* // NEW INFERENCE: The session with the largest scheduled duration on this day.  
  *Formula:* `FIND_MAX(sessions, sessionDurationMinutes)`
- **dayHasSponsorSessions**  
  *Description:* // NEW INFERENCE: True if any session on this day has hasSponsorHighlight=true.  
  *Formula:* `EXISTS(sessions WHERE hasSponsorHighlight=true)`

### Lambdas
- **startDay**
    
  *Formula:* `IF (CURRENT_TIME >= this.startTime) THEN (this.isDayActive=true)`
- **endDay**
    
  *Formula:* `IF (this.isDayComplete=true) THEN (DayStatus='ENDED')`


---

## Entity: Room

**Description**: A physical location or room for sessions. Tracks capacity, A/V, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **conferenceId**  
  *Type:* lookup, *Datatype:*   
  
- **roomName**  
  *Type:* scalar, *Datatype:* string  
  
- **capacity**  
  *Type:* scalar, *Datatype:* integer  
  

### Lookups
- **sessions**  
  *Target Entity:* Session, *Type:* one_to_many  
    
  (Join condition: **Session.roomId = this.id**)  
  *Description:* All sessions scheduled in this room.

### Aggregations
- **currentSession**  
  *Description:* Which session is in progress right now in this room, if any.  
  *Formula:* `FIND(Session WHERE roomId=this.id AND isInProgress=true)`
- **totalSessionsInRoom**  
  *Description:* Number of sessions scheduled in this room across all days.  
  *Formula:* `COUNT(sessions)`
- **roomUtilizationRate**  
  *Description:* Calculated ratio of how many hours this room is in use vs. total conference hours. Conceptual.  
  *Formula:* `CALCULATE_ROOM_UTILIZATION(this.id)`
- **roomIsCurrentlyOccupied**  
  *Description:* // NEW INFERENCE: True if currentSession is in progress (i.e. isInProgress=true).  
  *Formula:* `EXISTS(currentSession WHERE isInProgress=true)`

### Lambdas
- **assignSession**
  (Parameters: sessionId)  
  *Formula:* `Session(sessionId).roomId = this.id`

### Constraints
- **roomCapacityNonNegative**  
  *Formula:* `capacity >= 0`  
  *Error Message:* Room capacity cannot be negative.

---

## Entity: Session

**Description**: A single talk, workshop, panel, or break event within the conference day/room assignment.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **dayId**  
  *Type:* lookup, *Datatype:*   
  
- **roomId**  
  *Type:* lookup, *Datatype:*   
  
- **sessionTitle**  
  *Type:* scalar, *Datatype:* string  
  
- **startTime**  
  *Type:* scalar, *Datatype:* datetime  
  
- **endTime**  
  *Type:* scalar, *Datatype:* datetime  
  
- **sessionType**  
  *Type:* scalar, *Datatype:* string  
  
- **isCanceled**  
  *Type:* scalar, *Datatype:* boolean  
  

### Lookups
- **speakers**  
  *Target Entity:* Speaker, *Type:* many_to_many  
    
    
  *Description:* Which speaker(s) are leading this session.
- **attendeeEvents**  
  *Target Entity:* SessionAttendanceEvent, *Type:* one_to_many  
    
  (Join condition: **SessionAttendanceEvent.sessionId = this.id**)  
  *Description:* All check-in or check-out events referencing this session.

### Aggregations
- **isInProgress**  
  *Description:* Session is in progress if current time is between start/end and not canceled.  
  *Formula:* `(CURRENT_TIME >= startTime AND CURRENT_TIME < endTime) AND (isCanceled=false)`
- **isCompleted**  
  *Description:* True if current time >= endTime or a SessionEndEvent ended it, and not canceled.  
  *Formula:* `((CURRENT_TIME >= endTime) OR (EXISTS(SessionEndEvent WHERE sessionId=this.id))) AND (isCanceled=false)`
- **sessionDurationMinutes**  
  *Description:* Number of minutes from scheduled start to scheduled end.  
  *Formula:* `TIMEDIFF(endTime, startTime)`
- **sessionAttendeeCount**  
  *Description:* Number of unique attendees currently checked in (arrived but not departed).  
  *Formula:* `COUNT(DISTINCT attendeeEvents.attendeeId WHERE checkInTime != null AND checkOutTime=null)`
- **speakersCount**  
  *Description:* Number of assigned speakers for this session.  
  *Formula:* `COUNT(speakers)`
- **hasSponsorHighlight**  
  *Description:* If a sponsor is officially associated with the session. Implementation conceptual.  
  *Formula:* `EXISTS(SponsorSessionAssignment WHERE sessionId=this.id)`
- **minutesOverrun**  
  *Description:* How many minutes the session has run past its scheduled endTime, if still in progress.  
  *Formula:* `IF (CURRENT_TIME > endTime AND isInProgress=true) THEN (TIMEDIFF(CURRENT_TIME, endTime)) ELSE 0`
- **isFull**  
  *Description:* True if sessionAttendeeCount >= assigned Room.capacity.  
  *Formula:* `sessionAttendeeCount >= (SELECT capacity FROM Room WHERE id=roomId)`
- **sessionHasEndedEarly**  
  *Description:* // NEW INFERENCE: True if a SessionEndEvent with forcedEndTime < scheduled endTime exists.  
  *Formula:* `EXISTS(SessionEndEvent WHERE sessionId=this.id AND forcedEndTime < endTime)`
- **actualEndTime**  
  *Description:* // NEW INFERENCE: The earliest of endTime or forcedEndTime from SessionEndEvent (if any). Implementation conceptual.  
  *Formula:* `IF (EXISTS(SessionEndEvent WHERE sessionId=this.id)) THEN MIN(endTime, SessionEndEvent.forcedEndTime) ELSE endTime`
- **speakersPresentNow**  
  *Description:* // NEW INFERENCE: Lists speakers if session isInProgress=true. Implementation conceptual.  
  *Formula:* `IF (isInProgress=true) THEN (speakers) ELSE []`

### Lambdas
- **cancelSession**
    
  *Formula:* `this.isCanceled = true`
- **extendSession**
  (Parameters: newEndTime)  
  *Formula:* `this.endTime = newEndTime`

### Constraints
- **endAfterStart**  
  *Formula:* `endTime > startTime`  
  *Error Message:* Session endTime must be later than startTime.
- **roomCapacityNotExceeded**  
  *Formula:* `sessionAttendeeCount <= (SELECT capacity FROM Room WHERE id=roomId)`  
  *Error Message:* Cannot exceed room capacity for this session.
- **noSpeakerDoubleBooking**  
  *Formula:* `NOT EXISTS( (Session s2 JOIN Speaker sp2) WHERE s2.id != this.id AND sp2 IN this.speakers AND sp2 IN s2.speakers AND s2.isInProgress=true AND this.isInProgress=true )`  
  *Error Message:* Speaker cannot be in two sessions at once.

---

## Entity: Speaker

**Description**: An individual presenting at one or more sessions in the conference.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **conferenceId**  
  *Type:* lookup, *Datatype:*   
  
- **fullName**  
  *Type:* scalar, *Datatype:* string  
  
- **bio**  
  *Type:* scalar, *Datatype:* text  
  

### Lookups
- **sessions**  
  *Target Entity:* Session, *Type:* many_to_many  
    
    
  *Description:* All sessions that this speaker is assigned to.

### Aggregations
- **sessionCount**  
  *Description:* Number of sessions in which this speaker is scheduled.  
  *Formula:* `COUNT(sessions)`
- **sessionsToday**  
  *Description:* Number of sessions the speaker has on the current calendar day.  
  *Formula:* `COUNT(sessions WHERE dayId.dayDate = CURRENT_DATE)`
- **isSpeakingNow**  
  *Description:* True if the speaker has at least one session currently in progress.  
  *Formula:* `EXISTS(sessions WHERE isInProgress=true)`
- **speakerHasOverlappingSessions**  
  *Description:* // NEW INFERENCE: True if speaker has any pair of sessions that overlap.  
  *Formula:* `CHECK_IF_SPEAKER_HAS_OVERLAPS(this.id)`
- **speakerHasConsecutiveSessions**  
  *Description:* // NEW INFERENCE: True if the speaker has sessions back-to-back with insufficient buffer time.  
  *Formula:* `CHECK_CONSECUTIVE_SESSIONS_WITH_BUFFER(this.id)`
- **totalSpeakingMinutes**  
  *Description:* // NEW INFERENCE: Sum of sessionDurationMinutes for all sessions assigned to this speaker.  
  *Formula:* `SUM(sessions.sessionDurationMinutes)`

### Lambdas
- **assignToSession**
  (Parameters: sessionId)  
  *Formula:* `this.sessions += sessionId`


---

## Entity: Attendee

**Description**: Individual attending the conference. Minimal registration details, focusing on presence at sessions and days.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **fullName**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **attendeeDayCheckInRecords**  
  *Target Entity:* AttendeeDayCheckInEvent, *Type:* one_to_many  
    
  (Join condition: **AttendeeDayCheckInEvent.attendeeId = this.id**)  
  *Description:* // NEW INFERENCE: All day-level check-ins the attendee has performed.

### Aggregations
- **currentSessionsJoined**  
  *Description:* All sessions the attendee is currently checked into (not checked out). Implementation conceptual.  
  *Formula:* `SessionAttendanceEvent WHERE attendeeId=this.id AND checkOutTime=null => sessionId`
- **isInsideConference**  
  *Description:* Indicates if the attendee is physically on-site (per day-level or session-level check-in). Implementation depends on presence of check-in events.  
  *Formula:* `EXISTS(AttendeeCheckInEvent WHERE attendeeId=this.id AND checkOutTime=null)`
- **attendeeHasFutureSessions**  
  *Description:* // NEW INFERENCE: True if attendee has at least one session with startTime > CURRENT_TIME. Implementation conceptual.  
  *Formula:* `EXISTS(SessionAttendanceEvent WHERE attendeeId=this.id AND Session.startTime > CURRENT_TIME)`
- **attendeeTotalAttendanceTime**  
  *Description:* // NEW INFERENCE: Sum of all attendanceDurationMinutes across this attendee’s SessionAttendanceEvents.  
  *Formula:* `SUM(SessionAttendanceEvent.attendanceDurationMinutes WHERE attendeeId=this.id)`
- **attendeeLastSessionAttended**  
  *Description:* // NEW INFERENCE: The most recent session (by checkIn or checkOut) the attendee has attended.  
  *Formula:* `FIND_MOST_RECENT(SessionAttendanceEvent WHERE attendeeId=this.id => sessionId)`

### Lambdas
- **checkIntoSession**
  (Parameters: sessionId)  
  *Formula:* `SessionAttendanceEvent(attendeeId=this.id, sessionId=sessionId, checkInTime=NOW, checkOutTime=null)`


---

## Entity: SessionAttendanceEvent

**Description**: Fact-based record that a specific attendee joined or left a given session.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **sessionId**  
  *Type:* lookup, *Datatype:*   
  
- **attendeeId**  
  *Type:* lookup, *Datatype:*   
  
- **checkInTime**  
  *Type:* scalar, *Datatype:* datetime  
  
- **checkOutTime**  
  *Type:* scalar, *Datatype:* datetime  
  


### Aggregations
- **attendanceDurationMinutes**  
  *Description:* How long the attendee was (or has been) in the session. If checkOutTime is null, partial duration up to now.  
  *Formula:* `IF (checkOutTime!=null) THEN TIMEDIFF(checkOutTime, checkInTime) ELSE TIMEDIFF(CURRENT_TIME, checkInTime)`
- **isCurrentlyCheckedIn**  
  *Description:* // NEW INFERENCE: True if checkOutTime is null and checkInTime != null.  
  *Formula:* `(checkInTime != null) AND (checkOutTime = null)`

### Lambdas
- **checkOut**
    
  *Formula:* `this.checkOutTime = NOW`

### Constraints
- **mustHaveCheckInBeforeCheckOut**  
  *Formula:* `(checkOutTime IS NULL) OR (checkOutTime >= checkInTime)`  
  *Error Message:* Cannot check out before you have checked in.

---

## Entity: Sponsor

**Description**: Represents a sponsor for the conference (e.g., a company or organization).

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **conferenceId**  
  *Type:* lookup, *Datatype:*   
  
- **sponsorName**  
  *Type:* scalar, *Datatype:* string  
  
- **sponsorTier**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **hasSponsoredSession**  
  *Description:* Indicates if the sponsor is attached to any sessions.  
  *Formula:* `EXISTS(SponsorSessionAssignment WHERE sponsorId=this.id)`
- **assignedBooth**  
  *Description:* If the sponsor has an allocated booth space. Implementation conceptual.  
  *Formula:* `LOOKUP(BoothAssignment WHERE sponsorId=this.id => boothName)`
- **sponsorHasBoothAssignment**  
  *Description:* // NEW INFERENCE: True if there's a BoothAssignment record for this sponsor.  
  *Formula:* `EXISTS(BoothAssignment WHERE sponsorId=this.id)`



---

## Entity: SessionEndEvent

**Description**: Event-based record that forcibly ends a session early (or triggers session completion).

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **sessionId**  
  *Type:* lookup, *Datatype:*   
  
- **endReason**  
  *Type:* scalar, *Datatype:* string  
  
- **forcedEndTime**  
  *Type:* scalar, *Datatype:* datetime  
  





---

## Entity: ConferencePolicy

**Description**: Represents adjustable rules or global constraints for a conference.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **conferenceId**  
  *Type:* lookup, *Datatype:*   
  
- **maxSessionLengthMinutes**  
  *Type:* scalar, *Datatype:* integer  
  
- **minBreakBetweenSessionsMinutes**  
  *Type:* scalar, *Datatype:* integer  
  
- **roomChangeBufferMinutes**  
  *Type:* scalar, *Datatype:* integer  
  


### Aggregations
- **requiresSponsorApprovalForKeynotes**  
  *Description:* // NEW INFERENCE: If true, any KEYNOTE session must have sponsor sign-off. Implementation conceptual.  
  *Formula:* `GET_POLICY_VALUE('requiresSponsorApprovalForKeynotes')`


### Constraints
- **enforceSessionLength**  
  *Formula:* `NOT EXISTS(Session WHERE TIMEDIFF(endTime, startTime) > maxSessionLengthMinutes)`  
  *Error Message:* No session can exceed the max allowed session length.
- **enforceRoomTurnover**  
  *Formula:* `CHECK_NO_OVERLAP_IN_ROOM_WITHOUT_BUFFER(roomChangeBufferMinutes, minBreakBetweenSessionsMinutes)`  
  *Error Message:* Sessions in the same room must have at least minBreakBetweenSessionsMinutes gap.

---

## Entity: AttendeeDayCheckInEvent

**Description**: // NEW ENTITY: Tracks an attendee’s day-level presence. Separate from session-level attendance.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **attendeeId**  
  *Type:* lookup, *Datatype:*   
  
- **dayId**  
  *Type:* lookup, *Datatype:*   
  
- **checkInTime**  
  *Type:* scalar, *Datatype:* datetime  
  
- **checkOutTime**  
  *Type:* scalar, *Datatype:* datetime  
  


### Aggregations
- **dayCheckInDurationMinutes**  
  *Description:* // NEW INFERENCE: How long the attendee stayed for that day. Implementation conceptual.  
  *Formula:* `IF (checkOutTime!=null) THEN TIMEDIFF(checkOutTime, checkInTime) ELSE TIMEDIFF(CURRENT_TIME, checkInTime)`


### Constraints
- **mustCheckInBeforeCheckOut**  
  *Formula:* `(checkOutTime IS NULL) OR (checkOutTime >= checkInTime)`  
  *Error Message:* Day checkOutTime cannot precede checkInTime.

---