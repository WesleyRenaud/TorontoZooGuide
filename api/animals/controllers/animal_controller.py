from ..data_access.animal_information import fetch_animal_information
from ..data_access.animal_species_name import fetch_animal_species_names
from ..data_access.animal_viewable_on_day import fetch_animals_viewable_on_day_records
from ..logic.animal_viewability import build_viewable_animals_on_day
from ..logic.animal_viewability import resolve_animal_viewability_context
from ..logic.animals_matching_query import build_animals_matching_query
from ..logic.itinerary_animals import build_itinerary_animals


class AnimalController():
   def __init__( self, conn ):
      self._conn = conn


   def get_animals_viewable_on_day(
         self,
         day,
         month,
         year,
         temp=None,
         include_off_display_animals=False,
         threshold=0,
         exhibits_to_include=None ):

      exhibits_to_include = exhibits_to_include or []
      context = resolve_animal_viewability_context(
         day=day,
         month=month,
         year=year,
         temp=temp )

      animal_records = fetch_animals_viewable_on_day_records(
         self._conn,
         context.calendar_month,
         context.day_of_month,
         exhibits_to_include=exhibits_to_include )

      return build_viewable_animals_on_day(
         animal_records,
         target_date=context.target_date,
         temp=context.temp,
         sigma=context.sigma,
         include_off_display_animals=include_off_display_animals,
         threshold=threshold )


   def get_animal_information( self, species ):
      return fetch_animal_information(
         self._conn,
         species=species )


   def get_animal_species_names( self ):
      return fetch_animal_species_names( self._conn )


   def get_animals_for_saved_itinerary(
         self,
         day,
         month,
         year,
         saved_animals,
         temp=None ):

      if not saved_animals:
         return []

      exhibits_to_include = list( {
         saved_animal.exhibit
         for saved_animal in saved_animals
      } )

      viewable_animals = self.get_animals_viewable_on_day(
         day=day,
         month=month,
         year=year,
         temp=temp,
         include_off_display_animals=True,
         threshold=0,
         exhibits_to_include=exhibits_to_include )

      return build_itinerary_animals(
         viewable_animals,
         saved_animals )


   def get_animals_matching_query(
         self,
         query,
         day,
         month,
         year,
         temp=None,
         include_off_display_animals=False ):

      animals = self.get_animals_viewable_on_day(
         day=day,
         month=month,
         year=year,
         temp=temp,
         include_off_display_animals=include_off_display_animals )

      return build_animals_matching_query( animals, query )
