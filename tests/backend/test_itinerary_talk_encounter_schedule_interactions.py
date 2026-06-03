from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.guardians.controllers.guardians_controller import GuardiansController
from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueType
from api.wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from conftest import DbControllers


ANIMAL_KEY = 'African Lion||Africa Savanna'
GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}


def _guardians_talk_save_entry(
      name: str,
      *,
      start_time: str | None = None,
      end_time: str | None = None,
) -> dict[ str, str | None ]:
   return {
      'name': name,
      'start_time': start_time,
      'end_time': end_time,
   }


def _set_schedules_at_1400() -> None:
   assert GuardiansController.set_guardians_talk_schedule(
      talk=GUARDIANS_TALK,
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='14:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None,
   )
   assert WildEncounterController.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='14:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None,
   )


def _set_itinerary_with_animal_scheduled_at_1400(
      *,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='14:00',
   ).success


def test_set_itinerary_blocks_talk_and_encounter_conflict_before_unschedule_warnings(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_schedules_at_1400()
   _set_itinerary_with_animal_scheduled_at_1400(
      freeze_database_today=freeze_database_today )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[ WILD_ENCOUNTER ],
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.issues ) == 1
   assert (
      result.issues[ 0 ].issue_type
      == ItinerarySaveIssueType.WILD_ENCOUNTER_TIME_CONFLICT )
   assert { item.name for item in result.issues[ 0 ].items } == {
      GUARDIANS_TALK,
      WILD_ENCOUNTER,
   }

   saved = fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '14:00'
   assert animal.end_time == '14:08'
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()


def test_set_itinerary_returns_guardians_unschedule_after_talk_encounter_conflict_resolved(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_schedules_at_1400()
   _set_itinerary_with_animal_scheduled_at_1400(
      freeze_database_today=freeze_database_today )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[],
      overriding_conflicting_guardians_talks=True,
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert len( result.issues ) == 1
   assert (
      result.issues[ 0 ].issue_type
      == ItinerarySaveIssueType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.issues[ 0 ].items ] == [ GUARDIANS_TALK ]

   saved = fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '14:00'
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()


def test_set_itinerary_returns_wild_encounter_warning_after_talk_encounter_conflict_resolved(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_schedules_at_1400()
   _set_itinerary_with_animal_scheduled_at_1400(
      freeze_database_today=freeze_database_today )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ WILD_ENCOUNTER ],
      overriding_conflicting_guardians_talks=True,
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
   assert len( result.issues ) == 1
   assert (
      result.issues[ 0 ].issue_type
      == ItinerarySaveIssueType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.issues[ 0 ].items ] == [ WILD_ENCOUNTER ]

   saved = fetch_saved_itinerary( db.conn )
   animal = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )
   assert animal.start_time == '14:00'
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()


def test_set_itinerary_saves_talk_after_conflict_and_unschedule_confirmations(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_schedules_at_1400()
   _set_itinerary_with_animal_scheduled_at_1400(
      freeze_database_today=freeze_database_today )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[],
      overriding_conflicting_guardians_talks=True,
      confirming_guardians_talk_unschedule=True,
   )

   assert result.success
   assert result.error_type == ItineraryErrorType.SUCCESS
   assert result.issues == ()

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


def test_set_itinerary_blocks_talk_encounter_conflict_when_no_other_items_overlap(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_schedules_at_1400()
   freeze_database_today( date( 2026, 6, 15 ) )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[ WILD_ENCOUNTER ],
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.issues ) == 1
   assert (
      result.issues[ 0 ].issue_type
      == ItinerarySaveIssueType.WILD_ENCOUNTER_TIME_CONFLICT )
   assert { item.name for item in result.issues[ 0 ].items } == {
      GUARDIANS_TALK,
      WILD_ENCOUNTER,
   }

   saved = fetch_saved_itinerary( db.conn )
   assert not saved.guardians_talk_names()
   assert not saved.wild_encounter_names()
