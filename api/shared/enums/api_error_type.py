from enum import Enum


class ApiErrorType( str, Enum ):
   COULD_NOT_SET_CLOSED = 'couldNotSetClosed'
   COULD_NOT_SET_OPEN = 'couldNotSetOpen'
   COULD_NOT_CREATE_CLOSURE_OVERRIDE = 'couldNotCreateClosureOverride'
   COULD_NOT_SET_OPENING_SCHEDULE = 'couldNotSetOpeningSchedule'
   COULD_NOT_REPLACE_OPENING_SCHEDULE_OVERLAPS = (
      'couldNotReplaceOpeningScheduleOverlaps' )
   COULD_NOT_TRIM_OPENING_SCHEDULE_OVERLAPS = (
      'couldNotTrimOpeningScheduleOverlaps' )
   COULD_NOT_SET_ATTRACTION_HOURS = 'couldNotSetAttractionHours'
   COULD_NOT_REPLACE_ATTRACTION_HOURS_OVERLAPS = (
      'couldNotReplaceAttractionHoursOverlaps' )
   COULD_NOT_TRIM_ATTRACTION_HOURS_OVERLAPS = (
      'couldNotTrimAttractionHoursOverlaps' )
   COULD_NOT_SET_GUARDIANS_TALK_SCHEDULE = 'couldNotSetGuardiansTalkSchedule'
   COULD_NOT_END_GUARDIANS_TALK_SCHEDULE = 'couldNotEndGuardiansTalkSchedule'
   COULD_NOT_CANCEL_GUARDIANS_TALK_OCCURRENCE = (
      'couldNotCancelGuardiansTalkOccurrence' )
   COULD_NOT_SET_WILD_ENCOUNTER_SCHEDULE = 'couldNotSetWildEncounterSchedule'
   COULD_NOT_END_WILD_ENCOUNTER_SCHEDULE = 'couldNotEndWildEncounterSchedule'
   COULD_NOT_CANCEL_WILD_ENCOUNTER_OCCURRENCE = (
      'couldNotCancelWildEncounterOccurrence' )
   COULD_NOT_SET_RESTROOM_ALERT = 'couldNotSetRestroomAlert'
   COULD_NOT_REMOVE_RESTROOM_ALERT = 'couldNotRemoveRestroomAlert'
   COULD_NOT_SET_TRANSPORTATION_ROUTE = 'couldNotSetTransportationRoute'
   DRINKING_FOUNTAINS_COULD_NOT_SET_CLOSED = (
      'drinkingFountainsCouldNotSetClosed' )
   DRINKING_FOUNTAINS_COULD_NOT_SET_OPEN = 'drinkingFountainsCouldNotSetOpen'
   COULD_NOT_CREATE_UPDATE = 'couldNotCreateUpdate'
   COULD_NOT_END_UPDATE = 'couldNotEndUpdate'
   COULD_NOT_EDIT_UPDATE = 'couldNotEditUpdate'
   COULD_NOT_CREATE_EVENT = 'couldNotCreateEvent'
   NO_ANIMAL_FOUND_WITH_SPECIES = 'noAnimalFoundWithSpecies'
   NO_OFF_DISPLAY_ENTRY_FOUND = 'noOffDisplayEntryFound'
   COULD_NOT_SET_LIMITED_VIEWING_SCHEDULE = 'couldNotSetLimitedViewingSchedule'
   COULD_NOT_REMOVE_VISIBILITY_SCHEDULE = 'couldNotRemoveVisibilitySchedule'
   COULD_NOT_SET_VIEWING_ALERT = 'couldNotSetViewingAlert'
   COULD_NOT_REMOVE_VIEWING_ALERT = 'couldNotRemoveViewingAlert'
   COULD_NOT_CLEAR_ITINERARY = 'couldNotClearItinerary'
   COULD_NOT_ACCEPT_ITINERARY_CHANGES = 'couldNotAcceptItineraryChanges'
   INVALID_ATTRACTION_HOURS = 'invalidAttractionHours'
   GUARDIANS_TALK_OCCURRENCE_ALREADY_EXISTS = (
      'guardiansTalkOccurrenceAlreadyExists' )
   COULD_NOT_ADD_GUARDIANS_TALK_OCCURRENCE = (
      'couldNotAddGuardiansTalkOccurrence' )
   COULD_NOT_RESOLVE_ATTRACTION_HOURS_TIME_BOUNDS = (
      'couldNotResolveAttractionHoursTimeBounds' )
