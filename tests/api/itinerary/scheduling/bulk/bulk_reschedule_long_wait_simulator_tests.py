from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.bulk.bulk_reschedule_long_wait_simulator import BulkRescheduleLongWaitSimulator
from api.models import Animal
from api.models import GuardiansTalk
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


VISIT_DATE = date( 2026, 6, 15 )

ITINERARY_CONTEXT = {
   'animal_coordinator': AnimalCoordinator,
   'attraction_coordinator': AttractionCoordinator,
   'guardians_coordinator': GuardiansCoordinator,
   'wild_encounter_coordinator': WildEncounterCoordinator,
   'visit_date_temp': None,
}

ISOLATED_TALK = GuardiansTalk(
   name='Slender-Tailed Meerkat',
   location='African Rainforest Pavilion',
   x_coord=0.0,
   y_coord=0.0,
   start_time='1:00 PM',
   end_time='1:30 PM',
)

SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='10:00 AM',
         end_time='10:08 AM',
      ),
   ],
)


@pytest.fixture
def long_wait_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


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
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
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
      lambda saved_itinerary, *, only_previously_scheduled: [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM',
         ),
      ] )

   assert BulkRescheduleLongWaitSimulator.is_isolated_after_adding(
      long_wait_conn,
      ISOLATED_TALK,
      propose_on_itinerary=lambda itinerary, new_item, context: None,
      itinerary_context=ITINERARY_CONTEXT ) is True


def Test_NewlyAddedReason_TestNoIsolatedNewItems_ExpectNone(
      long_wait_conn: sqlite3.Connection ) -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
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
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ) ) is None


def Test_NewlyAddedReason_TestIsolatedNewTalk_ExpectLongWaitReason(
      long_wait_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name='Slender-Tailed Meerkat',
            is_deleted=False,
            start_time='1:00 PM',
            end_time='1:30 PM',
            location='African Rainforest Pavilion' ),
      ],
      wild_encounters=[],
      events=[],
   )
   packed_itinerary = ItineraryBuilder.empty()
   packed_itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]

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
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ) )

   assert reason is not None
   assert reason.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in reason.items ] == [ 'Slender-Tailed Meerkat' ]
