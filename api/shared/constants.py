from __future__ import annotations

from .enums import ItineraryErrorType
from .enums import ItineraryEventType
from .enums import ItineraryTransportationStationRole
from ..itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from ..itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType
from ..types import Connection


OPEN_ENDED_SQL_DATE = '9999-12-31'
ANIMAL_VISIBILITY_CHANGE_THRESHOLD = 20
ITINERARY_ANIMAL_MIN_LIKELIHOOD = 40
MIN_ITINERARY_VISIT_DURATION_MINUTES = 120
MAX_FIXED_TIME_ITEM_WAIT_MINUTES = 30
SCHEDULE_SLOT_STEP_SECONDS = 30
SCHEDULED_OCCURRENCE_DAYS_AHEAD = 60
# Insert a Zoomobile ride between two anchors when the remaining walk
# (to board + from alight) is at most this fraction of walking the whole way.
TRANSPORTATION_WALK_SAVINGS_MAX_REMAINING_FRACTION = 0.5
# Reject a Zoomobile transfer when ride time is more than this multiple of
# the direct walk minutes (allows modestly longer rides; blocks full-loop hops).
TRANSPORTATION_RIDE_MAX_WALK_DURATION_MULTIPLIER = 2


def itinerary_config_to_dict(
      conn: Connection | None = None ) -> dict[
         str,
         int | list[ str ] | dict[ str, str ] | list[ dict[ str, bool | str ] ],
      ]:
   statuses = ItineraryStatusProvider.fetch_itinerary_statuses( conn ) if conn is not None else []

   config: dict[
         str,
         int | list[ str ] | dict[ str, str ] | list[ dict[ str, bool | str ] ],
      ] = {
      'animal_visibility_change_threshold': ANIMAL_VISIBILITY_CHANGE_THRESHOLD,
      'itinerary_animal_min_likelihood': ITINERARY_ANIMAL_MIN_LIKELIHOOD,
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
      'itinerary_transportation_station_roles': (
         ItineraryTransportationStationRole.to_config_dict()
      ),
      'itinerary_transportation_station_onboarding_roles': (
         ItineraryTransportationStationRole.onboarding_role_values()
      ),
      'itinerary_transportation_station_offboarding_roles': (
         ItineraryTransportationStationRole.offboarding_role_values()
      ),
      'itinerary_statuses': [
         {
            'status': status.status,
            'is_suppressable': status.is_suppressable,
            'is_suppressed': status.is_suppressed,
         }
         for status in statuses
      ],
      'suppressed_error_types': (
         ItineraryStatusProvider.fetch_suppressed_status_values( conn )
         if conn is not None
         else []
      ),
   }

   return config
