from __future__ import annotations

from dataclasses import dataclass
import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.operations.itinerary_item_schedule_change_committer import ItineraryItemScheduleChangeCommitter
from api.itinerary.operations.itinerary_item_unscheduler import ItineraryItemUnscheduler
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.bulk.guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.unscheduling.guest_schedule_shift_applier import GuestScheduleShiftApplier
from api.models import Animal, Attraction
from api.shared.enums import ItineraryErrorType

@dataclass
class _RestoredGuestScheduleState:
   replacement_end_seconds: int | None = None

CHEETAH_KEY = AnimalScheduleItemKey(
   species='Cheetah',
   exhibit='Africa Savanna',
)

KANGAROO_WALK_THRU_KEY = AttractionScheduleItemKey(
   name='Kangaroo Walk-Thru',
)

ZEBRA_TALK_KEY = GuardiansTalkScheduleItemKey(
   name="Grevy's Zebra",
   start_time='2:00 PM',
)

FULLY_SCHEDULED_ITINERARY = ItineraryBuilder.build(
   date='2026-06-15',
   selected_exhibits=[],
   animals=[
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:15 AM' ),
      Animal(
         species='Cheetah',
         exhibit='Africa Savanna',
         start_time='10:30 AM',
         end_time='10:45 AM' ),
   ],
   attractions=[],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time='9:50 AM',
   departure_time='11:00 AM' )

INCOMPLETE_ITINERARY = ItineraryBuilder.build(
   date='2026-06-15',
   selected_exhibits=[],
   animals=[
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:15 AM' ),
      Animal(
         species='Cheetah',
         exhibit='Africa Savanna' ),
   ],
   attractions=[],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time=None,
   departure_time=None )

COVERING_ATTRACTION_SCHEDULED_ITINERARY = ItineraryBuilder.build(
   date='2026-06-20',
   selected_exhibits=[],
   animals=[
      Animal(
         species='Western Grey Kangaroo',
         exhibit='Australasia Outdoor',
         start_time='11:00 AM',
         end_time='11:30 AM',
         covered_by_talk=True ),
   ],
   attractions=[
      Attraction(
         name='Kangaroo Walk-Thru',
         free_with_admission=0,
         start_time='11:00 AM',
         end_time='11:30 AM' ),
   ],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time='10:45 AM',
   departure_time='12:00 PM' )

COVERING_ATTRACTION_INCOMPLETE_ITINERARY = ItineraryBuilder.build(
   date='2026-06-20',
   selected_exhibits=[],
   animals=[
      Animal(
         species='Western Grey Kangaroo',
         exhibit='Australasia Outdoor',
         start_time='11:00 AM',
         end_time='11:05 AM' ),
   ],
   attractions=[
      Attraction(
         name='Kangaroo Walk-Thru',
         free_with_admission=0 ),
   ],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time=None,
   departure_time=None )


@pytest.fixture
def committer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Commit_TestUnscheduleMiddleAnimal_ExpectVisitTimesCleared(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:50 AM',
      departure_time='11:00 AM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:15 AM',
         ),
         ItineraryAnimalRecord(
            species='Cheetah',
            exhibit='Africa Savanna',
            start_time='10:30 AM',
            end_time='10:45 AM',
         ),
      ],
   )
   build_calls = [ FULLY_SCHEDULED_ITINERARY, INCOMPLETE_ITINERARY, INCOMPLETE_ITINERARY ]
   cleared: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: build_calls.pop( 0 ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.GuestScheduleShiftApplier.apply_for_unschedule',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      ItineraryItemUnscheduler,
      'apply',
      lambda cur, schedule_item_key: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ScheduledEndpointVisitTimesSyncer.sync_if_complete',
      lambda conn, itinerary: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda conn, *, previous_itinerary, current_itinerary: cleared.append( 'cleared' ) )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'persist_walk_route',
      lambda conn, **context: None )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ItineraryItemScheduleChangeCommitter.commit(
      committer_conn,
      CHEETAH_KEY,
      ItineraryItemUnscheduler.apply )

   assert result.status == ItineraryErrorType.SUCCESS
   assert cleared == [ 'cleared' ]


def Test_Commit_TestUnscheduleCoveringAttraction_ExpectVisitTimesCleared(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-20',
      arrival_time='10:45 AM',
      departure_time='12:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='Western Grey Kangaroo',
            exhibit='Australasia Outdoor',
            start_time='11:00 AM',
            end_time='11:30 AM',
            covered_by_talk=True,
         ),
      ],
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction='Kangaroo Walk-Thru',
            old_likelihood=None,
            new_likelihood=None,
            start_time='11:00 AM',
            end_time='11:30 AM',
         ),
      ],
   )
   build_calls = [
      COVERING_ATTRACTION_SCHEDULED_ITINERARY,
      COVERING_ATTRACTION_INCOMPLETE_ITINERARY,
      COVERING_ATTRACTION_INCOMPLETE_ITINERARY,
   ]
   cleared: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: build_calls.pop( 0 ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.AttractionAnimalCoverer.restore_after_removed',
      lambda *args, **kwargs: type(
         'Restored',
         (),
         { 'replacement_end_seconds': 11 * 3600 + 5 * 60, 'animals': [] },
      )() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.GuestScheduleShiftApplier.shift_items_after_unschedule',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      ItineraryItemUnscheduler,
      'apply',
      lambda cur, schedule_item_key: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ScheduledEndpointVisitTimesSyncer.sync_if_complete',
      lambda conn, itinerary: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda conn, *, previous_itinerary, current_itinerary: cleared.append( 'cleared' ) )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'persist_walk_route',
      lambda conn, **context: None )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ItineraryItemScheduleChangeCommitter.commit(
      committer_conn,
      KANGAROO_WALK_THRU_KEY,
      ItineraryItemUnscheduler.apply )

   assert result.status == ItineraryErrorType.SUCCESS
   assert cleared == [ 'cleared' ]


def Test_Commit_TestUnscheduleGuardiansTalk_ExpectCoveredAnimalsRestored(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[],
      animal_rows=[
         ItineraryAnimalRecord(
            species="Grevy's Zebra",
            exhibit='Africa Savanna',
            start_time='2:00 PM',
            end_time='2:30 PM',
            covered_by_talk=True,
         ),
      ],
   )
   removed_block = TimeBlock( start_seconds=14 * 3600, end_seconds=14 * 3600 + 30 * 60 )
   restored = _RestoredGuestScheduleState()

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: saved_itinerary )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      GuestScheduleShiftApplier,
      'resolve_unscheduled_item_time_block',
      lambda saved_itinerary, schedule_item_key: removed_block )
   monkeypatch.setattr(
      GuardiansTalkAnimalCoverer,
      'restore_after_removed',
      lambda cur, conn, *, talk_name, talk_block, animal_rows: restored )
   monkeypatch.setattr(
      GuestScheduleShiftApplier,
      'apply_for_unschedule',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      ItineraryItemUnscheduler,
      'apply',
      lambda cur, schedule_item_key: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ScheduledEndpointVisitTimesSyncer.sync_if_complete',
      lambda conn, itinerary: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_schedule_change_committer.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda conn, *, previous_itinerary, current_itinerary: None )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'persist_walk_route',
      lambda conn, **context: None )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ItineraryItemScheduleChangeCommitter.commit(
      committer_conn,
      ZEBRA_TALK_KEY,
      ItineraryItemUnscheduler.apply )

   assert result.status == ItineraryErrorType.SUCCESS
