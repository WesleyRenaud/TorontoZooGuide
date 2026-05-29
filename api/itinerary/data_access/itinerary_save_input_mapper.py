from __future__ import annotations

from collections.abc import Iterable

from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from .itinerary_save_input import ItinerarySaveInput
from ...shared.date_values import DateValues
from ...types import DateInput, TimeInput


def map_named_strings( names: Iterable[ str ] | None ) -> tuple[ str, ... ]:
   return tuple(
      name.strip()
      for name in names or []
      if str( name ).strip()
   )


def map_guardians_talk_inputs(
      guardians_talks: Iterable[ dict[ str, str | None ] ] | None,
) -> tuple[ ItineraryGuardiansTalkInput, ... ]:
   mapped: list[ ItineraryGuardiansTalkInput ] = []

   for item in guardians_talks or []:
      mapped.append(
         ItineraryGuardiansTalkInput(
            name=item[ 'name' ],
            start_time=DateValues.normalize_itinerary_schedule_time(
               item[ 'start_time' ] ),
            end_time=DateValues.normalize_itinerary_schedule_time(
               item[ 'end_time' ] ),
         )
      )

   return tuple( mapped )


def map_animal_inputs( animals: Iterable[ dict[ str, str ] ] | None ) -> tuple[ ItineraryAnimalInput, ... ]:
   return tuple(
      ItineraryAnimalInput(
         species=animal[ 'species' ],
         exhibit=animal[ 'exhibit' ] )
      for animal in animals or []
   )


def map_itinerary_save_input(
      date: DateInput,
      arrival_time: TimeInput,
      departure_time: TimeInput,
      animals: Iterable[ dict[ str, str ] ] | None,
      attractions: Iterable[ str ] | None,
      guardians_talks: Iterable[ dict[ str, str | None ] ] | None,
      wild_encounters: Iterable[ str ] | None,
      selected_exhibits: Iterable[ str ] | None = None ) -> ItinerarySaveInput:

   return ItinerarySaveInput(
      date=DateValues.parse_date_value( date ),
      arrival_time=DateValues.normalize_itinerary_schedule_time( arrival_time ),
      departure_time=DateValues.normalize_itinerary_schedule_time( departure_time ),
      animals=map_animal_inputs( animals ),
      attractions=map_named_strings( attractions ),
      guardians_talks=map_guardians_talk_inputs( guardians_talks ),
      wild_encounters=map_named_strings( wild_encounters ),
      selected_exhibits=map_named_strings( selected_exhibits ) )
