from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import GUARDIANS_TALK, guardians_talk_save_entry, LION_ITINERARY_ENTRY, set_guardians_talk_and_wild_encounter_schedules_at_1400, set_itinerary_with_lion_scheduled_at_1400, WILD_ENCOUNTER

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_set_itinerary_returns_guardians_unschedule_after_talk_encounter_conflict_resolved(
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
      guardians_talks=[ guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[],
      overriding_conflicting_guardians_talks=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ GUARDIANS_TALK ]

   saved = fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '14:00'
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()


def test_set_itinerary_returns_wild_encounter_warning_after_talk_encounter_conflict_resolved(
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
      guardians_talks=[],
      wild_encounters=[ WILD_ENCOUNTER ],
      overriding_conflicting_guardians_talks=True,
   )

   assert not result.success
   assert result.status == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ WILD_ENCOUNTER ]

   saved = fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '14:00'
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()


def test_set_itinerary_saves_talk_after_conflict_and_unschedule_confirmations(
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
      guardians_talks=[ guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[],
      overriding_conflicting_guardians_talks=True,
      confirming_guardians_talk_unschedule=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == ()

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.start_time is None
   assert lion.end_time is None
   assert [ talk.name for talk in result.itinerary.guardians_talks ] == [ GUARDIANS_TALK ]
   assert not result.itinerary.wild_encounters

   saved = fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time is None
   assert animal.end_time is None
   assert saved.guardians_talk_names() == [ GUARDIANS_TALK ]
   assert not saved.wild_encounter_names()
