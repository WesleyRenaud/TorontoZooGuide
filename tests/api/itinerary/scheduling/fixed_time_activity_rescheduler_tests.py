from __future__ import annotations

import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner
from api.itinerary.scheduling.bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector
from api.itinerary.scheduling.fixed_time_activity_rescheduler import FixedTimeActivityRescheduler
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


SAVED_ITINERARY_BEFORE = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM',
      ),
   ],
)

SAVED_ITINERARY_AFTER = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
)


@pytest.fixture
def rescheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_RescheduleAfterAdd_TestNoStopsToSchedule_ExpectSuccess(
      rescheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.fixed_time_activity_rescheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY_AFTER )
   monkeypatch.setattr(
      BulkScheduleStopSelector,
      'stops_matching_previous',
      lambda saved_itinerary_before, saved_itinerary_after: [] )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = FixedTimeActivityRescheduler.reschedule_after_add(
      rescheduler_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      saved_itinerary_before_clear=SAVED_ITINERARY_BEFORE )

   assert result.status == ItineraryErrorType.SUCCESS


def Test_RescheduleAfterAdd_TestHasStops_ExpectBulkRunnerCalled(
      rescheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.fixed_time_activity_rescheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY_AFTER )
   monkeypatch.setattr(
      BulkScheduleStopSelector,
      'stops_matching_previous',
      lambda saved_itinerary_before, saved_itinerary_after: [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM',
         ),
      ] )

   def run(
         conn: sqlite3.Connection,
         *,
         stops_to_schedule: list[ ItineraryAnimalRecord ],
         confirming_fixed_time_item_long_wait: bool,
         **context: object ) -> ItinerarySaveResult:
      captured[ 'stops_to_schedule' ] = stops_to_schedule
      captured[ 'confirming_fixed_time_item_long_wait' ] = (
         confirming_fixed_time_item_long_wait )
      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() )

   monkeypatch.setattr( BulkScheduleItineraryRunner, 'run', run )

   result = FixedTimeActivityRescheduler.reschedule_after_add(
      rescheduler_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      saved_itinerary_before_clear=SAVED_ITINERARY_BEFORE )

   assert result.status == ItineraryErrorType.SUCCESS
   assert len( captured[ 'stops_to_schedule' ] ) == 1
   assert captured[ 'stops_to_schedule' ][ 0 ].species == 'African Lion'
   assert captured[ 'confirming_fixed_time_item_long_wait' ] is True
