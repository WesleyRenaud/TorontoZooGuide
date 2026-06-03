from enum import Enum


class ItineraryErrorType( str, Enum ):
   SUCCESS = 'success'
   ITINERARY_DATE_NOT_SET = 'itineraryDateNotSet'
   TIME_OUT_OF_BOUNDS = 'timeOutOfBounds'
   TIME_ORDER_INVALID = 'timeOrderInvalid'
   SAVE_FAILED = 'saveFailed'
   ARRIVAL_DEPARTURE_TOO_CLOSE = 'arrivalDepartureTooClose'
   NO_AVAILABLE_SLOT = 'noAvailableSlot'
   REQUESTED_TIME_NOT_AVAILABLE = 'requestedTimeNotAvailable'
   ITEM_NOT_ON_ITINERARY = 'itemNotOnItinerary'
   GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS = 'guardiansTalkWillUnscheduleItems'
