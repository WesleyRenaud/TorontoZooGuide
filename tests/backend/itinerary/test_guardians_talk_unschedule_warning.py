from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import entrance_travel_seconds_to_animal, schedule_itinerary_item, schedule_time_after_seconds
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.fetch_itinerary_walk_route import fetch_itinerary_walk_route
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_status import suppress_itinerary_status
from api.itinerary.data_access.itinerary_walk_route_helpers import walk_route_matches
from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
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
      start_time: str = '10:00',
      end_time: str | None = None ) -> dict[ str, str | None ]:
   return {
      'name': name,
      'start_time': start_time,
      'end_time': end_time,
   }


def _set_guardians_talk_schedule(
      *,
      monday_time: str = '10:00' ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=GUARDIANS_TALK,
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( monday_time, monday=True, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=False, sunday=False ),
      message=None,
   )


def _set_itinerary_with_scheduled_animal(
      db: DbControllers,
      *,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success


def test_set_itinerary_returns_warning_when_guardians_talk_would_unschedule_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK, start_time='10:00' ) ],
      wild_encounters=[],
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
   assert animal.start_time == '10:00 AM'
   assert animal.end_time == '10:08 AM'
   assert not saved.guardians_talk_names()


def test_set_itinerary_keeps_talk_before_arrival_and_warns_about_overlap(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=GUARDIANS_TALK,
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         '11:00',
         monday=True,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False ),
      message=None,
   )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='11:00',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='11:21',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         _guardians_talk_save_entry( GUARDIANS_TALK, start_time='11:00' ),
      ],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ GUARDIANS_TALK ]

   confirmed = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='11:21',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         _guardians_talk_save_entry( GUARDIANS_TALK, start_time='11:00' ),
      ],
      wild_encounters=[],
      confirming_guardians_talk_unschedule=True,
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   )

   assert confirmed.success
   assert any(
      talk.name == GUARDIANS_TALK and not talk.is_deleted
      for talk in confirmed.itinerary.guardians_talks
   )
   assert DateValues.time_value_in_seconds( confirmed.itinerary.arrival_time ) <= (
      DateValues.time_value_in_seconds( '11:00 AM' )
   )


def test_set_itinerary_unschedules_overlapping_items_when_confirmed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK, start_time='10:00' ) ],
      wild_encounters=[],
      confirming_guardians_talk_unschedule=True,
   )

   assert result.success
   assert len( result.itinerary.guardians_talks ) == 1
   assert result.itinerary.guardians_talks[ 0 ].start_time == '10:00 AM'
   assert result.itinerary.guardians_talks[ 0 ].end_time == '10:30 AM'

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.covered_by_talk is True
   assert lion.start_time == '10:00 AM'
   assert lion.end_time == '10:30 AM'


def test_schedule_guardians_talk_returns_warning_when_it_would_unschedule_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = schedule_itinerary_item(
      item_type='guardians_talks',
      key=f'{ GUARDIANS_TALK }||10:00',
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
   assert animal.start_time == '10:00 AM'
   assert not saved.guardians_talk_names()


def test_schedule_guardians_talk_unschedules_overlapping_items_when_confirmed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = schedule_itinerary_item(
      item_type='guardians_talks',
      key=f'{ GUARDIANS_TALK }||10:00',
      confirming_guardians_talk_unschedule=True,
   )

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.covered_by_talk is True
   assert lion.start_time == '10:00 AM'
   assert lion.end_time == '10:30 AM'

   talk = next(
      saved_talk for saved_talk in result.itinerary.guardians_talks
      if saved_talk.name == GUARDIANS_TALK )
   assert talk.start_time == '10:00 AM'
   assert talk.end_time == '10:30 AM'


def test_confirmed_guardians_talk_reschedule_persists_walk_route(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   result = schedule_itinerary_item(
      item_type='guardians_talks',
      key=f'{ GUARDIANS_TALK }||10:00',
      confirming_guardians_talk_unschedule=True,
   )

   assert result.success

   expected_route = build_itinerary_walk_route( result.itinerary )
   persisted_route = fetch_itinerary_walk_route( db.conn )

   assert walk_route_matches( expected_route, persisted_route )
   assert any(
      stop.item_key == GUARDIANS_TALK
      for stop in persisted_route.stops )


def test_guardians_talk_unschedule_warning_cannot_be_suppressed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   _set_guardians_talk_schedule()
   _set_itinerary_with_scheduled_animal(
      db,
      freeze_database_today=freeze_database_today )

   suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ _guardians_talk_save_entry( GUARDIANS_TALK, start_time='10:00' ) ],
      wild_encounters=[],
   )

   assert not result.success
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert len( result.reasons ) == 1
   assert (
      result.reasons[ 0 ].code
      == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )
   assert [ item.name for item in result.reasons[ 0 ].items ] == [ GUARDIANS_TALK ]
