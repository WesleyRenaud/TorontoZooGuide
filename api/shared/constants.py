from .enums import ItineraryErrorType
from .enums import ItineraryEventType
from ..itinerary.data_access.itinerary_error_suppression import fetch_suppressed_error_type_values
from ..types import Connection


OPEN_ENDED_SQL_DATE = '9999-12-31'
ANIMAL_VISIBILITY_CHANGE_THRESHOLD = 20
MIN_ITINERARY_VISIT_DURATION_MINUTES = 120
SCHEDULE_SLOT_STEP_SECONDS = 30


def itinerary_config_to_dict(
      conn: Connection | None = None ) -> dict[
         str,
         int | list[ str ] | dict[ str, str ],
      ]:
   config: dict[
         str,
         int | list[ str ] | dict[ str, str ],
      ] = {
      'animal_visibility_change_threshold': ANIMAL_VISIBILITY_CHANGE_THRESHOLD,
      'itinerary_event_types': [
         event_type.value for event_type in ItineraryEventType
      ],
      'itinerary_visit_boundary_event_types': {
         'arrival': ItineraryEventType.ARRIVAL.value,
         'departure': ItineraryEventType.DEPARTURE.value,
      },
      'itinerary_error_types': {
         error_type.name: error_type.value
         for error_type in ItineraryErrorType
      },
      'suppressed_error_types': (
         fetch_suppressed_error_type_values( conn )
         if conn is not None
         else []
      ),
   }

   return config
