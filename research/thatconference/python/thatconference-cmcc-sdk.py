"""
Auto-generated Python code from your quantum-walk rulebook.
References SHIFT, APPLY_BARRIER, EVOLVE, etc. from an external python file.
"""
import math
import numpy as np

# ----- Generated classes below -----

class Conference:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.conferenceName = kwargs.get('conferenceName')
        self.location = kwargs.get('location')

class ConferenceDay:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.conferenceId = kwargs.get('conferenceId')
        self.dayDate = kwargs.get('dayDate')
        self.startTime = kwargs.get('startTime')
        self.endTime = kwargs.get('endTime')

class Room:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.conferenceId = kwargs.get('conferenceId')
        self.roomName = kwargs.get('roomName')
        self.capacity = kwargs.get('capacity')

class Session:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.dayId = kwargs.get('dayId')
        self.roomId = kwargs.get('roomId')
        self.sessionTitle = kwargs.get('sessionTitle')
        self.startTime = kwargs.get('startTime')
        self.endTime = kwargs.get('endTime')
        self.sessionType = kwargs.get('sessionType')
        self.isCanceled = kwargs.get('isCanceled')

class Speaker:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.conferenceId = kwargs.get('conferenceId')
        self.fullName = kwargs.get('fullName')
        self.bio = kwargs.get('bio')

class Attendee:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.fullName = kwargs.get('fullName')

class SessionAttendanceEvent:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.sessionId = kwargs.get('sessionId')
        self.attendeeId = kwargs.get('attendeeId')
        self.checkInTime = kwargs.get('checkInTime')
        self.checkOutTime = kwargs.get('checkOutTime')

class Sponsor:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.conferenceId = kwargs.get('conferenceId')
        self.sponsorName = kwargs.get('sponsorName')
        self.sponsorTier = kwargs.get('sponsorTier')

class SessionEndEvent:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.sessionId = kwargs.get('sessionId')
        self.endReason = kwargs.get('endReason')
        self.forcedEndTime = kwargs.get('forcedEndTime')

class ConferencePolicy:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.conferenceId = kwargs.get('conferenceId')
        self.maxSessionLengthMinutes = kwargs.get('maxSessionLengthMinutes')
        self.minBreakBetweenSessionsMinutes = kwargs.get('minBreakBetweenSessionsMinutes')
        self.roomChangeBufferMinutes = kwargs.get('roomChangeBufferMinutes')

class AttendeeDayCheckInEvent:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.attendeeId = kwargs.get('attendeeId')
        self.dayId = kwargs.get('dayId')
        self.checkInTime = kwargs.get('checkInTime')
        self.checkOutTime = kwargs.get('checkOutTime')
