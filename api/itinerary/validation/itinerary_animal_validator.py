from __future__ import annotations

from datetime import date

from ...animals.coordinators.animal_coordinator import AnimalCoordinator
from ...animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from ..data_access.itinerary_animal_input import ItineraryAnimalInput
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_animal_save_carryover_mapper import ItineraryAnimalSaveCarryoverMapper
from ..data_access.itinerary_animal_save_carryover_record import ItineraryAnimalSaveCarryover
from ..domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from ...models import Animal
from ...models import AnimalDiff
from ...shared.value_conversion import ValueConversion
from ...types import DateKey, ScheduleTimeKey


class ItineraryAnimalValidator():
   @classmethod
   def validate(
         cls,
         animal_coordinator: type[ AnimalCoordinator ],
         animals: list[ ItineraryAnimalInput ],
         new_visit_date: date,
         *,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey,
         new_visit_date_temp: float | None = None,
         old_visit_date: DateKey | None = None,
         saved_animal_rows: list[ ItineraryAnimalRecord ] | None = None,
         visit_date_is_changing: bool = False ) -> list[ AnimalDiff ]:
      diffs: list[ AnimalDiff ] = []
      removed_habitats: list[ tuple[
         ItineraryAnimalSaveCarryover,
         ScheduleTimeKey,
         ScheduleTimeKey,
      ] ] = []

      for animal in animals:
         carryover = ItineraryAnimalSaveCarryoverMapper.map_from_saved_animal_rows(
            saved_animal_rows,
            animal,
            old_visit_date=old_visit_date )
         start_time, end_time = (
            ( carryover.start_time, carryover.end_time )
            if visit_date_is_changing
            else ItineraryVisitWindowBuilder.cleared_schedule_times(
               carryover.start_time,
               carryover.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ) )

         saved_animals = animal_coordinator.get_animals_for_saved_itinerary(
            day=new_visit_date.day,
            month=new_visit_date.month,
            year=new_visit_date.year,
            temp=new_visit_date_temp,
            saved_animals=[
               ItineraryAnimalRecord(
                  species=carryover.species,
                  exhibit=carryover.exhibit,
                  enclosure_name=carryover.enclosure_name,
                  old_likelihood=None,
                  new_likelihood=None ) ],
         )

         if not saved_animals:
            removed_habitats.append( ( carryover, start_time, end_time ) )
            continue

         diffs.append(
            cls._animal_diff_from_carryover(
               carryover,
               enclosure_name=carryover.enclosure_name,
               new_likelihood=max(
                  ( a.likelihood or 0 ) for a in saved_animals ),
               start_time=start_time,
               end_time=end_time ) )

      for carryover, start_time, end_time in removed_habitats:
         preferred = cls._preferred_habitat_for_removed_animal(
            animal_coordinator,
            visit_date=new_visit_date,
            visit_date_temp=new_visit_date_temp,
            removed=carryover )

         if preferred is None:
            diffs.append(
               cls._animal_diff_from_carryover(
                  carryover,
                  enclosure_name=carryover.enclosure_name,
                  new_likelihood=None,
                  start_time=start_time,
                  end_time=end_time ) )
            continue

         enclosure_name = ValueConversion.as_nullable_string(
            preferred.enclosure_name )
         already_present = any(
            diff.species == carryover.species
            and diff.exhibit == carryover.exhibit
            and diff.enclosure_name == enclosure_name
            for diff in diffs )

         if already_present:
            continue

         diffs.append(
            cls._animal_diff_from_carryover(
               carryover,
               enclosure_name=enclosure_name,
               new_likelihood=preferred.likelihood or 0,
               start_time=start_time,
               end_time=end_time ) )

      return diffs


   @classmethod
   def _preferred_habitat_for_removed_animal(
         cls,
         animal_coordinator: type[ AnimalCoordinator ],
         *,
         visit_date: date,
         visit_date_temp: float | None,
         removed: ItineraryAnimalSaveCarryover ) -> Animal | None:
      preferred_habitats = [
         animal
         for animal in animal_coordinator.get_animals_viewable_on_day(
            day=visit_date.day,
            month=visit_date.month,
            year=visit_date.year,
            temp=visit_date_temp,
            include_off_display_animals=True,
            threshold=0,
            exhibits_to_include=[ removed.exhibit ] )
         if (
            SpeciesExhibitKeyBuilder.from_animal( animal )
            == SpeciesExhibitKeyBuilder.from_values( removed.species, removed.exhibit ) )
      ]

      if len( preferred_habitats ) != 1:
         return None

      return preferred_habitats[ 0 ]


   @classmethod
   def _animal_diff_from_carryover(
         cls,
         carryover: ItineraryAnimalSaveCarryover,
         *,
         enclosure_name: str | None,
         new_likelihood: int | None,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> AnimalDiff:
      return AnimalDiff(
         species=carryover.species,
         exhibit=carryover.exhibit,
         enclosure_name=enclosure_name,
         old_likelihood=carryover.old_likelihood,
         new_likelihood=new_likelihood,
         is_added=carryover.is_added,
         covered_by_talk=carryover.covered_by_talk,
         start_time=start_time,
         end_time=end_time,
      )
