from __future__ import annotations

from datetime import date

from ... import zoo
from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ...guardians.controllers.guardians_controller import GuardiansController
from ...types import Connection, DateInput, DateKey
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ..data_access.itinerary import fetch_itinerary_animal_rows
from ..data_access.itinerary import fetch_itinerary_attraction_rows
from ..data_access.itinerary_animal_input import ItineraryAnimalInput
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.validated_itinerary import ValidatedItinerary
from ...guardians.logic.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from ...wild_encounters.logic.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary


def validate_itinerary_animals(
      animal_controller: type[ AnimalController ],
      animals: tuple[ ItineraryAnimalInput, ... ],
      new_visit_date: date,
      new_visit_date_temp: float | None = None,
      old_visit_date: DateKey | None = None,
      saved_itinerary_animal_rows: list[ ItineraryAnimalRecord ] | None = None ) -> list[ zoo.AnimalDiff ]:
   old_likelihood_by_pair: dict[ tuple[ str, str ], int | None ] = {}

   if old_visit_date != None and saved_itinerary_animal_rows:
      for row in saved_itinerary_animal_rows:
         old_likelihood_by_pair[
            ( row.species, row.exhibit )
         ] = row.new_likelihood

   diffs: list[ zoo.AnimalDiff ] = []

   for animal in animals:
      species = animal.species
      exhibit = animal.exhibit

      old_likelihood = (
         None
         if old_visit_date == None
         else old_likelihood_by_pair.get( ( species, exhibit ) ) )

      saved_animals = animal_controller.get_animals_for_saved_itinerary(
         day=new_visit_date.day,
         month=new_visit_date.month,
         year=new_visit_date.year,
         temp=new_visit_date_temp,
         saved_animals=[
            ItineraryAnimalRecord(
               species=species,
               exhibit=exhibit,
               old_likelihood=None,
               new_likelihood=None ) ],
      )

      new_likelihood = (
         None
         if not saved_animals
         else saved_animals[ 0 ].likelihood )

      diffs.append(
         zoo.AnimalDiff(
            species=species,
            exhibit=exhibit,
            old_likelihood=old_likelihood,
            new_likelihood=new_likelihood,
         )
      )

   return diffs



def validate_itinerary_attractions(
      attraction_controller: type[ AttractionController ],
      attractions: tuple[ str, ... ],
      new_visit_date: date,
      old_visit_date: DateKey | None = None,
      saved_itinerary_attraction_rows: list[ ItineraryAttractionRecord ] | None = None ) -> list[ zoo.AttractionDiff ]:

   old_likelihood_by_name: dict[ str, int | None ] = {}

   if old_visit_date != None and saved_itinerary_attraction_rows:
      for row in saved_itinerary_attraction_rows:
         old_likelihood_by_name[ row.attraction ] = row.new_likelihood

   diffs: list[ zoo.AttractionDiff ] = []

   for attraction_name in attractions:

      old_likelihood = (
         None
         if old_visit_date == None
         else old_likelihood_by_name.get( attraction_name ) )

      new_likelihood = attraction_controller.get_attraction_likelihood_for_visit_date(
         visit_date=new_visit_date,
         attraction_name=attraction_name )

      diffs.append(
         zoo.AttractionDiff(
            name=attraction_name,
            old_likelihood=old_likelihood,
            new_likelihood=new_likelihood,
         )
      )

   return diffs



def validate_itinerary_for_save(
      conn: Connection,
      save_input: ItinerarySaveInput,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      *,
      new_visit_date_temp: float | None = None,
      old_visit_date: DateKey | None = None ) -> ValidatedItinerary:
   saved_itinerary_animal_rows: list[ ItineraryAnimalRecord ] = []
   saved_itinerary_attraction_rows: list[ ItineraryAttractionRecord ] = []

   if old_visit_date != None:
      saved_itinerary_animal_rows = fetch_itinerary_animal_rows( conn )
      saved_itinerary_attraction_rows = fetch_itinerary_attraction_rows( conn )

   return ValidatedItinerary(
      animals=(
         validate_itinerary_animals(
            animal_controller,
            animals=save_input.animals,
            new_visit_date=save_input.date,
            new_visit_date_temp=new_visit_date_temp,
            old_visit_date=old_visit_date,
            saved_itinerary_animal_rows=saved_itinerary_animal_rows )
         if save_input.animals
         else [] ),
      attractions=(
         validate_itinerary_attractions(
            attraction_controller,
            attractions=save_input.attractions,
            new_visit_date=save_input.date,
            old_visit_date=old_visit_date,
            saved_itinerary_attraction_rows=saved_itinerary_attraction_rows )
         if save_input.attractions
         else [] ),
      guardians_talks=validate_guardians_talks_for_itinerary(
         save_input.guardians_talks,
         guardians_controller.get_guardians_talk_schedule(
            month=save_input.month(),
            day=save_input.day(),
            year=save_input.year() ) ),
      wild_encounters=validate_wild_encounters_for_itinerary(
         save_input.wild_encounters,
         wild_encounter_controller.get_wild_encounter_schedule(
            month=save_input.month(),
            day=save_input.day(),
            year=save_input.year() ) ),
   )
