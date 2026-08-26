from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import GUARDIANS_TALK, guardians_talk_save_entry, LION_ITINERARY_ENTRY, set_guardians_talk_and_wild_encounter_schedules_at_1400, set_itinerary_with_lion_scheduled_at_1400, WILD_ENCOUNTER, wild_encounter_key, wild_encounter_key

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_set_itinerary_blocks_talk_and_encounter_conflict_before_unschedule_warnings(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   set_guardians_talk_and_wild_encounter_schedules_at_1400()
   set_itinerary_with_lion_scheduled_at_1400(
      freeze_database_today=freeze_database_today )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( GUARDIANS_TALK, start_time='14:00' ) ],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER ) ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT )
   assert { item.name for item in result.reasons[ 0 ].items } == {
      GUARDIANS_TALK,
      WILD_ENCOUNTER,
   }

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '2:00 PM'
   assert animal.end_time == '2:08 PM'
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()


def test_set_itinerary_blocks_talk_encounter_conflict_when_no_other_items_overlap(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   set_guardians_talk_and_wild_encounter_schedules_at_1400()
   freeze_database_today( date( 2026, 6, 15 ) )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( GUARDIANS_TALK, start_time='14:00' ) ],
      wild_encounters=[ wild_encounter_key( WILD_ENCOUNTER ) ],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT )
   assert { item.name for item in result.reasons[ 0 ].items } == {
      GUARDIANS_TALK,
      WILD_ENCOUNTER,
   }

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()
