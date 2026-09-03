from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder import BulkScheduleFinalizeBuilder
from api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner
from api.itinerary.scheduling.bulk.bulk_schedule_loop_packer import BulkScheduleLoopPacker
from api.itinerary.scheduling.bulk.bulk_schedule_loop_packing_result import BulkScheduleLoopPackingResult
from api.itinerary.scheduling.bulk.bulk_schedule_transit_legs_builder import BulkScheduleTransitLegsBuilder
from api.itinerary.scheduling.bulk.bulk_schedule_window_preparer import BulkScheduleWindowPreparer
from api.itinerary.scheduling.bulk.guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.prepared_schedule_window import PreparedScheduleWindow
from api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer import ScheduledEndpointVisitTimesSyncer
from api.models import Animal
from api.models.guardians_talk import GuardiansTalk
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


EMPTY_SAVED_ITINERARY = SavedItinerary(
   date_value=None,
   arrival_time=None,
   departure_time=None,
)

DATE_ONLY_SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
)

TALK_ONLY_SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   guardians_talk_rows=[
      ItineraryGuardiansTalkRecord(
         talk_name="Grevy's Zebra",
         start_time='2:00 PM',
         end_time='2:30 PM',
         is_deleted=False,
      ),
   ],
)

TALK_ONLY_ITINERARY = ItineraryBuilder.build(
   date='2026-06-15',
   selected_exhibits=[],
   animals=[],
   attractions=[],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[
      GuardiansTalk(
         name="Grevy's Zebra",
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='2:00 PM',
         end_time='2:30 PM',
      ),
   ],
   wild_encounters=[],
   events=[],
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
)

ITINERARY_CONTEXT = { 'visit_date_temp': None }


class _TalkOnlyPrep:
   previous_itinerary = TALK_ONLY_ITINERARY


@pytest.fixture
def bulk_runner_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_bulk_runner_context( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ItineraryScheduleContextBuilder.build',
      lambda **kwargs: ITINERARY_CONTEXT )


def Test_IsAnimalUnscheduled_TestScheduleTimes_ExpectUnscheduledWhenIncomplete() -> None:
   assert BulkScheduleItineraryRunner.is_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      )
   )
   assert BulkScheduleItineraryRunner.is_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='',
         end_time='',
      )
   )
   assert not BulkScheduleItineraryRunner.is_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='09:30',
         end_time='09:38',
      )
   )


def Test_Run_TestEmptyItinerary_ExpectAlreadyScheduled(
      bulk_runner_conn: sqlite3.Connection,
      stub_bulk_runner_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: EMPTY_SAVED_ITINERARY )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = BulkScheduleItineraryRunner.run(
      bulk_runner_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result.status == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED


def Test_Run_TestDateOnlyItinerary_ExpectAlreadyScheduled(
      bulk_runner_conn: sqlite3.Connection,
      stub_bulk_runner_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: DATE_ONLY_SAVED_ITINERARY )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'save_result',
      lambda conn, status, **context: ItinerarySaveResult(
         status=status,
         reasons=[],
         itinerary=ItineraryBuilder.build(
            date='2026-06-20',
            selected_exhibits=[],
            animals=[],
            attractions=[],
            transportations=[],
            transportation_stations=[],
            guardians_talks=[],
            wild_encounters=[],
            events=[],
            arrival_time='9:30 AM',
            departure_time='5:00 PM',
         ) ) )

   result = BulkScheduleItineraryRunner.run(
      bulk_runner_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result.status == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED
   assert result.reasons == []
   assert result.itinerary.animals == []


def Test_Run_TestTalkOnlyItinerary_ExpectSuccess(
      bulk_runner_conn: sqlite3.Connection,
      stub_bulk_runner_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=TALK_ONLY_SAVED_ITINERARY,
      window=( 9 * 3600, 17 * 3600 ),
      visit_date=date( 2026, 6, 15 ),
   )
   prep = _TalkOnlyPrep()
   packing = BulkScheduleLoopPackingResult(
      remaining_stops=[],
      covered_by_talk={ 'talk-covered': () },
      covered_by_attraction={},
      schedule_windows=[],
      loop_units=[],
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: TALK_ONLY_SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      BulkScheduleWindowPreparer,
      'prepare_windows',
      lambda conn, prepared_window, itinerary_context: prep )
   monkeypatch.setattr(
      BulkScheduleLoopPacker,
      'pack_stops',
      lambda conn, prep, stops_to_schedule: packing )
   monkeypatch.setattr( GuardiansTalkAnimalCoverer, 'apply', lambda conn, covered_by_talk: None )
   monkeypatch.setattr( BulkScheduleTransitLegsBuilder, 'apply', lambda conn, prep: None )
   monkeypatch.setattr(
      BulkScheduleFinalizeBuilder,
      'finalize',
      lambda conn, previous_itinerary, itinerary_context, **kwargs: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=previous_itinerary,
      ) )

   result = BulkScheduleItineraryRunner.run(
      bulk_runner_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result.status == ItineraryErrorType.SUCCESS
   assert len( result.itinerary.guardians_talks ) == 1
   assert result.itinerary.guardians_talks[ 0 ].start_time is not None


def Test_Run_TestRemainingStopsFromPacker_ExpectSuccessWithNotEnoughTimeIssue(
      bulk_runner_conn: sqlite3.Connection,
      stub_bulk_runner_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time=None,
      animal_rows=[
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Indo-Malaya',
            old_likelihood=None,
            new_likelihood=100,
            start_time='9:30 AM',
            end_time='9:38 AM',
         ),
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
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=( 9 * 3600 + 30 * 60, 9 * 3600 + 41 * 60 ),
      visit_date=date( 2026, 6, 20 ),
   )
   prep = _TalkOnlyPrep()
   prep.previous_itinerary = ItineraryBuilder.build(
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
   packing = BulkScheduleLoopPackingResult(
      remaining_stops=[
         ItineraryAnimalRecord(
            species='African Penguin',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100,
         ),
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
      covered_by_talk={},
      covered_by_attraction={},
      schedule_windows=[],
      loop_units=[ object() ],
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      BulkScheduleWindowPreparer,
      'prepare_windows',
      lambda conn, prepared_window, itinerary_context: prep )
   monkeypatch.setattr(
      BulkScheduleLoopPacker,
      'pack_stops',
      lambda conn, prep, stops_to_schedule: packing )
   monkeypatch.setattr( GuardiansTalkAnimalCoverer, 'apply', lambda conn, covered_by_talk: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.AttractionAnimalCoverer.apply',
      lambda conn, covered_by_attraction: None )
   monkeypatch.setattr( BulkScheduleTransitLegsBuilder, 'apply', lambda conn, prep: None )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_finalize_builder.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: prep.previous_itinerary )
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

   result = BulkScheduleItineraryRunner.run(
      bulk_runner_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result.status == ItineraryErrorType.SUCCESS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME )
   assert result.itinerary.departure_time is None


def Test_Run_TestPrepareWindowFailure_ExpectSaveResult(
      bulk_runner_conn: sqlite3.Connection,
      stub_bulk_runner_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   failure = ItinerarySaveResult(
      status=ItineraryErrorType.SAVE_FAILED,
      reasons=[],
      itinerary=ItineraryBuilder.empty() )
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: failure )

   result = BulkScheduleItineraryRunner.run(
      bulk_runner_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      animals_to_schedule=list( saved_itinerary.animal_rows ) )

   assert result is failure


def Test_Run_TestEmptyPackingResult_ExpectFinalize(
      bulk_runner_conn: sqlite3.Connection,
      stub_bulk_runner_context: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )
   prepared_window = PreparedScheduleWindow(
      saved_itinerary=saved_itinerary,
      window=( 9 * 3600 + 30 * 60, 17 * 3600 ),
      visit_date=date( 2026, 6, 20 ),
   )
   prep = _TalkOnlyPrep()
   empty_packing = BulkScheduleLoopPackingResult(
      remaining_stops=[],
      covered_by_talk=False,
      covered_by_attraction=False,
      schedule_windows=[],
      loop_units=[] )
   finalized = ItinerarySaveResult(
      status=ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
      reasons=[],
      itinerary=ItineraryBuilder.empty() )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner.ScheduleWindowPreparer.prepare_zoo_hours',
      lambda conn, saved_itinerary, **context: prepared_window )
   monkeypatch.setattr(
      BulkScheduleWindowPreparer,
      'prepare_windows',
      lambda conn, *, prepared_window, itinerary_context: prep )
   monkeypatch.setattr(
      BulkScheduleLoopPacker,
      'pack_stops',
      lambda conn, *, prep, stops_to_schedule: empty_packing )
   monkeypatch.setattr(
      BulkScheduleFinalizeBuilder,
      'finalize',
      lambda conn, *, previous_itinerary, itinerary_context: finalized )

   result = BulkScheduleItineraryRunner.run(
      bulk_runner_conn,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator )

   assert result is finalized
