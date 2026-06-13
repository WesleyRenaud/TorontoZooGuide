from __future__ import annotations

from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator

GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
CAROUSEL = 'Conservation Carousel'
LION_KEY = 'African Lion||Africa Savanna'
CHEETAH_KEY = 'Cheetah||Africa Savanna'
LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
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
