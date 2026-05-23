from __future__ import annotations

from ...models import Animal
from ...models import Attraction
from ...models import GuardiansTalk
from ...models import Itinerary
from ...models import WildEncounter
from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ...guardians.controllers.guardians_controller import GuardiansController
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...types import DateInput
from ..data_access.saved_itinerary import SavedItinerary


def empty_itinerary() -> Itinerary:
   return Itinerary(
      date='',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[] )


def build_itinerary(
      date: DateInput,
      animals: list[ Animal ],
      attractions: list[ Attraction ],
      guardians_talks: list[ GuardiansTalk ],
      wild_encounters: list[ WildEncounter ] ) -> Itinerary:

   return Itinerary(
      date=date,
      animals=animals,
      attractions=attractions,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters )


def build_current_itinerary(
      saved_itinerary: SavedItinerary,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ] ) -> Itinerary:

   if saved_itinerary.is_empty():
      return empty_itinerary()

   day = saved_itinerary.day()
   month = saved_itinerary.month()
   year = saved_itinerary.year()

   animals = animal_controller.get_animals_for_saved_itinerary(
      day=day,
      month=month,
      year=year,
      saved_animals=list( saved_itinerary.animal_rows ) )

   attractions = attraction_controller.get_attractions_for_saved_itinerary(
      day=day,
      month=month,
      year=year,
      saved_attractions=list( saved_itinerary.attraction_rows ) )

   guardians_talks = guardians_controller.get_guardians_talks_for_saved_itinerary(
      list( saved_itinerary.guardians_talk_rows ) )

   wild_encounters = wild_encounter_controller.get_wild_encounters_for_saved_itinerary(
      list( saved_itinerary.wild_encounter_rows ) )

   return build_itinerary(
      date=saved_itinerary.date_value,
      animals=animals,
      attractions=attractions,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters )
