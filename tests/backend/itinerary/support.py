from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
TURTLE_TALK = 'Nile Soft-Shelled Turtle'
RHINO_ENCOUNTER = 'Guardians of White Rhinos'
CAROUSEL = 'Conservation Carousel'
LION_KEY = 'African Lion||Africa Savanna'
ANIMAL_KEY = LION_KEY
PENGUIN_KEY = 'African Penguin||Africa Savanna'
CHEETAH_KEY = 'Cheetah||Africa Savanna'
LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}
PENGUIN_ITINERARY_ENTRY = {
   'species': 'African Penguin',
   'exhibit': 'Africa Savanna',
}
CHEETAH_ITINERARY_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Africa Savanna',
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


def guardians_talk_save_entries( *names: str ) -> list[ dict[ str, str | None ] ]:
   return [
      guardians_talk_save_entry( name )
      for name in names
   ]


def set_wild_encounter_schedule( *, encounter_time: str ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time=encounter_time,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
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

   assert ItineraryCoordinator.schedule_itinerary_item(
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

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='guardians_talks',
      key=TURTLE_TALK,
   ).success

   assert ItineraryCoordinator.schedule_itinerary_item(
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
