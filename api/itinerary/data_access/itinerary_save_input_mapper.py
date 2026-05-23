from __future__ import annotations

from collections.abc import Iterable

from ...zoo_util import ZooUtil
from ...types import DateInput
from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_save_input import ItinerarySaveInput


def map_named_strings( names: Iterable[ str ] | None ) -> tuple[ str, ... ]:
   return tuple(
      name.strip()
      for name in names or []
      if str( name ).strip()
   )



def map_animal_inputs( animals: Iterable[ dict[ str, str ] ] | None ) -> tuple[ ItineraryAnimalInput, ... ]:
   return tuple(
      ItineraryAnimalInput(
         species=animal[ 'species' ],
         exhibit=animal[ 'exhibit' ] )
      for animal in animals or []
   )



def map_itinerary_save_input(
      date: DateInput,
      animals: Iterable[ dict[ str, str ] ] | None,
      attractions: Iterable[ str ] | None,
      guardians_talks: Iterable[ str ] | None,
      wild_encounters: Iterable[ str ] | None ) -> ItinerarySaveInput:

   return ItinerarySaveInput(
      date=ZooUtil.parse_date_value( date ),
      animals=map_animal_inputs( animals ),
      attractions=map_named_strings( attractions ),
      guardians_talks=map_named_strings( guardians_talks ),
      wild_encounters=map_named_strings( wild_encounters ) )
