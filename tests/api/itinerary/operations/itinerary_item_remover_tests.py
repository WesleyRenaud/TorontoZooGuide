from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.itinerary_item_remover import ItineraryItemRemover
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.shared.enums import ItineraryErrorType


ZOOMOBILE = 'Zoomobile'


@pytest.fixture
def remover_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_IsTransitModeTransportationKey_TestTransitRow_ExpectTrue() -> None:
   assert ItineraryItemRemover.is_transit_mode_transportation_key(
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=False ) )


def Test_IsTransitModeTransportationKey_TestAttractionRow_ExpectFalse() -> None:
   assert not ItineraryItemRemover.is_transit_mode_transportation_key(
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=True ) )


def Test_RemoveTransitTransportationAndReschedule_TestNoStops_ExpectSyncCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: object() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      ItineraryItemRemover,
      'apply',
      lambda cur, schedule_item_key: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.BulkScheduleStopSelector.stops_matching_previous',
      lambda saved_before, saved_after: [] )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ScheduledEndpointVisitTimesSyncer.sync_if_complete',
      lambda conn, itinerary: calls.append( 'sync' ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda conn, *, previous_itinerary, current_itinerary: calls.append( 'clear' ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItinerarySaveResultBuilder.persist_walk_route',
      lambda conn, **context: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItinerarySaveResultBuilder.success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ItineraryItemRemover.remove_transit_transportation_and_reschedule(
      remover_conn,
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=False ) )

   assert result.status == ItineraryErrorType.SUCCESS
   assert calls == [ 'sync', 'clear' ]
