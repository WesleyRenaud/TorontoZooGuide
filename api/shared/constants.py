from .enums import ItineraryErrorType
from .enums import ItineraryEventType


OPEN_ENDED_SQL_DATE = '9999-12-31'
ANIMAL_VISIBILITY_CHANGE_THRESHOLD = 20
MIN_ITINERARY_VISIT_DURATION_MINUTES = 120


def itinerary_config_to_dict() -> dict[ str, int | list[ str ] | dict[ str, str ] ]:
   return {
      'animal_visibility_change_threshold': ANIMAL_VISIBILITY_CHANGE_THRESHOLD,
      'itinerary_event_types': [
         event_type.value for event_type in ItineraryEventType
      ],
      'itinerary_error_types': {
         error_type.name: error_type.value
         for error_type in ItineraryErrorType
      },
   }
