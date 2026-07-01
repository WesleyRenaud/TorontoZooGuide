from __future__ import annotations

from .enums import ItineraryErrorType
from .enums import ItineraryEventType
from ..itinerary.data_access.itinerary_status import fetch_itinerary_statuses
from ..itinerary.data_access.itinerary_status import fetch_suppressed_status_values
from ..itinerary.domain.itinerary_adjustment import ItineraryAdjustmentType
from ..types import Connection


OPEN_ENDED_SQL_DATE = '9999-12-31'
ANIMAL_VISIBILITY_CHANGE_THRESHOLD = 20
OUTDOOR_LIKELIHOOD_EXCLUDE_INDOOR_THRESHOLD = 50
MIN_ITINERARY_VISIT_DURATION_MINUTES = 120
SCHEDULE_SLOT_STEP_SECONDS = 30


def itinerary_config_to_dict(
      conn: Connection | None = None ) -> dict[
         str,
         int | list[ str ] | dict[ str, str ] | list[ dict[ str, bool | str ] ],
      ]:
   statuses = fetch_itinerary_statuses( conn ) if conn is not None else []

   config: dict[
         str,
         int | list[ str ] | dict[ str, str ] | list[ dict[ str, bool | str ] ],
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
      'itinerary_adjustment_types': {
         adjustment_type.name: adjustment_type.value
         for adjustment_type in ItineraryAdjustmentType
      },
      'itinerary_statuses': [
         {
            'status': status.status,
            'is_suppressable': status.is_suppressable,
            'is_suppressed': status.is_suppressed,
         }
         for status in statuses
      ],
      'suppressed_error_types': (
         fetch_suppressed_status_values( conn )
         if conn is not None
         else []
      ),
   }

   return config
