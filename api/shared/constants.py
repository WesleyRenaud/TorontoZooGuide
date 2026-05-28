from .enums import ItineraryEventType


OPEN_ENDED_SQL_DATE = '9999-12-31'
ANIMAL_VISIBILITY_CHANGE_THRESHOLD = 20


def itinerary_config_to_dict() -> dict[ str, int | list[ str ] ]:
   return {
      'animal_visibility_change_threshold': ANIMAL_VISIBILITY_CHANGE_THRESHOLD,
      'itinerary_event_types': [
         event_type.value for event_type in ItineraryEventType
      ],
   }
