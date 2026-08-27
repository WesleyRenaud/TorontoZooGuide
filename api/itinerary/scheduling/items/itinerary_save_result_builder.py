from __future__ import annotations

from typing import Any

from ...data_access.itinerary_provider import ItineraryProvider
from ...domain.itinerary_adjustment import ItineraryAdjustment
from ...domain.itinerary_builder import ItineraryBuilder
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ....shared.enums import ItineraryErrorType
from ....types import Connection


class ItinerarySaveResultBuilder():
   @classmethod
   def save_result(
         cls,
         conn: Connection,
         status: ItineraryErrorType,
         *,
         reasons: list[ ItineraryResultReason ] | None = None,
         suppressed_warnings: list[ ItineraryErrorType ] | None = None,
         **itinerary_context: Any ) -> ItinerarySaveResult:
      return ItinerarySaveResult(
         status=status,
         reasons=reasons or [],
         suppressed_warnings=suppressed_warnings or [],
         itinerary=ItineraryBuilder.build_current(
            ItineraryProvider.fetch_saved_itinerary( conn ),
            **itinerary_context ) )


   @classmethod
   def success_result(
         cls,
         conn: Connection,
         *,
         adjustments: list[ ItineraryAdjustment ] | None = None,
         suppressed_warnings: list[ ItineraryErrorType ] | None = None,
         **itinerary_context: Any ) -> ItinerarySaveResult:
      return ItinerarySaveResult(
         adjustments=adjustments or [],
         suppressed_warnings=suppressed_warnings or [],
         itinerary=ItineraryBuilder.build_current(
            ItineraryProvider.fetch_saved_itinerary( conn ),
            **itinerary_context ) )


   @classmethod
   def persist_walk_route(
         cls,
         conn: Connection,
         **itinerary_context: Any ) -> None:
      from ...routing.persist_itinerary_walk_route import rebuild_and_persist_itinerary_walk_route

      rebuild_and_persist_itinerary_walk_route( conn, **itinerary_context )
