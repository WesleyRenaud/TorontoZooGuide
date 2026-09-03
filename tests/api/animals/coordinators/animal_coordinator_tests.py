from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import sqlite3
from typing import cast

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.data_access.animal_information_provider import AnimalInformationProvider
from api.animals.data_access.animal_species_name_provider import AnimalSpeciesNameProvider
from api.animals.data_access.animal_status_provider import AnimalStatusProvider
from api.animals.data_access.animal_viewable_on_day_provider import AnimalViewableOnDayProvider
from api.animals.data_access.animal_viewing_alert_provider import AnimalViewingAlertProvider
from api.animals.data_access.animal_viewing_scope_provider import AnimalViewingScopeProvider
from api.animals.data_access.animal_visibility_schedule_provider import AnimalVisibilityScheduleProvider
from api.animals.domain.animal_viewability_builder import AnimalViewabilityBuilder
from api.animals.domain.animal_viewability_context_builder import AnimalViewabilityContextBuilder
from api.animals.domain.itinerary_animal_records_filter_builder import ItineraryAnimalRecordsFilterBuilder
from api.animals.scheduling.animal_limited_viewing_schedule import AnimalLimitedViewingSchedule
from api.animals.scheduling.animal_limited_viewing_schedule_builder import AnimalLimitedViewingScheduleBuilder
from api.animals.search.animals_matching_query_builder import AnimalsMatchingQueryBuilder
from api.animals.status.animal_off_display_status import AnimalOffDisplayStatus
from api.animals.status.animal_off_display_status_builder import AnimalOffDisplayStatusBuilder
from api.animals.status.animal_viewing_alert import AnimalViewingAlert
from api.animals.status.animal_viewing_alert_builder import AnimalViewingAlertBuilder
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator import BulkRescheduleLongWaitSimulator
from api.itinerary.scheduling.bulk.loop_schedule_slot import LoopScheduleSlot
from api.itinerary.scheduling.items.prepared_schedule_window import PreparedScheduleWindow
from api.itinerary.scheduling.items.schedule_window_preparer import ScheduleWindowPreparer
from api.models import Animal
from api.models import Attraction
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.models.animal_diff import AnimalDiff
from api.models.attraction_diff import AttractionDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.request_connection_provider import RequestConnectionProvider
from api.shared.enums import AnimalViewingScope
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums import ScheduleItemKind
from api.types import Types
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


VISIT_DATE = date( 2026, 6, 15 )
LION_SPECIES = 'African Lion'
LION_EXHIBIT = 'Africa Savanna'
SPLASH_ISLAND = 'Splash Island'
MEERKAT_TALK = 'Slender-Tailed Meerkat'
ARRIVAL_TIME = '9:30 AM'
DEPARTURE_TIME = '5:00 PM'
ANIMAL_START = '10:00 AM'
ANIMAL_END = '10:08 AM'
TALK_START = '1:00 PM'
TALK_END = '1:30 PM'
ATTRACTION_START = '2:00 PM'
ATTRACTION_END = '3:00 PM'
WINDOW_ANCHOR_SECONDS = 9 * 3600 + 30 * 60
WINDOW_END_SECONDS = 17 * 3600

ITINERARY_CONTEXT = {
   'animal_coordinator': AnimalCoordinator,
   'attraction_coordinator': AttractionCoordinator,
   'guardians_coordinator': GuardiansCoordinator,
   'wild_encounter_coordinator': WildEncounterCoordinator,
   'visit_date_temp': None,
}

ISOLATED_TALK = GuardiansTalk(
   name=MEERKAT_TALK,
   location='African Rainforest Pavilion',
   x_coord=0.0,
   y_coord=0.0,
   start_time=TALK_START,
   end_time=TALK_END,
)

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time=ARRIVAL_TIME,
   departure_time=DEPARTURE_TIME,
   animal_rows=[
      ItineraryAnimalRecord(
         species=LION_SPECIES,
         exhibit=LION_EXHIBIT,
         old_likelihood=None,
         new_likelihood=100,
         start_time=ANIMAL_START,
         end_time=ANIMAL_END,
      ),
   ],
)

LION_ANIMAL_ROW = ItineraryAnimalRecord(
   species=LION_SPECIES,
   exhibit=LION_EXHIBIT,
   old_likelihood=None,
   new_likelihood=100,
   start_time=ANIMAL_START,
   end_time=ANIMAL_END,
)


QUERY = 'lion'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Behind the scenes.'
DAILY_START = '10:00 AM'
DAILY_END = '4:00 PM'
SPECIES = 'African Lion'
EXHIBIT = 'Africa Savanna'
VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026

ANIMAL = Animal(
   species=SPECIES,
   exhibit=EXHIBIT )

@dataclass
class StubConnection:
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def _animal(
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name )

@pytest.fixture
def long_wait_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def _lion_animal(
      *,
      start_time: str | None = ANIMAL_START,
      end_time: str | None = ANIMAL_END,
      covered_by_talk: bool = False,
   ) -> Animal:
   return Animal(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      start_time=start_time,
      end_time=end_time,
      covered_by_talk=covered_by_talk )


def _splash_attraction(
      *,
      start_time: str | None = ATTRACTION_START,
      end_time: str | None = ATTRACTION_END,
   ) -> Attraction:
   return Attraction(
      name=SPLASH_ISLAND,
      free_with_admission=True,
      start_time=start_time,
      end_time=end_time )


def _timed_itinerary() -> Itinerary:
   return ItineraryBuilder.build(
      date=VISIT_DATE,
      selected_exhibits=[ LION_EXHIBIT ],
      animals=[ _lion_animal() ],
      attractions=[ _splash_attraction() ],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[ ISOLATED_TALK ],
      wild_encounters=[],
      events=[],
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME )


def Test_IsIsolatedAfterAdding_TestNotIsolatedOnCurrentItinerary_ExpectFalse(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding',
      lambda itinerary, new_item: False )

   assert BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
      long_wait_conn,
      ISOLATED_TALK,
      propose_on_itinerary=lambda itinerary, new_item, context: itinerary,
      itinerary_context=ITINERARY_CONTEXT ) is False


def Test_IsIsolatedAfterAdding_TestIsolatedWithNoAnimalsToPack_ExpectTrue(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   empty_saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: empty_saved )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding',
      lambda itinerary, new_item: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleStopSelector.animals',
      lambda saved_itinerary, *, only_previously_scheduled: [] )

   assert BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
      long_wait_conn,
      ISOLATED_TALK,
      propose_on_itinerary=lambda itinerary, new_item, context: itinerary,
      itinerary_context=ITINERARY_CONTEXT ) is True


def Test_IsIsolatedAfterAdding_TestProposedItineraryMissing_ExpectTrue(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding',
      lambda itinerary, new_item: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleStopSelector.animals',
      lambda saved_itinerary, *, only_previously_scheduled: [ LION_ANIMAL_ROW ] )

   assert BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
      long_wait_conn,
      ISOLATED_TALK,
      propose_on_itinerary=lambda itinerary, new_item, context: None,
      itinerary_context=ITINERARY_CONTEXT ) is True


def Test_IsIsolatedAfterAdding_TestFullPackPathStillIsolated_ExpectTrue(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   proposed = _timed_itinerary()
   packed = _timed_itinerary()

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding',
      lambda itinerary, new_item: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleStopSelector.animals',
      lambda saved_itinerary, *, only_previously_scheduled: [ LION_ANIMAL_ROW ] )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'pack_animals_in_memory',
      lambda conn, itinerary, *, animals_to_schedule, itinerary_context: packed )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated_on_schedule',
      lambda new_item_block, schedule_blocks: True )

   assert BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
      long_wait_conn,
      ISOLATED_TALK,
      propose_on_itinerary=lambda itinerary, new_item, context: proposed,
      itinerary_context=ITINERARY_CONTEXT ) is True


def Test_IsIsolatedAfterAdding_TestPackReturnsNone_ExpectTrue(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding',
      lambda itinerary, new_item: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleStopSelector.animals',
      lambda saved_itinerary, *, only_previously_scheduled: [ LION_ANIMAL_ROW ] )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'pack_animals_in_memory',
      lambda conn, itinerary, *, animals_to_schedule, itinerary_context: None )

   assert BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
      long_wait_conn,
      ISOLATED_TALK,
      propose_on_itinerary=lambda itinerary, new_item, context: itinerary,
      itinerary_context=ITINERARY_CONTEXT ) is True


def Test_NewlyAddedReason_TestNoIsolatedNewItems_ExpectNone(
      long_wait_conn: sqlite3.Connection ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[
         AnimalDiff(
            species=LION_SPECIES,
            exhibit=LION_EXHIBIT,
            old_likelihood=None,
            new_likelihood=100,
            start_time=ANIMAL_START,
            end_time=ANIMAL_END ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )

   assert BulkRescheduleLongWaitSimulator.newly_added_reason(
      long_wait_conn,
      validated,
      visit_date=VISIT_DATE,
      itinerary_context=ITINERARY_CONTEXT,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-14',
         arrival_time=ARRIVAL_TIME,
         departure_time=DEPARTURE_TIME,
      ) ) is None


def Test_NewlyAddedReason_TestIsolatedNewTalk_ExpectLongWaitReason(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name=MEERKAT_TALK,
            is_deleted=False,
            start_time=TALK_START,
            end_time=TALK_END,
            location='African Rainforest Pavilion' ),
      ],
      wild_encounters=[],
      events=[],
   )

   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_has_newly_added_isolated_fixed_time_items',
      lambda validated_itinerary, item_type, *, saved_itinerary: (
         item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK ) )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_newly_added_long_wait_items_for_type',
      lambda validated_itinerary, item_type, *, packed_itinerary, saved_itinerary: (
         validated_itinerary.guardians_talks
         if item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK
         else [] ) )

   reason = BulkRescheduleLongWaitSimulator.newly_added_reason(
      long_wait_conn,
      validated,
      visit_date=VISIT_DATE,
      itinerary_context=ITINERARY_CONTEXT,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-14',
         arrival_time=ARRIVAL_TIME,
         departure_time=DEPARTURE_TIME,
      ) )

   assert reason is not None
   assert reason.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in reason.items ] == [ MEERKAT_TALK ]


def Test_ItineraryWithClearedAnimalTimes_TestClearsAnimalAndAttractionTimes_ExpectNoneTimes() -> None:
   itinerary = _timed_itinerary()

   cleared = BulkRescheduleLongWaitSimulator._itinerary_with_cleared_animal_times( itinerary )

   assert cleared.animals[ 0 ].start_time is None
   assert cleared.animals[ 0 ].end_time is None
   assert cleared.animals[ 0 ].covered_by_talk is False
   assert cleared.attractions[ 0 ].start_time is None
   assert cleared.attractions[ 0 ].end_time is None
   assert cleared.guardians_talks[ 0 ].start_time == TALK_START
   assert itinerary.animals[ 0 ].start_time == ANIMAL_START


def Test_ApplySlotsToItineraryAnimals_TestAnimalAndAttractionSlots_ExpectTimesApplied() -> None:
   itinerary = _timed_itinerary()
   itinerary.animals[ 0 ].start_time = None
   itinerary.animals[ 0 ].end_time = None
   itinerary.attractions[ 0 ].start_time = None
   itinerary.attractions[ 0 ].end_time = None
   animal_row = ItineraryAnimalRecord(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      old_likelihood=None,
      new_likelihood=100 )
   attraction_row = ItineraryAttractionRecord(
      attraction=SPLASH_ISLAND,
      old_likelihood=None,
      new_likelihood=100 )
   slots = [
      LoopScheduleSlot( animal_row, '10:30 AM', '10:38 AM' ),
      LoopScheduleSlot( attraction_row, '11:00 AM', '12:00 PM' ),
   ]

   BulkRescheduleLongWaitSimulator._apply_slots_to_itinerary_animals( itinerary, slots )

   assert itinerary.animals[ 0 ].start_time == '10:30 AM'
   assert itinerary.animals[ 0 ].end_time == '10:38 AM'
   assert itinerary.attractions[ 0 ].start_time == '11:00 AM'
   assert itinerary.attractions[ 0 ].end_time == '12:00 PM'


def Test_ApplyTalkCovered_TestMatchingAnimal_ExpectTalkTimesAndCovered() -> None:
   itinerary = _timed_itinerary()
   itinerary.animals[ 0 ].start_time = None
   itinerary.animals[ 0 ].end_time = None
   animal_row = ItineraryAnimalRecord(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      old_likelihood=None,
      new_likelihood=100 )
   loop_pin = LoopSchedulePin(
      loop_id='africa_savanna',
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ 'n-talk' ],
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key=MEERKAT_TALK,
         start_time=TALK_START,
         end_time=TALK_END ),
      start_seconds=13 * 3600,
      end_seconds=13 * 3600 + 30 * 60 )

   BulkRescheduleLongWaitSimulator._apply_talk_covered_to_itinerary_animals(
      itinerary,
      { animal_row.viewing_spot_key(): ( animal_row, loop_pin ) } )

   assert itinerary.animals[ 0 ].start_time == TALK_START
   assert itinerary.animals[ 0 ].end_time == TALK_END
   assert itinerary.animals[ 0 ].covered_by_talk is True


def Test_ApplyAttractionCovered_TestMatchingAnimalAndTimedAttraction_ExpectCovered() -> None:
   itinerary = _timed_itinerary()
   itinerary.animals[ 0 ].start_time = None
   itinerary.animals[ 0 ].end_time = None
   animal_row = ItineraryAnimalRecord(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      old_likelihood=None,
      new_likelihood=100 )

   BulkRescheduleLongWaitSimulator._apply_attraction_covered_to_itinerary_animals(
      itinerary,
      { animal_row.viewing_spot_key(): ( animal_row, SPLASH_ISLAND ) } )

   assert itinerary.animals[ 0 ].start_time == ATTRACTION_START
   assert itinerary.animals[ 0 ].end_time == ATTRACTION_END
   assert itinerary.animals[ 0 ].covered_by_talk is True


def Test_ApplyAttractionCovered_TestAttractionMissingTimes_ExpectAnimalUnchanged() -> None:
   itinerary = _timed_itinerary()
   itinerary.animals[ 0 ].start_time = None
   itinerary.animals[ 0 ].end_time = None
   itinerary.attractions[ 0 ].start_time = None
   itinerary.attractions[ 0 ].end_time = None
   animal_row = ItineraryAnimalRecord(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      old_likelihood=None,
      new_likelihood=100 )

   BulkRescheduleLongWaitSimulator._apply_attraction_covered_to_itinerary_animals(
      itinerary,
      { animal_row.viewing_spot_key(): ( animal_row, SPLASH_ISLAND ) } )

   assert itinerary.animals[ 0 ].start_time is None
   assert itinerary.animals[ 0 ].covered_by_talk is False


def Test_BuildItineraryFromProposedItems_TestCoordinatorStubs_ExpectBuiltItinerary(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[
         AnimalDiff(
            species=LION_SPECIES,
            exhibit=LION_EXHIBIT,
            old_likelihood=None,
            new_likelihood=100,
            start_time=ANIMAL_START,
            end_time=ANIMAL_END ),
      ],
      attractions=[
         AttractionDiff(
            name=SPLASH_ISLAND,
            old_likelihood=None,
            new_likelihood=100,
            start_time=ATTRACTION_START,
            end_time=ATTRACTION_END ),
      ],
      guardians_talks=[
         GuardiansTalkDiff(
            name=MEERKAT_TALK,
            is_deleted=False,
            start_time=TALK_START,
            end_time=TALK_END ),
      ],
      wild_encounters=[
         WildEncounterDiff(
            name='Giraffe Encounter',
            is_deleted=False,
            start_time='3:00 PM',
            end_time='3:15 PM' ),
      ],
      events=[],
   )
   built_animals = [ _lion_animal() ]
   built_attractions = [ _splash_attraction() ]
   built_talks = [ ISOLATED_TALK ]
   built_encounters: list[ object ] = []

   class _AnimalCoordinator:
      @staticmethod
      def get_animals_for_saved_itinerary( **_kwargs: object ) -> list[ Animal ]:
         return built_animals

   class _AttractionCoordinator:
      @staticmethod
      def get_attractions_for_saved_itinerary( **_kwargs: object ) -> list[ Attraction ]:
         return built_attractions

   class _GuardiansCoordinator:
      @staticmethod
      def get_guardians_talks_for_saved_itinerary(
            _talk_rows: list[ ItineraryGuardiansTalkRecord ] ) -> list[ GuardiansTalk ]:
         return built_talks

   class _WildEncounterCoordinator:
      @staticmethod
      def get_wild_encounters_for_saved_itinerary(
            _encounter_rows: list[ ItineraryWildEncounterRecord ] ) -> list[ WildEncounter ]:
         return built_encounters

   context = {
      'animal_coordinator': _AnimalCoordinator,
      'attraction_coordinator': _AttractionCoordinator,
      'guardians_coordinator': _GuardiansCoordinator,
      'wild_encounter_coordinator': _WildEncounterCoordinator,
      'visit_date_temp': None,
   }

   built = BulkRescheduleLongWaitSimulator._build_itinerary_from_proposed_items(
      validated,
      visit_date=VISIT_DATE,
      itinerary_context=context )

   assert built.animals == built_animals
   assert built.attractions == built_attractions
   assert built.guardians_talks == built_talks
   assert built.arrival_time == ARRIVAL_TIME
   assert built.departure_time == DEPARTURE_TIME


def Test_PackAnimalsInMemory_TestEmptyAnimals_ExpectSameItinerary(
      long_wait_conn: sqlite3.Connection ) -> None:
   itinerary = _timed_itinerary()

   packed = BulkRescheduleLongWaitSimulator.pack_animals_in_memory(
      long_wait_conn,
      itinerary,
      animals_to_schedule=[],
      itinerary_context=ITINERARY_CONTEXT )

   assert packed is itinerary


def Test_PackAnimalsInMemory_TestZooHoursFail_ExpectNone(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   itinerary = _timed_itinerary()

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ScheduleWindowPreparer,
      'prepare_zoo_hours',
      lambda conn, saved_itinerary, **kwargs: ItinerarySaveResult(
         itinerary=ItineraryBuilder.empty(),
         status=ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE ) )

   assert BulkRescheduleLongWaitSimulator.pack_animals_in_memory(
      long_wait_conn,
      itinerary,
      animals_to_schedule=[ LION_ANIMAL_ROW ],
      itinerary_context=ITINERARY_CONTEXT ) is None


def Test_PackAnimalsInMemory_TestHappyPathWithStubs_ExpectSlotsAndCoverageApplied(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   itinerary = _timed_itinerary()
   schedule_calls: list[ object ] = []
   applied_slots: list[ list[ LoopScheduleSlot ] ] = []
   talk_cover_calls: list[ object ] = []
   attraction_cover_calls: list[ object ] = []
   animal_row = ItineraryAnimalRecord(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      old_likelihood=None,
      new_likelihood=100 )
   slot = LoopScheduleSlot( animal_row, '10:15 AM', '10:23 AM' )

   class _SlotSink:
      def __init__( self, *, persist: bool ) -> None:
         self.persist = persist
         self.slots = [ slot ]

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ScheduleWindowPreparer,
      'prepare_zoo_hours',
      lambda conn, saved_itinerary, **kwargs: PreparedScheduleWindow(
         saved_itinerary=saved_itinerary,
         window=( WINDOW_ANCHOR_SECONDS, WINDOW_END_SECONDS ),
         visit_date=VISIT_DATE ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.WalkGraphProvider.fetch',
      lambda: { 'entrance_node_id': 'n-entrance' } )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleWindowPreparer.start_state',
      lambda walk_graph, animal_rows, anchor_seconds: type(
         'StartState',
         (),
         {
            'schedule_anchor_seconds': anchor_seconds,
            'start_node_id': 'n-entrance',
         } )() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryStopResolver.resolve_fixed_time',
      lambda packing_itinerary: [] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleLoopPinAttacher.separate_boundaries_and_pins',
      lambda conn, packing_itinerary, fixed_time_stops: ( [], [] ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryScheduleWindowPartitioner.partition',
      lambda start_seconds, day_end_seconds, boundary_stops: [
         type( 'Window', (), { 'start_seconds': start_seconds, 'end_seconds': day_end_seconds } )(),
      ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleLoopPinAttacher.keep_completable',
      lambda schedule_windows, loop_pins: loop_pins )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.GuardiansTalkAnimalCoverer.keys_to_cover',
      lambda conn, loop_pins, animals_to_schedule: {} )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.AttractionAnimalCoverer.keys_to_cover',
      lambda conn, attraction_names, animals_to_schedule: {} )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.AttractionAnimalCoverer.merge_keys',
      lambda covered_by_talk, covered_by_attraction: set() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.GuardiansTalkAnimalCoverer.excluding_covered',
      lambda animals_to_schedule, covered_keys: animals_to_schedule )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.MasterRouteLoopAnimalGrouper.group',
      lambda animals_to_pack: [ animals_to_pack ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.LoopScheduleUnitBuilder.build',
      lambda sorted_loop_groups: [ object() ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleLoopPinAttacher.attach_to_windows',
      lambda schedule_windows, loop_pins: schedule_windows )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.LoopScheduleSlotSink',
      _SlotSink )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.MasterRouteLoopScheduler.schedule',
      lambda *args, **kwargs: schedule_calls.append( ( args, kwargs ) ) or ( [], WINDOW_ANCHOR_SECONDS ) )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_apply_slots_to_itinerary_animals',
      lambda packing_itinerary, slots: applied_slots.append( list( slots ) ) )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_apply_talk_covered_to_itinerary_animals',
      lambda packing_itinerary, covered_by_talk: talk_cover_calls.append( covered_by_talk ) )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_apply_attraction_covered_to_itinerary_animals',
      lambda packing_itinerary, covered_by_attraction: attraction_cover_calls.append(
         covered_by_attraction ) )

   packed = BulkRescheduleLongWaitSimulator.pack_animals_in_memory(
      long_wait_conn,
      itinerary,
      animals_to_schedule=[ LION_ANIMAL_ROW ],
      itinerary_context=ITINERARY_CONTEXT )

   assert packed is not None
   assert packed.animals[ 0 ].start_time is None
   assert schedule_calls
   assert applied_slots == [ [ slot ] ]
   assert talk_cover_calls == [ {} ]
   assert attraction_cover_calls == [ {} ]


def Test_IsIsolatedAfterAdding_TestInvalidNewItemTimes_ExpectFalse(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.ItineraryBuilder.build_current',
      lambda saved_itinerary, **kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding',
      lambda itinerary, new_item: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.BulkScheduleStopSelector.animals',
      lambda saved_itinerary, *, only_previously_scheduled: [ LION_ANIMAL_ROW ] )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'pack_animals_in_memory',
      lambda conn, itinerary, *, animals_to_schedule, itinerary_context: _timed_itinerary() )

   invalid_talk = GuardiansTalk(
      name=MEERKAT_TALK,
      location='African Rainforest Pavilion',
      x_coord=0.0,
      y_coord=0.0,
      start_time=None,
      end_time=None )

   assert BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
      long_wait_conn,
      invalid_talk,
      propose_on_itinerary=lambda itinerary, new_item, context: itinerary,
      itinerary_context=ITINERARY_CONTEXT ) is False


def Test_NewlyAddedReason_TestTimedAnimalsPacked_ExpectPackedIsolationPath(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[
         AnimalDiff(
            species=LION_SPECIES,
            exhibit=LION_EXHIBIT,
            old_likelihood=None,
            new_likelihood=100,
            start_time=ANIMAL_START,
            end_time=ANIMAL_END ),
      ],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name=MEERKAT_TALK,
            is_deleted=False,
            start_time=TALK_START,
            end_time=TALK_END,
            location='African Rainforest Pavilion' ),
      ],
      wild_encounters=[],
      events=[],
   )
   build_calls: list[ object ] = []
   pack_calls: list[ object ] = []

   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_has_newly_added_isolated_fixed_time_items',
      lambda validated_itinerary, item_type, *, saved_itinerary: True )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_build_itinerary_from_proposed_items',
      lambda validated_itinerary, *, visit_date, itinerary_context: (
         build_calls.append( validated_itinerary ) or _timed_itinerary() ) )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      'pack_animals_in_memory',
      lambda conn, itinerary, *, animals_to_schedule, itinerary_context: (
         pack_calls.append( animals_to_schedule ) or _timed_itinerary() ) )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_newly_added_long_wait_items_for_type',
      lambda validated_itinerary, item_type, *, packed_itinerary, saved_itinerary: (
         [ ISOLATED_TALK ]
         if packed_itinerary is not None and item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK
         else [] ) )

   reason = BulkRescheduleLongWaitSimulator.newly_added_reason(
      long_wait_conn,
      validated,
      visit_date=VISIT_DATE,
      itinerary_context=ITINERARY_CONTEXT,
      saved_itinerary=SAVED_ITINERARY )

   assert reason is not None
   assert reason.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert build_calls
   assert pack_calls
   assert pack_calls[ 0 ][ 0 ].species == LION_SPECIES
   assert pack_calls[ 0 ][ 0 ].start_time == ANIMAL_START


def Test_NewlyAddedReason_TestIsolatedButNoIssueItems_ExpectNone(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name=MEERKAT_TALK,
            is_deleted=False,
            start_time=TALK_START,
            end_time=TALK_END ),
      ],
      wild_encounters=[],
      events=[],
   )

   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_has_newly_added_isolated_fixed_time_items',
      lambda validated_itinerary, item_type, *, saved_itinerary: True )
   monkeypatch.setattr(
      BulkRescheduleLongWaitSimulator,
      '_newly_added_long_wait_items_for_type',
      lambda validated_itinerary, item_type, *, packed_itinerary, saved_itinerary: [] )

   assert BulkRescheduleLongWaitSimulator.newly_added_reason(
      long_wait_conn,
      validated,
      visit_date=VISIT_DATE,
      itinerary_context=ITINERARY_CONTEXT ) is None


def Test_NewlyAddedLongWaitItems_TestPackedItineraryFilters_ExpectMatchingNames(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name=MEERKAT_TALK,
            is_deleted=False,
            start_time=TALK_START,
            end_time=TALK_END,
            location='African Rainforest Pavilion' ),
         GuardiansTalkDiff(
            name='African Lion',
            is_deleted=False,
            start_time='2:00 PM',
            end_time='2:30 PM',
            location='Africa Savanna' ),
      ],
      wild_encounters=[],
      events=[],
   )
   packed = _timed_itinerary()

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary',
      lambda itinerary, item_type: [ ISOLATED_TALK ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.items_from_validated',
      lambda validated_itinerary, item_type: list( validated_itinerary.guardians_talks ) )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items',
      lambda saved_itinerary, isolated_items, item_type: isolated_items )

   items = BulkRescheduleLongWaitSimulator._newly_added_long_wait_items_for_type(
      validated,
      ItinerarySaveIssueItemType.GUARDIANS_TALK,
      packed_itinerary=packed,
      saved_itinerary=SAVED_ITINERARY )

   assert [ item.name for item in items ] == [ MEERKAT_TALK ]


def Test_HasNewlyAddedIsolated_TestNoSavedItinerary_ExpectBoolFromIsolated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.isolated_from_validated_itinerary',
      lambda validated_itinerary, item_type: [ ISOLATED_TALK ] )

   assert BulkRescheduleLongWaitSimulator._has_newly_added_isolated_fixed_time_items(
      validated,
      ItinerarySaveIssueItemType.GUARDIANS_TALK,
      saved_itinerary=None ) is True

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.isolated_from_validated_itinerary',
      lambda validated_itinerary, item_type: [] )

   assert BulkRescheduleLongWaitSimulator._has_newly_added_isolated_fixed_time_items(
      validated,
      ItinerarySaveIssueItemType.GUARDIANS_TALK,
      saved_itinerary=None ) is False


def Test_NewlyAddedLongWaitItems_TestNoSavedItinerary_ExpectAllIsolated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator.FixedTimeItemLongWaitWarningBuilder.isolated_from_validated_itinerary',
      lambda validated_itinerary, item_type: [ ISOLATED_TALK ] )

   items = BulkRescheduleLongWaitSimulator._newly_added_long_wait_items_for_type(
      validated,
      ItinerarySaveIssueItemType.GUARDIANS_TALK,
      packed_itinerary=None,
      saved_itinerary=None )

   assert items == [ ISOLATED_TALK ]


def Test_ApplySlotsToItineraryAnimals_TestUnknownTargets_ExpectSkipped() -> None:
   itinerary = _timed_itinerary()
   original_animal_start = itinerary.animals[ 0 ].start_time
   original_attraction_start = itinerary.attractions[ 0 ].start_time
   unknown_animal = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Indo-Malaya Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   unknown_attraction = ItineraryAttractionRecord(
      attraction='Conservation Carousel',
      old_likelihood=None,
      new_likelihood=100 )

   BulkRescheduleLongWaitSimulator._apply_slots_to_itinerary_animals(
      itinerary,
      [
         LoopScheduleSlot( unknown_attraction, '11:00 AM', '12:00 PM' ),
         LoopScheduleSlot( unknown_animal, '10:30 AM', '10:38 AM' ),
      ] )

   assert itinerary.animals[ 0 ].start_time == original_animal_start
   assert itinerary.attractions[ 0 ].start_time == original_attraction_start


def Test_ApplyTalkCovered_TestAnimalNotOnItinerary_ExpectSkipped() -> None:
   itinerary = _timed_itinerary()
   unknown_animal = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Indo-Malaya Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   loop_pin = LoopSchedulePin(
      loop_id='indo_malaya',
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ 'n-talk' ],
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key=MEERKAT_TALK,
         start_time=TALK_START,
         end_time=TALK_END ),
      start_seconds=13 * 3600,
      end_seconds=13 * 3600 + 30 * 60 )

   BulkRescheduleLongWaitSimulator._apply_talk_covered_to_itinerary_animals(
      itinerary,
      { unknown_animal.viewing_spot_key(): ( unknown_animal, loop_pin ) } )

   assert itinerary.animals[ 0 ].covered_by_talk is False


def Test_ApplyAttractionCovered_TestMissingAnimalOrAttraction_ExpectSkipped() -> None:
   itinerary = _timed_itinerary()
   unknown_animal = ItineraryAnimalRecord(
      species='Cheetah',
      exhibit='Indo-Malaya Outdoor',
      old_likelihood=None,
      new_likelihood=100 )
   lion_row = ItineraryAnimalRecord(
      species=LION_SPECIES,
      exhibit=LION_EXHIBIT,
      old_likelihood=None,
      new_likelihood=100 )

   BulkRescheduleLongWaitSimulator._apply_attraction_covered_to_itinerary_animals(
      itinerary,
      {
         unknown_animal.viewing_spot_key(): ( unknown_animal, SPLASH_ISLAND ),
         lion_row.viewing_spot_key(): ( lion_row, 'Missing Attraction' ),
      } )

   assert itinerary.animals[ 0 ].covered_by_talk is False
   assert itinerary.animals[ 0 ].start_time == ANIMAL_START

def Test_GetAnimalSpeciesNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalSpeciesNameProvider,
      'fetch_animal_species_names',
      lambda _conn: [ SPECIES ] )

   assert AnimalCoordinator.get_animal_species_names() == [ SPECIES ]

def Test_GetAnimalInformation_TestProviderAnimal_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalInformationProvider,
      'fetch_animal_information',
      lambda _conn, *, species, exhibit: ANIMAL if species == SPECIES and exhibit == EXHIBIT else None )

   assert AnimalCoordinator.get_animal_information( SPECIES, EXHIBIT ) is ANIMAL

def Test_GetAnimalViewingScopes_TestProviderScopes_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalViewingScopeProvider,
      'fetch_animal_viewing_scopes',
      lambda _conn, *, species, exhibit: (
         [ AnimalViewingScope.INDOOR, AnimalViewingScope.OUTDOOR ]
         if species == SPECIES and exhibit == EXHIBIT
         else [] ) )

   assert AnimalCoordinator.get_animal_viewing_scopes( SPECIES, EXHIBIT ) == [
      AnimalViewingScope.INDOOR,
      AnimalViewingScope.OUTDOOR,
   ]

def Test_GetAnimalsViewableOnDay_TestProvidersAndBuilder_ExpectAnimals(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal_records = [ { 'species': SPECIES } ]
   filtered_records = [ { 'species': SPECIES, 'filtered': True } ]
   captured: dict[ str, Any ] = {}

   class _Context:
      calendar_month = 6
      day_of_month = 15
      target_date = VISIT_DATE
      temp = 22.0
      sigma = 2

   monkeypatch.setattr(
      AnimalViewabilityContextBuilder,
      'resolve',
      lambda **_kwargs: _Context() )
   monkeypatch.setattr(
      AnimalViewableOnDayProvider,
      'fetch_animals_viewable_on_day_records',
      lambda _conn, month, day, *, exhibits_to_include: (
         animal_records
         if month == 6 and day == 15 and exhibits_to_include == [ EXHIBIT ]
         else [] ) )
   monkeypatch.setattr(
      ItineraryAnimalRecordsFilterBuilder,
      'filter',
      lambda records: filtered_records if records is animal_records else [] )

   def build_viewable_animals_on_day(
         records: list[ Any ],
         *,
         target_date: date,
         temp: float,
         sigma: int,
         include_off_display_animals: bool,
         threshold: int | None ) -> list[ Animal ]:
      captured[ 'records' ] = records
      captured[ 'target_date' ] = target_date
      captured[ 'temp' ] = temp
      captured[ 'sigma' ] = sigma
      captured[ 'include_off_display_animals' ] = include_off_display_animals
      captured[ 'threshold' ] = threshold
      return [ ANIMAL ]

   monkeypatch.setattr(
      AnimalViewabilityBuilder,
      'build_viewable_animals_on_day',
      build_viewable_animals_on_day )

   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      temp=22.0,
      include_off_display_animals=True,
      for_itinerary=True,
      threshold=5,
      exhibits_to_include=[ EXHIBIT ] )

   assert animals == [ ANIMAL ]
   assert captured[ 'records' ] is filtered_records
   assert captured[ 'target_date' ] == VISIT_DATE
   assert captured[ 'temp' ] == 22.0
   assert captured[ 'sigma' ] == 2
   assert captured[ 'include_off_display_animals' ] is True
   assert captured[ 'threshold' ] == 5

def Test_GetAnimalsMatchingQuery_TestBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animals = [ ANIMAL ]

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      lambda **_kwargs: animals )
   monkeypatch.setattr(
      AnimalsMatchingQueryBuilder,
      'build',
      lambda rows, query: rows if query == QUERY else [] )

   assert AnimalCoordinator.get_animals_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR ) == animals

def Test_SetAnimalAsOffDisplay_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   status = AnimalOffDisplayStatus(
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.INDOOR,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )
   captured: dict[ str, Any ] = {}

   monkeypatch.setattr(
      AnimalOffDisplayStatusBuilder,
      'build',
      lambda **_kwargs: status )

   def save_animal_off_display_status(
         _conn: Types.Connection,
         *,
         species: str,
         exhibit: str,
         viewing_scope: AnimalViewingScope,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      captured[ 'args' ] = (
         species,
         exhibit,
         viewing_scope,
         start_date,
         end_date,
         message )
      return True

   monkeypatch.setattr(
      AnimalStatusProvider,
      'save_animal_off_display_status',
      save_animal_off_display_status )

   assert AnimalCoordinator.set_animal_as_off_display(
      SPECIES,
      EXHIBIT,
      START_DATE,
      END_DATE,
      MESSAGE,
      viewing_scope=AnimalViewingScope.INDOOR ) is True
   assert captured[ 'args' ] == (
      SPECIES,
      EXHIBIT,
      AnimalViewingScope.INDOOR,
      START_DATE,
      END_DATE,
      MESSAGE )

def Test_SetAnimalAsOnDisplay_TestProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, Any ] = {}

   def save_animal_on_display_status(
         _conn: Types.Connection,
         *,
         species: str,
         exhibit: str,
         viewing_scope: AnimalViewingScope ) -> bool:
      captured[ 'args' ] = ( species, exhibit, viewing_scope )
      return True

   monkeypatch.setattr(
      AnimalStatusProvider,
      'save_animal_on_display_status',
      save_animal_on_display_status )

   assert AnimalCoordinator.set_animal_as_on_display(
      SPECIES,
      EXHIBIT,
      viewing_scope=AnimalViewingScope.OUTDOOR ) is True
   assert captured[ 'args' ] == ( SPECIES, EXHIBIT, AnimalViewingScope.OUTDOOR )

def Test_SetAnimalLimitedViewingSchedule_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   schedule = AnimalLimitedViewingSchedule(
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      daily_start_time=DAILY_START,
      daily_end_time=DAILY_END,
      message=MESSAGE )
   captured: dict[ str, Any ] = {}

   monkeypatch.setattr(
      AnimalLimitedViewingScheduleBuilder,
      'build',
      lambda **_kwargs: schedule )

   def save_animal_limited_viewing_schedule(
         _conn: Types.Connection,
         *,
         species: str,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         daily_start_time: str,
         daily_end_time: str,
         message: str ) -> bool:
      captured[ 'args' ] = (
         species,
         exhibit,
         start_date,
         end_date,
         daily_start_time,
         daily_end_time,
         message )
      return True

   monkeypatch.setattr(
      AnimalVisibilityScheduleProvider,
      'save_animal_limited_viewing_schedule',
      save_animal_limited_viewing_schedule )

   assert AnimalCoordinator.set_animal_limited_viewing_schedule(
      SPECIES,
      EXHIBIT,
      START_DATE,
      END_DATE,
      DAILY_START,
      DAILY_END,
      MESSAGE ) is True
   assert captured[ 'args' ] == (
      SPECIES,
      EXHIBIT,
      START_DATE,
      END_DATE,
      DAILY_START,
      DAILY_END,
      MESSAGE )

def Test_RemoveAnimalVisibilitySchedule_TestProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalVisibilityScheduleProvider,
      'delete_animal_visibility_schedule',
      lambda _conn, *, species, exhibit: species == SPECIES and exhibit == EXHIBIT )

   assert AnimalCoordinator.remove_animal_visibility_schedule( SPECIES, EXHIBIT ) is True

def Test_SetAnimalViewingAlert_TestBuilderAndProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   alert = AnimalViewingAlert(
      species=SPECIES,
      exhibit=EXHIBIT,
      start_date=START_DATE,
      end_date=END_DATE,
      message=MESSAGE )
   captured: dict[ str, Any ] = {}

   monkeypatch.setattr(
      AnimalViewingAlertBuilder,
      'build',
      lambda **_kwargs: alert )

   def save_animal_viewing_alert(
         _conn: Types.Connection,
         *,
         species: str,
         exhibit: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
         message: str ) -> bool:
      captured[ 'args' ] = (
         species,
         exhibit,
         alert_start_date,
         alert_end_date,
         message )
      return True

   monkeypatch.setattr(
      AnimalViewingAlertProvider,
      'save_animal_viewing_alert',
      save_animal_viewing_alert )

   assert AnimalCoordinator.set_animal_viewing_alert(
      SPECIES,
      EXHIBIT,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == (
      SPECIES,
      EXHIBIT,
      START_DATE,
      END_DATE,
      MESSAGE )

def Test_RemoveAnimalViewingAlert_TestProvider_ExpectDelegated(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AnimalViewingAlertProvider,
      'delete_animal_viewing_alert',
      lambda _conn, *, species, exhibit: species == SPECIES and exhibit == EXHIBIT )

   assert AnimalCoordinator.remove_animal_viewing_alert( SPECIES, EXHIBIT ) is True

def Test_GetAnimalsForSavedItinerary_TestEmptySavedAnimals_ExpectEmpty() -> None:
   assert AnimalCoordinator.get_animals_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_animals=[],
   ) == []

def Test_GetAnimalsForSavedItinerary_TestSavedAnimals_ExpectBuilderFilteredAnimals(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   viewable_animals = [
      _animal( 'African Penguin', 'Africa Savanna', enclosure_name='Outdoor' ),
      _animal( 'African Lion', 'Africa Savanna' ),
      _animal( 'Masai Giraffe', 'Africa Savanna' ),
   ]
   captured: dict[ str, object ] = {}

   def get_animals_viewable_on_day( **kwargs: object ) -> list[ Animal ]:
      captured[ 'kwargs' ] = kwargs
      return viewable_animals

   monkeypatch.setattr(
      AnimalCoordinator,
      'get_animals_viewable_on_day',
      get_animals_viewable_on_day )

   saved_animals = [
      ItineraryAnimalRecord(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         old_likelihood=None,
         new_likelihood=None ),
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=None ),
   ]

   animals = AnimalCoordinator.get_animals_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_animals=saved_animals,
   )

   assert captured[ 'kwargs' ] == {
      'day': VISIT_DAY,
      'month': VISIT_MONTH,
      'year': VISIT_YEAR,
      'temp': None,
      'include_off_display_animals': True,
      'threshold': 0,
      'exhibits_to_include': [ 'Africa Savanna' ],
   }
   assert [ animal.species for animal in animals ] == [ 'African Lion', 'African Penguin' ]
