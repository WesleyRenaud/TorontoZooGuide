from __future__ import annotations

from typing import Any

from ...data_access.itinerary_provider import ItineraryProvider
from ...domain.itinerary_builder import ItineraryBuilder
from ..items.schedule_itinerary_helpers import persist_itinerary_walk_route
from .loop_schedule_stop import LoopScheduleStop
from ....models import Itinerary
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ....shared.enums import ItineraryErrorType
from ..sync_visit_times_to_scheduled_endpoints import clear_visit_times_if_became_incomplete
from ..sync_visit_times_to_scheduled_endpoints import sync_visit_times_to_scheduled_endpoints_if_complete
from ....types import Connection
from ...warnings.bulk_schedule_itinerary_warning_builder import BulkScheduleItineraryWarningBuilder


class BulkScheduleFinalizeBuilder():
   @classmethod
   def finalize(
         cls,
         conn: Connection,
         *,
         previous_itinerary: Itinerary,
         itinerary_context: dict[ str, Any ],
         remaining_stops: list[ LoopScheduleStop ] | None = None ) -> ItinerarySaveResult:
      reasons: list[ ItineraryResultReason ] = []

      if remaining_stops:
         reasons = [
            BulkScheduleItineraryWarningBuilder.build_not_enough_time_issue(
               remaining_stops ),
         ]

      sync_visit_times_to_scheduled_endpoints_if_complete(
         conn,
         ItineraryBuilder.build_current(
            ItineraryProvider.fetch_saved_itinerary( conn ),
            **itinerary_context ) )

      clear_visit_times_if_became_incomplete(
         conn,
         previous_itinerary=previous_itinerary,
         current_itinerary=ItineraryBuilder.build_current(
            ItineraryProvider.fetch_saved_itinerary( conn ),
            **itinerary_context ) )

      persist_itinerary_walk_route( conn, **itinerary_context )

      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=reasons,
         itinerary=ItineraryBuilder.build_current(
            ItineraryProvider.fetch_saved_itinerary( conn ),
            **itinerary_context ) )
