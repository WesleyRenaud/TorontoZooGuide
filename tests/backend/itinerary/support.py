from __future__ import annotations

from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
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
