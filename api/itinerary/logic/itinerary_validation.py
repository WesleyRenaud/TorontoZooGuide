from __future__ import annotations

from datetime import date

from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ..data_access.itinerary import fetch_itinerary_animal_rows
from ..data_access.itinerary import fetch_itinerary_attraction_rows
from ..data_access.itinerary import fetch_itinerary_event_rows
from ..data_access.itinerary import fetch_itinerary_wild_encounter_rows
from ..data_access.itinerary_animal_input import ItineraryAnimalInput
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_animal_save_carryover import itinerary_animal_save_carryover
from ..data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..data_access.itinerary_attraction_save_carryover import itinerary_attraction_save_carryover
from ..data_access.itinerary_event_record import ItineraryEventRecord
from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ..data_access.validated_itinerary import ValidatedItinerary
from ...guardians.controllers.guardians_controller import GuardiansController
from ...guardians.logic.guardians_talk_itinerary_validation import validate_guardians_talks_for_itinerary
from ...models import Animal
from ...models import AnimalDiff
from ...models import Attraction
from ...models import AttractionDiff
from ...models.itinerary_event import ItineraryEvent
from ...types import Connection, DateInput, DateKey
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...wild_encounters.logic.wild_encounter_itinerary_validation import validate_wild_encounters_for_itinerary


def validate_itinerary_animals(
      animal_controller: type[ AnimalController ],
      animals: tuple[ ItineraryAnimalInput, ... ],
      new_visit_date: date,
      new_visit_date_temp: float | None = None,
      old_visit_date: DateKey | None = None,
      saved_itinerary_animal_rows: list[ ItineraryAnimalRecord ] | None = None ) -> list[ AnimalDiff ]:
   diffs: list[ AnimalDiff ] = []

   for animal in animals:
      carryover = itinerary_animal_save_carryover(
         saved_itinerary_animal_rows,
         animal,
         old_visit_date=old_visit_date )

      saved_animals = animal_controller.get_animals_for_saved_itinerary(
         day=new_visit_date.day,
         month=new_visit_date.month,
         year=new_visit_date.year,
         temp=new_visit_date_temp,
         saved_animals=[
            ItineraryAnimalRecord(
               species=carryover.species,
               exhibit=carryover.exhibit,
               old_likelihood=None,
               new_likelihood=None ) ],
      )

      new_likelihood = (
         None
         if not saved_animals
         else max( ( a.likelihood or 0 ) for a in saved_animals ) )

      diffs.append(
         AnimalDiff(
            species=carryover.species,
            exhibit=carryover.exhibit,
            old_likelihood=carryover.old_likelihood,
            new_likelihood=new_likelihood,
            is_added=carryover.is_added,
            start_time=carryover.start_time,
            end_time=carryover.end_time,
         )
      )

   return diffs



def validate_itinerary_attractions(
      attraction_controller: type[ AttractionController ],
      attractions: tuple[ str, ... ],
      new_visit_date: date,
      old_visit_date: DateKey | None = None,
      saved_itinerary_attraction_rows: list[ ItineraryAttractionRecord ] | None = None ) -> list[ AttractionDiff ]:

   diffs: list[ AttractionDiff ] = []

   for attraction_name in attractions:
      carryover = itinerary_attraction_save_carryover(
         saved_itinerary_attraction_rows,
         attraction_name,
         old_visit_date=old_visit_date )

      new_likelihood = attraction_controller.get_attraction_likelihood_for_visit_date(
         visit_date=new_visit_date,
         attraction_name=attraction_name )

      diffs.append(
         AttractionDiff(
            name=carryover.name,
            old_likelihood=carryover.old_likelihood,
            new_likelihood=new_likelihood,
            start_time=carryover.start_time,
            end_time=carryover.end_time,
         )
      )

   return diffs



def itinerary_events_from_saved_rows(
      event_rows: list[ ItineraryEventRecord ] ) -> list[ ItineraryEvent ]:
   return [
      ItineraryEvent(
         event_type=event.event_type,
         start_time=event.start_time,
         end_time=event.end_time,
      )
      for event in event_rows
   ]



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
   saved_itinerary_wild_encounter_rows: list[ ItineraryWildEncounterRecord ] = []
   saved_itinerary_event_rows: list[ ItineraryEventRecord ] = []

   if old_visit_date != None:
      saved_itinerary_animal_rows = fetch_itinerary_animal_rows( conn )
      saved_itinerary_attraction_rows = fetch_itinerary_attraction_rows( conn )
      saved_itinerary_wild_encounter_rows = fetch_itinerary_wild_encounter_rows( conn )
      saved_itinerary_event_rows = fetch_itinerary_event_rows( conn )

   return ValidatedItinerary(
      arrival_time=save_input.arrival_time,
      departure_time=save_input.departure_time,
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
            year=save_input.year() ),
         saved_wild_encounter_rows=saved_itinerary_wild_encounter_rows ),
      events=itinerary_events_from_saved_rows( saved_itinerary_event_rows ),
   )
