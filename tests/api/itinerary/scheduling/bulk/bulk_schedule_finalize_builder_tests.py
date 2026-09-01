from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder import BulkScheduleFinalizeBuilder
from api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer import ScheduledEndpointVisitTimesSyncer
from api.models import Animal
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType


CHEETAH = ItineraryAnimalRecord(
   species='Cheetah',
   exhibit='Indo-Malaya',
   old_likelihood=None,
   new_likelihood=100,
   start_time='9:30 AM',
   end_time='9:38 AM',
)
PENGUIN = ItineraryAnimalRecord(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
   old_likelihood=None,
   new_likelihood=100,
)
LION = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)

PARTIAL_SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time=None,
   departure_time=None,
   animal_rows=[
      CHEETAH,
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      ),
      ItineraryAnimalRecord(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         old_likelihood=None,
         new_likelihood=100,
      ),
   ],
)

FULLY_SCHEDULED_PREVIOUS_ITINERARY = ItineraryBuilder.build(
   date='2026-06-20',
   selected_exhibits=[],
   animals=[
      Animal(
         species='Cheetah',
         exhibit='Indo-Malaya',
         start_time='9:30 AM',
         end_time='9:38 AM' ),
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='9:40 AM',
         end_time='9:48 AM' ),
      Animal(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         start_time='9:50 AM',
         end_time='10:05 AM' ),
   ],
   attractions=[],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time='9:20 AM',
   departure_time='10:15 AM' )

PARTIAL_CURRENT_ITINERARY = ItineraryBuilder.build(
   date='2026-06-20',
   selected_exhibits=[],
   animals=[
      Animal(
         species='Cheetah',
         exhibit='Indo-Malaya',
         start_time='9:30 AM',
         end_time='9:38 AM' ),
      Animal(
         species='African Lion',
         exhibit='Africa Savanna' ),
      Animal(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor' ),
   ],
   attractions=[],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time=None,
   departure_time=None )

ITINERARY_CONTEXT = { 'visit_date_temp': None }


@pytest.fixture
def finalize_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Finalize_TestRemainingStops_ExpectNotEnoughTimeIssue(
      finalize_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: PARTIAL_SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: PARTIAL_CURRENT_ITINERARY )
   monkeypatch.setattr(
      ScheduledEndpointVisitTimesSyncer,
      'sync_if_complete',
      lambda conn, itinerary: None )
   monkeypatch.setattr(
      ScheduledEndpointVisitTimesSyncer,
      'clear_if_became_incomplete',
      lambda conn, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItinerarySaveResultBuilder.persist_walk_route',
      lambda conn, **context: None )

   result = BulkScheduleFinalizeBuilder.finalize(
      finalize_conn,
      previous_itinerary=FULLY_SCHEDULED_PREVIOUS_ITINERARY,
      itinerary_context=ITINERARY_CONTEXT,
      remaining_stops=[ PENGUIN, LION ] )

   assert result.status == ItineraryErrorType.SUCCESS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [
      'African Penguin',
      'African Lion',
   ]
   assert [ item.location for item in result.reasons[ 0 ].items ] == [
      'Africa Savanna',
      'Africa Savanna',
   ]
   assert result.reasons[ 0 ].items[ 0 ].item_type == ItinerarySaveIssueItemType.ANIMAL
   assert {
      animal.species
      for animal in result.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   } == { 'Cheetah' }


def Test_Finalize_TestRemainingStops_ExpectVisitTimesClearedWhenIncomplete(
      finalize_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: PARTIAL_SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: PARTIAL_CURRENT_ITINERARY )
   monkeypatch.setattr(
      ScheduledEndpointVisitTimesSyncer,
      'sync_if_complete',
      lambda conn, itinerary: calls.append( 'sync' ) )
   monkeypatch.setattr(
      ScheduledEndpointVisitTimesSyncer,
      'clear_if_became_incomplete',
      lambda conn, **kwargs: calls.append( 'clear' ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItinerarySaveResultBuilder.persist_walk_route',
      lambda conn, **context: None )

   result = BulkScheduleFinalizeBuilder.finalize(
      finalize_conn,
      previous_itinerary=FULLY_SCHEDULED_PREVIOUS_ITINERARY,
      itinerary_context=ITINERARY_CONTEXT,
      remaining_stops=[ PENGUIN, LION ] )

   assert result.status == ItineraryErrorType.SUCCESS
   assert calls == [ 'sync', 'clear' ]
   assert result.itinerary.arrival_time is None
   assert result.itinerary.departure_time is None
   assert any(
      animal.start_time is not None
      for animal in result.itinerary.animals )


def Test_Finalize_TestNoRemainingStops_ExpectNoIssue(
      finalize_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: PARTIAL_SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: FULLY_SCHEDULED_PREVIOUS_ITINERARY )
   monkeypatch.setattr(
      ScheduledEndpointVisitTimesSyncer,
      'sync_if_complete',
      lambda conn, itinerary: None )
   monkeypatch.setattr(
      ScheduledEndpointVisitTimesSyncer,
      'clear_if_became_incomplete',
      lambda conn, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItinerarySaveResultBuilder.persist_walk_route',
      lambda conn, **context: None )

   result = BulkScheduleFinalizeBuilder.finalize(
      finalize_conn,
      previous_itinerary=FULLY_SCHEDULED_PREVIOUS_ITINERARY,
      itinerary_context=ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []
