from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.guardians.controllers.guardians_controller import GuardiansController
from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_error_suppression import suppress_itinerary_error
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueType
from conftest import DbControllers

ANIMAL_KEY = 'African Lion||Africa Savanna'
GUARDIANS_TALK = 'African Lion'
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


def _set_guardians_talk_schedule(
      *,
      monday_time: str = '10:00',
) -> None:
   assert GuardiansController.set_guardians_talk_schedule(
      talk=GUARDIANS_TALK,
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time=monday_time,
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=None,
   )


def _set_itinerary_with_scheduled_animal(
      db: DbControllers,
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
      start_time='10:00',
   ).success


def test_set_itinerary_returns_warning_when_guardians_talk_would_unschedule_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[],
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
   assert animal.start_time == '10:00'
   assert animal.end_time == '10:08'
   assert not saved.guardians_talk_names()


def test_set_itinerary_unschedules_overlapping_items_when_confirmed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[],
      confirming_guardians_talk_unschedule=True,
   )

   assert result.success
   assert len( result.itinerary.guardians_talks ) == 1
   assert result.itinerary.guardians_talks[ 0 ].start_time == '10:00'
   assert result.itinerary.guardians_talks[ 0 ].end_time == '10:30'

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.start_time is None
   assert lion.end_time is None


def test_schedule_guardians_talk_returns_warning_when_it_would_unschedule_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryController.schedule_itinerary_item(
      item_type='guardians_talks',
      key=GUARDIANS_TALK,
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
   assert animal.start_time == '10:00'
   assert not saved.guardians_talk_names()


def test_schedule_guardians_talk_unschedules_overlapping_items_when_confirmed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryController.schedule_itinerary_item(
      item_type='guardians_talks',
      key=GUARDIANS_TALK,
      confirming_guardians_talk_unschedule=True,
   )

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.start_time is None
   assert lion.end_time is None

   talk = next(
      saved_talk for saved_talk in result.itinerary.guardians_talks
      if saved_talk.name == GUARDIANS_TALK )
   assert talk.start_time == '10:00'
   assert talk.end_time == '10:30'


def test_guardians_talk_unschedule_warning_cannot_be_suppressed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   suppress_itinerary_error(
      db.conn,
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )

   result = ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK ) ],
      wild_encounters=[],
   )

   assert not result.success
   assert result.error_type == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert len( result.issues ) == 1
   assert (
      result.issues[ 0 ].issue_type
      == ItinerarySaveIssueType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.issues[ 0 ].items ] == [ GUARDIANS_TALK ]
