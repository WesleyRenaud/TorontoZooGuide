from enum import Enum


class ItinerarySaveIssueType( str, Enum ):
   # To-do: Revisit to potentially merge with ItineraryErrorType
   WILD_ENCOUNTER_TIME_CONFLICT = 'wildEncounterTimeConflict'
   GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS = 'guardiansTalkWillUnscheduleItems'
   WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS = 'wildEncounterWillUnscheduleItems'
   BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME = 'bulkScheduleAnimalsNotEnoughTime'
