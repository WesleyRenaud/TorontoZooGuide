from __future__ import annotations

from ...models import Animal
from ...itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...types import DateInput, MonthInput, VisitDay, VisitMonth, VisitYear
from ..data_access.animal_information import fetch_animal_information
from ..data_access.animal_species_name import fetch_animal_species_names
from ..data_access.animal_status import save_animal_off_display_status
from ..data_access.animal_status import save_animal_on_display_status
from ..data_access.animal_visibility_schedule import delete_animal_visibility_schedule
from ..data_access.animal_visibility_schedule import save_animal_limited_viewing_schedule
from ..data_access.animal_viewing_alert import delete_animal_viewing_alert
from ..data_access.animal_viewing_alert import save_animal_viewing_alert
from ..data_access.animal_viewable_on_day import fetch_animals_viewable_on_day_records
from ..logic.animal_status import build_animal_off_display_status
from ..logic.animal_visibility_schedule import build_animal_limited_viewing_schedule
from ..logic.animal_viewing_alert_builder import build_animal_viewing_alert
from ..logic.animal_viewability import build_viewable_animals_on_day
from ..logic.animal_viewability import resolve_animal_viewability_context
from ..logic.animals_matching_query import build_animals_matching_query
from ..logic.itinerary_animals import build_itinerary_animals
from ...request_connection import get_connection


class AnimalController():


   @classmethod
   def get_animals_viewable_on_day(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         temp: float | None = None,
         include_off_display_animals: bool = False,
         threshold: int = 0,
         exhibits_to_include: list[ str ] | None = None ) -> list[ Animal ]:

      exhibits_to_include = exhibits_to_include or []
      context = resolve_animal_viewability_context(
         day=day,
         month=month,
         year=year,
         temp=temp )

      animal_records = fetch_animals_viewable_on_day_records(
         get_connection(),
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


   @classmethod
   def get_animal_information( cls, species: str ) -> Animal | None:
      return fetch_animal_information(
         get_connection(),
         species=species )


   @classmethod
   def get_animal_species_names( cls ) -> list[ str ]:
      return fetch_animal_species_names( get_connection() )


   @classmethod
   def set_animal_as_off_display(
         cls,
         species: str,
         exhibit: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:

      status = build_animal_off_display_status(
         species=species,
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_animal_off_display_status(
         get_connection(),
         species=status.species,
         exhibit=status.exhibit,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   @classmethod
   def set_animal_as_on_display( cls, species: str, exhibit: str ) -> bool:
      return save_animal_on_display_status(
         get_connection(),
         species=species,
         exhibit=exhibit )


   @classmethod
   def set_animal_limited_viewing_schedule(
         cls,
         species: str,
         exhibit: str,
         start_date: DateInput,
         end_date: DateInput,
         daily_start_time: str,
         daily_end_time: str,
         message: str ) -> bool:
      schedule = build_animal_limited_viewing_schedule(
         species=species,
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         daily_start_time=daily_start_time,
         daily_end_time=daily_end_time,
         message=message )

      return save_animal_limited_viewing_schedule(
         get_connection(),
         species=schedule.species,
         exhibit=schedule.exhibit,
         start_date=schedule.start_date,
         end_date=schedule.end_date,
         daily_start_time=schedule.daily_start_time,
         daily_end_time=schedule.daily_end_time,
         message=schedule.message )


   @classmethod
   def remove_animal_visibility_schedule( cls, species: str, exhibit: str ) -> bool:
      return delete_animal_visibility_schedule(
         get_connection(),
         species=species,
         exhibit=exhibit )


   @classmethod
   def set_animal_viewing_alert(
         cls,
         species: str,
         exhibit: str,
         alert_start_date: DateInput,
         alert_end_date: DateInput,
         message: str ) -> bool:
      alert = build_animal_viewing_alert(
         species=species,
         exhibit=exhibit,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )

      return save_animal_viewing_alert(
         get_connection(),
         species=alert.species,
         exhibit=alert.exhibit,
         alert_start_date=alert.start_date,
         alert_end_date=alert.end_date,
         message=alert.message )


   @classmethod
   def remove_animal_viewing_alert( cls, species: str, exhibit: str ) -> bool:
      return delete_animal_viewing_alert(
         get_connection(),
         species=species,
         exhibit=exhibit )


   @classmethod
   def get_animals_for_saved_itinerary(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         saved_animals: list[ ItineraryAnimalRecord ],
         temp: float | None = None ) -> list[ Animal ]:

      if not saved_animals:
         return []

      exhibits_to_include = list( {
         saved_animal.exhibit
         for saved_animal in saved_animals
      } )

      viewable_animals = cls.get_animals_viewable_on_day(
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


   @classmethod
   def get_animals_matching_query(
         cls,
         query: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         temp: float | None = None,
         include_off_display_animals: bool = False ) -> list[ Animal ]:

      animals = cls.get_animals_viewable_on_day(
         day=day,
         month=month,
         year=year,
         temp=temp,
         include_off_display_animals=include_off_display_animals )

      return build_animals_matching_query( animals, query )
