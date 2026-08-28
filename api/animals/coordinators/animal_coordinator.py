from __future__ import annotations

from ..data_access.animal_information_provider import AnimalInformationProvider
from ..data_access.animal_species_name_provider import AnimalSpeciesNameProvider
from ..data_access.animal_status_provider import AnimalStatusProvider
from ..data_access.animal_viewable_on_day_provider import AnimalViewableOnDayProvider
from ..data_access.animal_viewing_alert_provider import AnimalViewingAlertProvider
from ..data_access.animal_viewing_scope_provider import AnimalViewingScopeProvider
from ..data_access.animal_visibility_schedule_provider import AnimalVisibilityScheduleProvider
from ..domain.animal_viewability_builder import AnimalViewabilityBuilder
from ..domain.animal_viewability_context_builder import AnimalViewabilityContextBuilder
from ..domain.itinerary_animal_records_filter_builder import ItineraryAnimalRecordsFilterBuilder
from ...itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..itinerary.itinerary_animals_builder import ItineraryAnimalsBuilder
from ...models import Animal
from ...request_connection_provider import RequestConnectionProvider
from ..scheduling.animal_limited_viewing_schedule_builder import AnimalLimitedViewingScheduleBuilder
from ..search.animals_matching_query_builder import AnimalsMatchingQueryBuilder
from ...shared.enums import AnimalViewingScope
from ..status.animal_off_display_status_builder import AnimalOffDisplayStatusBuilder
from ..status.animal_viewing_alert_builder import AnimalViewingAlertBuilder
from ...types import Types


class AnimalCoordinator():
   @classmethod
   def get_animals_viewable_on_day(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         temp: float | None = None,
         include_off_display_animals: bool = False,
         for_itinerary: bool = False,
         threshold: int | None = None,
         exhibits_to_include: list[ str ] | None = None ) -> list[ Animal ]:

      exhibits_to_include = exhibits_to_include or []
      context = AnimalViewabilityContextBuilder.resolve(
         day=day,
         month=month,
         year=year,
         temp=temp )

      animal_records = AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
         RequestConnectionProvider.get(),
         context.calendar_month,
         context.day_of_month,
         exhibits_to_include=exhibits_to_include )

      if for_itinerary:
         animal_records = ItineraryAnimalRecordsFilterBuilder.filter( animal_records )

      return AnimalViewabilityBuilder.build_viewable_animals_on_day(
         animal_records,
         target_date=context.target_date,
         temp=context.temp,
         sigma=context.sigma,
         include_off_display_animals=include_off_display_animals,
         threshold=threshold )


   @classmethod
   def get_animal_information(
         cls,
         species: str,
         exhibit: str ) -> Animal | None:
      return AnimalInformationProvider.fetch_animal_information(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit )


   @classmethod
   def get_animal_species_names( cls ) -> list[ str ]:
      return AnimalSpeciesNameProvider.fetch_animal_species_names( RequestConnectionProvider.get() )


   @classmethod
   def get_animal_viewing_scopes(
         cls,
         species: str,
         exhibit: str ) -> list[ AnimalViewingScope ]:
      return AnimalViewingScopeProvider.fetch_animal_viewing_scopes(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit )


   @classmethod
   def set_animal_as_off_display(
         cls,
         species: str,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str,
         viewing_scope: AnimalViewingScope = AnimalViewingScope.ALL ) -> bool:
      status = AnimalOffDisplayStatusBuilder.build(
         species=species,
         exhibit=exhibit,
         viewing_scope=viewing_scope,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return AnimalStatusProvider.save_animal_off_display_status(
         RequestConnectionProvider.get(),
         species=status.species,
         exhibit=status.exhibit,
         viewing_scope=status.viewing_scope,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   @classmethod
   def set_animal_as_on_display(
         cls,
         species: str,
         exhibit: str,
         viewing_scope: AnimalViewingScope = AnimalViewingScope.ALL ) -> bool:
      return AnimalStatusProvider.save_animal_on_display_status(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit,
         viewing_scope=viewing_scope )


   @classmethod
   def set_animal_limited_viewing_schedule(
         cls,
         species: str,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         daily_start_time: str,
         daily_end_time: str,
         message: str ) -> bool:
      schedule = AnimalLimitedViewingScheduleBuilder.build(
         species=species,
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         daily_start_time=daily_start_time,
         daily_end_time=daily_end_time,
         message=message )

      return AnimalVisibilityScheduleProvider.save_animal_limited_viewing_schedule(
         RequestConnectionProvider.get(),
         species=schedule.species,
         exhibit=schedule.exhibit,
         start_date=schedule.start_date,
         end_date=schedule.end_date,
         daily_start_time=schedule.daily_start_time,
         daily_end_time=schedule.daily_end_time,
         message=schedule.message )


   @classmethod
   def remove_animal_visibility_schedule( cls, species: str, exhibit: str ) -> bool:
      return AnimalVisibilityScheduleProvider.delete_animal_visibility_schedule(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit )


   @classmethod
   def set_animal_viewing_alert(
         cls,
         species: str,
         exhibit: str,
         alert_start_date: Types.DateInput,
         alert_end_date: Types.DateInput,
         message: str ) -> bool:
      alert = AnimalViewingAlertBuilder.build(
         species=species,
         exhibit=exhibit,
         alert_start_date=alert_start_date,
         alert_end_date=alert_end_date,
         message=message )

      return AnimalViewingAlertProvider.save_animal_viewing_alert(
         RequestConnectionProvider.get(),
         species=alert.species,
         exhibit=alert.exhibit,
         alert_start_date=alert.start_date,
         alert_end_date=alert.end_date,
         message=alert.message )


   @classmethod
   def remove_animal_viewing_alert( cls, species: str, exhibit: str ) -> bool:
      return AnimalViewingAlertProvider.delete_animal_viewing_alert(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit )


   @classmethod
   def get_animals_for_saved_itinerary(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
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

      return ItineraryAnimalsBuilder.build(
         viewable_animals,
         saved_animals )


   @classmethod
   def get_animals_matching_query(
         cls,
         query: str,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear,
         temp: float | None = None,
         include_off_display_animals: bool = False,
         for_itinerary: bool = False,
         threshold: int | None = None ) -> list[ Animal ]:

      animals = cls.get_animals_viewable_on_day(
         day=day,
         month=month,
         year=year,
         temp=temp,
         include_off_display_animals=include_off_display_animals,
         for_itinerary=for_itinerary,
         threshold=threshold )

      return AnimalsMatchingQueryBuilder.build( animals, query )
