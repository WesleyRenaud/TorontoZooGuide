from enum import Enum


class ItinerarySaveIssueType( str, Enum ):
   WILD_ENCOUNTER_TIME_CONFLICT = 'wildEncounterTimeConflict'
   GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS = 'guardiansTalkWillUnscheduleItems'
