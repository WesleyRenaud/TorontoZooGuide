from __future__ import annotations

from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from .itinerary_save_input import ItinerarySaveInput
from .itinerary_transportation_input import ItineraryTransportationInput
from ...shared.calendar_dates import DateValues
from ...shared.value_conversion import ValueConversion
from ...types import Types
from ..wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


class ItinerarySaveInputMapper():
   @classmethod
   def map_named_strings( cls, names: list[ str ] | None ) -> list[ str ]:
      mapped: list[ str ] = []

      for name in names or []:
         normalized = ValueConversion.as_trimmed_string( name )

         if normalized:
            mapped.append( normalized )

      return mapped


   @classmethod
   def map_guardians_talk_inputs(
         cls,
         guardians_talks: list[ dict[ str, str | None ] ] | None ) -> list[ ItineraryGuardiansTalkInput ]:
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


   @classmethod
   def map_animal_inputs(
         cls,
         animals: list[ dict[ str, str | None ] ] | None ) -> list[ ItineraryAnimalInput ]:
      mapped: list[ ItineraryAnimalInput ] = []

      for animal in animals or []:
         mapped.append(
            ItineraryAnimalInput(
               species=str( animal[ 'species' ] ),
               exhibit=str( animal[ 'exhibit' ] ),
               enclosure_name=ValueConversion.as_nullable_string(
                  animal.get( 'enclosure_name' ) ),
            )
         )

      return mapped


   @classmethod
   def map_itinerary_save_input(
         cls,
         date: Types.DateInput,
         arrival_time: Types.TimeInput,
         departure_time: Types.TimeInput,
         selected_exhibits: list[ str ] | None = None,
         animals: list[ dict[ str, str | None ] ] | None = None,
         attractions: list[ str ] | None = None,
         guardians_talks: list[ dict[ str, str | None ] ] | None = None,
         wild_encounters: list[ WildEncounterScheduleItemKey ] | None = None,
         transportations: list[ ItineraryTransportationInput ] | None = None,
   ) -> ItinerarySaveInput:

      return ItinerarySaveInput(
         date=DateValues.parse_date_value( date ),
         arrival_time=DateValues.normalize_itinerary_schedule_time( arrival_time ),
         departure_time=DateValues.normalize_itinerary_schedule_time( departure_time ),
         selected_exhibits=cls.map_named_strings( selected_exhibits ),
         animals=cls.map_animal_inputs( animals ),
         attractions=cls.map_named_strings( attractions ),
         transportations=list( transportations or [] ),
         guardians_talks=cls.map_guardians_talk_inputs( guardians_talks ),
         wild_encounters=list( wild_encounters or [] ) )
