from __future__ import annotations

from collections.abc import Iterable

from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from .itinerary_save_input import ItinerarySaveInput
from ...shared.calendar_dates import DateValues
from ...shared.enums.enclosure_type import EnclosureType
from ...shared.value_conversion import ValueConversion
from ...types import DateInput, TimeInput
from ..wild_encounter_item_key import WildEncounterScheduleItemKey


def map_named_strings( names: Iterable[ str ] | None ) -> list[ str ]:
   mapped: list[ str ] = []

   for name in names or []:
      normalized = ValueConversion.as_trimmed_string( name )

      if normalized:
         mapped.append( normalized )

   return mapped


def map_guardians_talk_inputs(
      guardians_talks: Iterable[ dict[ str, str | None ] ] | None ) -> list[ ItineraryGuardiansTalkInput ]:
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

   return mapped


def map_animal_inputs(
      animals: Iterable[ dict[ str, str | None ] ] | None ) -> list[ ItineraryAnimalInput ]:
   mapped: list[ ItineraryAnimalInput ] = []

   for animal in animals or []:
      mapped.append(
         ItineraryAnimalInput(
            species=str( animal[ 'species' ] ),
            exhibit=str( animal[ 'exhibit' ] ),
            enclosure_name=EnclosureType.normalize_viewing_spot_name(
               animal.get( 'enclosure_name' ) ),
         )
      )

   return mapped


def map_itinerary_save_input(
      date: DateInput,
      arrival_time: TimeInput,
      departure_time: TimeInput,
      animals: Iterable[ dict[ str, str | None ] ] | None,
      attractions: Iterable[ str ] | None,
      guardians_talks: Iterable[ dict[ str, str | None ] ] | None,
      wild_encounters: Iterable[ WildEncounterScheduleItemKey ] | None,
      selected_exhibits: Iterable[ str ] | None = None ) -> ItinerarySaveInput:

   return ItinerarySaveInput(
      date=DateValues.parse_date_value( date ),
      arrival_time=DateValues.normalize_itinerary_schedule_time( arrival_time ),
      departure_time=DateValues.normalize_itinerary_schedule_time( departure_time ),
      animals=map_animal_inputs( animals ),
      attractions=map_named_strings( attractions ),
      guardians_talks=map_guardians_talk_inputs( guardians_talks ),
      wild_encounters=list( wild_encounters or [] ),
      selected_exhibits=map_named_strings( selected_exhibits ) )
