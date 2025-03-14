# Conference ToE Meta-Model
## A 100% Declarative Framework for Multi-day Events

A unified meta-model capturing the domain of conferences—days, rooms, sessions, speakers, schedules, and real-time event logic—within a purely declarative structure. All domain rules (like session overlap, room capacity, speaker scheduling, or day closures) are expressed using lookups, aggregations, constraints, and event-based facts—no imperative instructions.

**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Conferencing

### Authors

### Abstract
This model demonstrates how to manage real-world conferences—sessions, speakers, rooms, sponsors, daily schedules—strictly through declarative definitions. Instead of imperative ‘start session now’ or ‘end session now’ code, we rely on aggregator fields and event records (e.g., SessionStartEvent) that reflect real-time facts about what is happening. Conflicts, availability, capacity, and daily or session-level transitions are derived from data-based constraints and aggregator formulas.

![Conference ToE Meta-Model Entity Diagram](conferencing.png)


### Key Points
- Models a conference’s day-to-day operations (room usage, session scheduling, speaker concurrency) as pure aggregator or lookup-based logic.
- Eliminates stepwise imperative procedures (e.g., ‘increment time’ or ‘mark session ended’). All logic is triggered by the presence/absence of event records or derived constraints.
- Supports arbitrary complexity: multi-track agendas, sponsor-driven sessions, daily wrap-ups, or even real-time session expansions can be captured by additional aggregator fields and events.
- Makes it easy to identify conflicts (double-booked rooms, overlapping speaker schedules) simply by referencing the aggregator or constraint outputs.

### Implications
- Simplifies the code needed to orchestrate an event. The data itself drives all ‘what is happening now’ logic.
- Enables advanced analytics in real-time—when your aggregator fields detect a capacity breach, or a session is auto-flagged as ‘running long,’ no custom code is required.
- Permits high-level additions (keynotes, sponsor sessions, brand new tracks) by simply adding more entities and aggregator fields referencing the same underlying structure.

### Narrative
#### Purely Declarative Day-to-Day Conference Operations
In this version, we avoid any imperative instructions like ‘if session is finished, set session.status=ENDED.’ Instead, a session’s status is derived from the time window, actual recorded events, or constraints. If the current time is beyond the scheduled end time and no SessionExtensionEvent is present, the aggregator logic sees that the session must be over. That same aggregator logic might also note if a sponsor event forced an extended Q&A, and we can reflect that purely by the presence of a SessionExtendedEvent record.
All day-to-day tasks—closing out a room at the end of the day, switching from one session to the next, or verifying that a speaker is not double-booked—are performed by constraints, lookups, or aggregator fields referencing the same data. This matches exactly how CMCC prescribes purely declarative domain logic: no step-by-step commands, just ‘statements of truth’ about room capacity, time slots, concurrency, and more.


---

# Schema Overview

## Entity: Conference

**Description**: Represents a multi-day event. Tracks overall name, location, included days, sponsor assignments, and high-level aggregator fields (e.g., total sessions).

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
  *Description:* The maximum number of sessions that are simultaneously running at any point in time. Implementation conceptual (requires scanning session overlaps).  
  *Formula:* `CALCULATE_MAX_OVERLAPPING_SESSIONS(all sessions in this conference)`
- **activeDayCount**  
  *Description:* Number of days that are still active or upcoming (based on the schedule).  
  *Formula:* `COUNT(days WHERE dayIsComplete=false)`
- **isConferenceComplete**  
  *Description:* True if all days in the conference are complete.  
  *Formula:* `NOT EXISTS(ConferenceDay WHERE conferenceId=this.id AND isDayComplete=false)`

### Lambdas
- **closeConference**
    
  *Formula:* `IF (isConferenceComplete=true) THEN (Conference.status='CLOSED')`


---

## Entity: ConferenceDay

**Description**: Represents a single day in the conference schedule. Tied to date(s), and contains references to sessions, breaks, or special events.

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
  *Description:* True if current time is between day start and end, or if any session is still running. Implementation conceptual.  
  *Formula:* `(CURRENT_TIME >= startTime AND CURRENT_TIME <= endTime) OR runningSessionsNow>0`
- **isDayComplete**  
  *Description:* True if all sessions are finished and the endTime has passed.  
  *Formula:* `(NOT EXISTS(sessions WHERE isCompleted=false)) AND (CURRENT_TIME > endTime)`
- **capacityUsed**  
  *Description:* An approximate aggregator for how many total seats are in use across all simultaneously running sessions. Implementation conceptual (requires sum of sessionAttendeeCount).  
  *Formula:* `SUM(sessions.sessionAttendeeCount WHERE isInProgress=true)`
- **hasScheduledBreaks**  
  *Description:* Indicates if any session is flagged as a break or meal. Implementation conceptual if sessions have a 'sessionType'.  
  *Formula:* `EXISTS(sessions WHERE sessionType='BREAK' OR sessionType='MEAL')`

### Lambdas
- **startDay**
    
  *Formula:* `IF (CURRENT_TIME >= this.startTime) THEN (this.isDayActive=true)`
- **endDay**
    
  *Formula:* `IF (this.isDayComplete=true) THEN (DayStatus='ENDED')`


---

## Entity: Room

**Description**: A physical location or room in which sessions can be held. Tracks capacity, A/V requirements, location details, etc.

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
  *Description:* Number of sessions scheduled in this room across all days of the conference.  
  *Formula:* `COUNT(sessions)`
- **roomUtilizationRate**  
  *Description:* Calculated ratio of how many hours this room is in use vs. total conference hours. Implementation conceptual.  
  *Formula:* `CALCULATE_ROOM_UTILIZATION(this.id)`

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

**Description**: A single talk, workshop, panel, or break event within the conference, assigned to a day and a room, with start/end times and a set of speakers.

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
    
    
  *Description:* Which speaker(s) are leading this session. Usually one or more, depending on type.
- **attendeeEvents**  
  *Target Entity:* SessionAttendanceEvent, *Type:* one_to_many  
    
  (Join condition: **SessionAttendanceEvent.sessionId = this.id**)  
  *Description:* All check-in or check-out events referencing this session.

### Aggregations
- **isInProgress**  
  *Description:* Session is in progress if current time is between start/end and not canceled or forcibly ended.  
  *Formula:* `(CURRENT_TIME >= startTime AND CURRENT_TIME < endTime) AND (isCanceled=false)`
- **isCompleted**  
  *Description:* True if current time >= endTime or session was forcibly ended, and not canceled.  
  *Formula:* `((CURRENT_TIME >= endTime) OR (EXISTS(SessionEndEvent WHERE sessionId=this.id))) AND (isCanceled=false)`
- **sessionDurationMinutes**  
  *Description:* Number of minutes from scheduled start to scheduled end.  
  *Formula:* `TIMEDIFF(endTime, startTime) // in minutes`
- **sessionAttendeeCount**  
  *Description:* Number of unique attendees currently checked in (arrived but not departed).  
  *Formula:* `COUNT(DISTINCT attendeeEvents.attendeeId WHERE checkInTime != null AND checkOutTime=null)`
- **speakersCount**  
  *Description:* Number of assigned speakers for this session.  
  *Formula:* `COUNT(speakers)`
- **hasSponsorHighlight**  
  *Description:* If a sponsor is officially associated with the session. Implementation conceptual—maybe a join table or a sessionType indicating sponsorship.  
  *Formula:* `EXISTS(SponsorSessionAssignment WHERE sessionId=this.id)`
- **minutesOverrun**  
  *Description:* How many minutes the session has run past its scheduled endTime, if still in progress. 0 if not overrunning.  
  *Formula:* `IF (CURRENT_TIME > endTime AND isInProgress=true) THEN (TIMEDIFF(CURRENT_TIME, endTime)) ELSE 0`
- **isFull**  
  *Description:* True if sessionAttendeeCount >= assigned Room.capacity (i.e., room limit reached).  
  *Formula:* `sessionAttendeeCount >= (SELECT capacity FROM Room WHERE id=roomId)`

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

**Description**: An individual presenting at one or more sessions in the conference. Tied to a single conference but can appear in multiple sessions.

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
  *Description:* Number of sessions the speaker has on the current calendar day, if any. Implementation conceptual (filter by day == today).  
  *Formula:* `COUNT(sessions WHERE dayId.dayDate = CURRENT_DATE)`
- **isSpeakingNow**  
  *Description:* True if the speaker has at least one session currently in progress.  
  *Formula:* `EXISTS(sessions WHERE isInProgress=true)`

### Lambdas
- **assignToSession**
  (Parameters: sessionId)  
  *Formula:* `this.sessions += sessionId`


---

## Entity: Attendee

**Description**: Individual attending the conference. (Note: We minimize registration details here—focus is on daily, in-session presence.)

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **fullName**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **currentSessionsJoined**  
  *Description:* All sessions the attendee is currently checked into (and not checked out). Implementation conceptual referencing SessionAttendanceEvent.  
  *Formula:* `SessionAttendanceEvent WHERE attendeeId=this.id AND checkOutTime=null => sessionId`
- **isInsideConference**  
  *Description:* Indicates if the attendee is physically on-site (has checked in for the day, for example). Implementation depends on day-level or session-level check-in events.  
  *Formula:* `EXISTS(AttendeeCheckInEvent WHERE attendeeId=this.id AND checkOutTime=null)`

### Lambdas
- **checkIntoSession**
  (Parameters: sessionId)  
  *Formula:* `SessionAttendanceEvent(attendeeId=this.id, sessionId=sessionId, checkInTime=NOW, checkOutTime=null)`


---

## Entity: SessionAttendanceEvent

**Description**: Fact-based record indicating that a specific attendee joined (checkIn) or left (checkOut) a given session.

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

### Lambdas
- **checkOut**
    
  *Formula:* `this.checkOutTime = NOW`

### Constraints
- **mustHaveCheckInBeforeCheckOut**  
  *Formula:* `(checkOutTime IS NULL) OR (checkOutTime >= checkInTime)`  
  *Error Message:* Cannot check out before you have checked in.

---

## Entity: Sponsor

**Description**: Represents a sponsor (company or organization) for the conference. Minimal day-to-day logic, but relevant for sponsor sessions or booths.

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
  *Description:* Indicates if the sponsor is attached to any sessions. Implementation conceptual—would reference a SponsorSessionAssignment entity or similar.  
  *Formula:* `EXISTS(SponsorSessionAssignment WHERE sponsorId=this.id)`
- **assignedBooth**  
  *Description:* If the sponsor has an allocated booth space. Implementation conceptual—another link entity or data field might define booth assignment.  
  *Formula:* `LOOKUP(BoothAssignment WHERE sponsorId=this.id => boothName)`



---

## Entity: SessionEndEvent

**Description**: Event-based record that forcibly ends a session early (or triggers the session’s completion aggregator) for any reason. Purely optional usage.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **sessionId**  
  *Type:* lookup, *Datatype:*   
  
- **endReason**  
  *Type:* scalar, *Datatype:* string  
  





---

## Entity: ConferencePolicy

**Description**: Represents adjustable rules or global constraints for a conference: e.g., max session length, break intervals, or quiet hours. Used in aggregator constraints.

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
  




### Constraints
- **enforceSessionLength**  
  *Formula:* `NOT EXISTS(Session WHERE TIMEDIFF(endTime, startTime) > maxSessionLengthMinutes)`  
  *Error Message:* No session can exceed the max allowed session length.
- **enforceRoomTurnover**  
  *Formula:* `CHECK_NO_OVERLAP_IN_ROOM_WITHOUT_BUFFER(roomChangeBufferMinutes, minBreakBetweenSessionsMinutes)`  
  *Error Message:* Sessions in the same room must have at least minBreakBetweenSessionsMinutes gap.

---