from __future__ import annotations

import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.all_itinerary_items_unscheduler import AllItineraryItemsUnscheduler
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.models import Animal, Attraction
from api.shared.enums import ItineraryErrorType, ItineraryEventType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


CAROUSEL = 'Conservation Carousel'
ITINERARY_CONTEXT = { 'visit_date_temp': 20.0 }

SCHEDULED_SAVED_ITINERARY = SavedItinerary(
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
   attraction_rows=[
      ItineraryAttractionRecord(
         attraction=CAROUSEL,
         old_likelihood=None,
         new_likelihood=None,
         start_time='11:00 AM',
         end_time='11:20 AM',
      ),
   ],
   event_rows=[
      ItineraryEventRecord(
         event_type=ItineraryEventType.LUNCH,
         start_time='12:00 PM',
         end_time='12:30 PM',
      ),
   ],
)

UNSCHEDULED_SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
      ),
   ],
   attraction_rows=[
      ItineraryAttractionRecord(
         attraction=CAROUSEL,
         old_likelihood=None,
         new_likelihood=None,
      ),
   ],
)

CLEARED_ITINERARY = ItineraryBuilder.build(
   date='2026-06-15',
   selected_exhibits=[],
   animals=[
      Animal(
         species='African Lion',
         exhibit='Africa Savanna' ),
   ],
   attractions=[
      Attraction( name=CAROUSEL, free_with_admission=0 ),
   ],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time='9:30 AM',
   departure_time='5:00 PM' )


@pytest.fixture
def unschedule_all_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_unschedule_all_context( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryScheduleContextBuilder.build',
      lambda **kwargs: ITINERARY_CONTEXT )


def Test_UnscheduleAll_TestScheduledGuestItems_ExpectClearedSchedules(
      unschedule_all_conn: sqlite3.Connection,
      stub_unschedule_all_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   cleared: list[ str ] = []
   fetch_calls = [ SCHEDULED_SAVED_ITINERARY, UNSCHEDULED_SAVED_ITINERARY ]

   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: fetch_calls.pop( 0 ) )
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryScheduleClearer.clear_all',
      lambda conn: cleared.append( 'cleared' ) )
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: CLEARED_ITINERARY )

   result = AllItineraryItemsUnscheduler.unschedule_all(
      unschedule_all_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert cleared == [ 'cleared' ]
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.itinerary.animals[ 0 ].start_time is None
   assert result.itinerary.attractions[ 0 ].start_time is None
   assert result.itinerary.events == []


def Test_UnscheduleAll_TestScheduledGuestItems_ExpectArrivalDeparturePreserved(
      unschedule_all_conn: sqlite3.Connection,
      stub_unschedule_all_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   fetch_calls = [ SCHEDULED_SAVED_ITINERARY, UNSCHEDULED_SAVED_ITINERARY ]

   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: fetch_calls.pop( 0 ) )
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryScheduleClearer.clear_all',
      lambda conn: None )
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: CLEARED_ITINERARY )

   result = AllItineraryItemsUnscheduler.unschedule_all(
      unschedule_all_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result.itinerary.arrival_time == '9:30 AM'
   assert result.itinerary.departure_time == '5:00 PM'


def Test_UnscheduleAll_TestEmptyItinerary_ExpectError(
      unschedule_all_conn: sqlite3.Connection,
      stub_unschedule_all_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value=None,
         arrival_time=None,
         departure_time=None,
      ) )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=CLEARED_ITINERARY ) )

   result = AllItineraryItemsUnscheduler.unschedule_all(
      unschedule_all_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result.status == ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED


def Test_UnscheduleAll_TestNothingGuestScheduled_ExpectError(
      unschedule_all_conn: sqlite3.Connection,
      stub_unschedule_all_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: UNSCHEDULED_SAVED_ITINERARY )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=CLEARED_ITINERARY ) )

   result = AllItineraryItemsUnscheduler.unschedule_all(
      unschedule_all_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result.status == ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED


def Test_UnscheduleAll_TestAlreadyUnscheduled_ExpectError(
      unschedule_all_conn: sqlite3.Connection,
      stub_unschedule_all_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   fetch_calls = [ SCHEDULED_SAVED_ITINERARY, UNSCHEDULED_SAVED_ITINERARY, UNSCHEDULED_SAVED_ITINERARY ]

   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: fetch_calls.pop( 0 ) )
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryScheduleClearer.clear_all',
      lambda conn: None )
   monkeypatch.setattr(
      'api.itinerary.operations.all_itinerary_items_unscheduler.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: CLEARED_ITINERARY )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=CLEARED_ITINERARY ) )

   first_result = AllItineraryItemsUnscheduler.unschedule_all(
      unschedule_all_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )
   second_result = AllItineraryItemsUnscheduler.unschedule_all(
      unschedule_all_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert first_result.status == ItineraryErrorType.SUCCESS
   assert second_result.status == ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED
