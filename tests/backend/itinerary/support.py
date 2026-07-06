from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.map_schedule_item_key_from_wire import map_schedule_item_key_from_wire
from api.itinerary.scheduling.items.schedule_item_key import ScheduleItemKey
from api.itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
WILD_ENCOUNTER_TIME = '14:00'
TURTLE_TALK = 'Nile Soft-Shelled Turtle'
RHINO_ENCOUNTER = 'Guardians of White Rhinos'
RHINO_ENCOUNTER_TIME = '14:00'
CAROUSEL = 'Conservation Carousel'
LION_KEY = 'African Lion||Africa Savanna'
ANIMAL_KEY = LION_KEY
PENGUIN_KEY = 'African Penguin||Africa Savanna||Outdoor'
CHEETAH_KEY = 'Cheetah||Africa Savanna'
LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}
PENGUIN_ITINERARY_ENTRY = {
   'species': 'African Penguin',
   'exhibit': 'Africa Savanna',
   'enclosure_name': 'Outdoor',
}
CHEETAH_ITINERARY_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Africa Savanna',
}
CHEETAH_INDO_MALAYA_ITINERARY_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Indo-Malaya Outdoor',
}


def guardians_talk_save_entry(
      name: str,
      *,
      start_time: str | None = None,
      end_time: str | None = None ) -> dict[ str, str | None ]:
   return {
      'name': name,
      'start_time': start_time,
      'end_time': end_time,
   }


def wild_encounter_save_entry(
      name: str,
      *,
      start_time: str,
      end_time: str | None = None ) -> str:
   return WildEncounterScheduleItemKey(
      name=name,
      start_time=start_time,
      end_time=end_time ).to_wire()


def guardians_talk_save_entries( *names: str ) -> list[ dict[ str, str | None ] ]:
   return [
      guardians_talk_save_entry( name )
      for name in names
   ]


def wild_encounter_save_entries(
      name: str,
      *,
      start_time: str,
      end_time: str | None = None ) -> list[ str ]:
   return [
      wild_encounter_save_entry( name, start_time=start_time, end_time=end_time )
   ]


def wild_encounter_keys(
      *names: str,
      start_time: str = WILD_ENCOUNTER_TIME,
      end_time: str | None = None ) -> list[ WildEncounterScheduleItemKey ]:
   return [
      wild_encounter_key( name, start_time=start_time, end_time=end_time )
      for name in names
   ]


def wild_encounter_key(
      name: str,
      *,
      start_time: str = WILD_ENCOUNTER_TIME,
      end_time: str | None = None ) -> WildEncounterScheduleItemKey:
   return WildEncounterScheduleItemKey(
      name=name,
      start_time=start_time,
      end_time=end_time )


def wild_encounter_wire(
      name: str,
      *,
      start_time: str = WILD_ENCOUNTER_TIME,
      end_time: str | None = None ) -> str:
   return wild_encounter_key(
      name,
      start_time=start_time,
      end_time=end_time ).to_wire()


def parsed_schedule_item(
      item_type: str,
      wire_key: str ) -> ScheduleItemKey | None:
   return map_schedule_item_key_from_wire( item_type, wire_key )


def schedule_itinerary_item(
      item_type: str,
      wire_key: str | None = None,
      *,
      key: str | None = None,
      **kwargs: object ) -> ItinerarySaveResult:
   return ItineraryCoordinator.schedule_itinerary_item(
      parsed_schedule_item(
         item_type,
         _resolved_wire_key( wire_key, key ) ),
      **kwargs )


def _resolved_wire_key(
      wire_key: str | None,
      key: str | None ) -> str:
   resolved_key = wire_key if wire_key is not None else key

   if resolved_key is None:
      raise TypeError( 'wire_key or key is required' )

   return resolved_key


def unschedule_itinerary_item(
      item_type: str,
      wire_key: str | None = None,
      *,
      key: str | None = None ) -> ItinerarySaveResult:
   return ItineraryCoordinator.unschedule_itinerary_item(
      parsed_schedule_item(
         item_type,
         _resolved_wire_key( wire_key, key ) ) )


def remove_itinerary_item(
      item_type: str,
      wire_key: str | None = None,
      *,
      key: str | None = None ) -> ItinerarySaveResult:
   return ItineraryCoordinator.remove_itinerary_item(
      parsed_schedule_item(
         item_type,
         _resolved_wire_key( wire_key, key ) ) )


def set_wild_encounter_schedule( *, encounter_time: str ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( encounter_time ),
      message=None,
   )


def set_guardians_talk_and_wild_encounter_schedules_at_1400() -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
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
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00' ),
      message=None,
   )


def set_itinerary_with_lion_scheduled_at_1400(
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
      start_time='14:00',
   ).success


def set_turtle_talk_and_rhino_encounter_schedules_at_1400() -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=TURTLE_TALK,
      location='African Rainforest Pavilion',
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
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=RHINO_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00' ),
      message=None,
   )


def set_itinerary_with_turtle_talk_and_lion_at_1430(
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
      item_type='guardians_talks',
      key=TURTLE_TALK,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='14:30',
      duration_minutes=15,
   ).success


def saved_animal_row(
      db: DbControllers,
      *,
      species: str,
      exhibit: str ) -> ItineraryAnimalRecord:
   saved_itinerary = fetch_saved_itinerary( db.conn )

   for row in saved_itinerary.animal_rows:
      if row.species == species and row.exhibit == exhibit:
         return row

   raise AssertionError(
      f'Expected saved animal row for { species } / { exhibit }' )
