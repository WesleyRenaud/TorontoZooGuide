from ..data_access.animal_viewable_on_day import fetch_animals_viewable_on_day_records
from ..logic.animal_viewability import build_viewable_animals_on_day
from ..logic.animal_viewability import resolve_animal_viewability_context


class AnimalController():
   def __init__( self, conn ):
      self._conn = conn


   def get_animals_viewable_on_day(
         self,
         month,
         day,
         temp=None,
         include_off_display_animals=False,
         threshold=0,
         exhibits_to_include=None,
         calendar_year=None ):

      exhibits_to_include = exhibits_to_include or []
      context = resolve_animal_viewability_context(
         month=month,
         day=day,
         calendar_year=calendar_year,
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
