from __future__ import annotations

from datetime import date

from ..data_access.animal_day_seasonal_viewability_provider import AnimalDaySeasonalViewabilityProvider
from ..data_access.animal_day_seasonal_viewability_record import AnimalDaySeasonalViewabilityRecord
from ..data_access.animal_enclosure_exhibit_name_provider import AnimalEnclosureExhibitNameProvider
from ..data_access.animal_information_provider import AnimalInformationProvider
from ..data_access.animal_off_display_exhibit_name_provider import AnimalOffDisplayExhibitNameProvider
from ..data_access.animal_off_display_record import AnimalOffDisplayRecord
from ..data_access.animal_off_display_species_name_provider import AnimalOffDisplaySpeciesNameProvider
from ..data_access.animal_off_display_viewing_scope_provider import AnimalOffDisplayViewingScopeProvider
from ..data_access.animal_species_name_provider import AnimalSpeciesNameProvider
from ..data_access.animal_status_provider import AnimalStatusProvider
from ..data_access.animal_viewable_on_day_provider import AnimalViewableOnDayProvider
from ..data_access.animal_viewing_alert_exhibit_name_provider import AnimalViewingAlertExhibitNameProvider
from ..data_access.animal_viewing_alert_provider import AnimalViewingAlertProvider
from ..data_access.animal_viewing_alert_species_name_provider import AnimalViewingAlertSpeciesNameProvider
from ..data_access.animal_viewing_scope_provider import AnimalViewingScopeProvider
from ..data_access.animal_visibility_schedule_exhibit_name_provider import AnimalVisibilityScheduleExhibitNameProvider
from ..data_access.animal_visibility_schedule_provider import AnimalVisibilityScheduleProvider
from ..data_access.animal_visibility_schedule_species_name_provider import AnimalVisibilityScheduleSpeciesNameProvider
from ..data_access.enclosure_off_display_month_provider import EnclosureOffDisplayMonthProvider
from ..domain.animal_species_exhibit import AnimalSpeciesExhibit
from ..domain.animal_viewability_builder import AnimalViewabilityBuilder
from ..domain.animal_viewability_context_builder import AnimalViewabilityContextBuilder
from ..domain.animal_viewing_scope import AnimalViewingScope
from ..domain.closure_linked_off_display_animal import ClosureLinkedOffDisplayAnimal
from ..domain.enclosure_off_display_month import EnclosureOffDisplayMonth
from ..domain.enclosure_off_display_status import EnclosureOffDisplayStatus
from ..domain.itinerary_animal_records_filter_builder import ItineraryAnimalRecordsFilterBuilder
from ..domain.seasonal_off_display_animal import SeasonalOffDisplayAnimal
from ..domain.seasonal_off_display_animal_builder import SeasonalOffDisplayAnimalBuilder
from ..domain.temporary_off_display_animal import TemporaryOffDisplayAnimal
from ...itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..itinerary.itinerary_animals_builder import ItineraryAnimalsBuilder
from ...models import Animal
from ...request_connection_provider import RequestConnectionProvider
from ..scheduling.animal_limited_viewing_schedule_builder import AnimalLimitedViewingScheduleBuilder
from ..search.animals_matching_query_builder import AnimalsMatchingQueryBuilder
from ...shared.calendar_dates import CalendarDates
from ...shared.date_values import DateValues
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
   def get_off_display_records( cls ) -> list[ AnimalOffDisplayRecord ]:
      return AnimalStatusProvider.fetch_off_display_records( RequestConnectionProvider.get() )


   @classmethod
   def get_off_display_enclosure_statuses( cls ) -> list[ EnclosureOffDisplayStatus ]:
      return AnimalStatusProvider.fetch_off_display_enclosure_statuses(
         RequestConnectionProvider.get() )


   @classmethod
   def get_temporary_off_display_animals( cls ) -> list[ TemporaryOffDisplayAnimal ]:
      return AnimalStatusProvider.fetch_temporary_off_display_animals(
         RequestConnectionProvider.get() )


   @classmethod
   def get_closure_linked_off_display_animals( cls ) -> list[ ClosureLinkedOffDisplayAnimal ]:
      return AnimalStatusProvider.fetch_closure_linked_off_display_animals(
         RequestConnectionProvider.get() )


   @classmethod
   def extend_closure_linked_off_display(
         cls,
         title: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> None:
      AnimalStatusProvider.extend_closure_linked_off_display_end(
         RequestConnectionProvider.get(),
         title=title,
         start_date=start_date,
         end_date=end_date )


   @classmethod
   def get_seasonal_off_display_animals( cls ) -> list[ SeasonalOffDisplayAnimal ]:
      return SeasonalOffDisplayAnimalBuilder.build(
         species=cls.get_animal_species_names(),
         records=cls.get_off_display_records(),
      )


   @classmethod
   def get_enclosure_off_display_months( cls ) -> list[ EnclosureOffDisplayMonth ]:
      return EnclosureOffDisplayMonthProvider.fetch_off_display_months(
         RequestConnectionProvider.get() )


   @classmethod
   def get_day_seasonal_viewability_records( cls ) -> list[ AnimalDaySeasonalViewabilityRecord ]:
      return AnimalDaySeasonalViewabilityProvider.fetch_records( RequestConnectionProvider.get() )


   @classmethod
   def get_exhibits_for_species( cls, species: str ) -> list[ str ]:
      return AnimalEnclosureExhibitNameProvider.fetch_exhibit_names_for_species(
         RequestConnectionProvider.get(),
         species=species )


   @classmethod
   def get_animal_species_exhibits( cls ) -> list[ AnimalSpeciesExhibit ]:
      return AnimalEnclosureExhibitNameProvider.fetch_animal_species_exhibits(
         RequestConnectionProvider.get() )


   @classmethod
   def get_off_display_animal_options(
         cls,
         exhibit: str | None,
         for_season_only: bool ) -> list[ str ]:
      if exhibit:
         return AnimalOffDisplaySpeciesNameProvider.fetch_off_display_species_names_in_exhibit(
            RequestConnectionProvider.get(),
            today=DateValues.today_date_key(),
            exhibit=exhibit,
            for_season_only=for_season_only )

      return AnimalOffDisplaySpeciesNameProvider.fetch_off_display_species_names(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key(),
         for_season_only=for_season_only )


   @classmethod
   def get_off_display_exhibit_options(
         cls,
         species: str,
         for_season_only: bool ) -> list[ str ]:
      if species:
         return AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names_for_species(
            RequestConnectionProvider.get(),
            today=DateValues.today_date_key(),
            species=species,
            for_season_only=for_season_only )

      return AnimalOffDisplayExhibitNameProvider.fetch_off_display_exhibit_names(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key(),
         for_season_only=for_season_only )


   @classmethod
   def get_animal_visibility_schedule_options( cls, exhibit: str | None = None ) -> list[ str ]:
      if exhibit:
         return AnimalVisibilityScheduleSpeciesNameProvider.fetch_visibility_schedule_species_names_in_exhibit(
            RequestConnectionProvider.get(),
            today=DateValues.today_date_key(),
            exhibit=exhibit )

      return AnimalVisibilityScheduleSpeciesNameProvider.fetch_visibility_schedule_species_names(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key() )


   @classmethod
   def get_animal_visibility_schedule_exhibit_options( cls, species: str ) -> list[ str ]:
      if species:
         return AnimalVisibilityScheduleExhibitNameProvider.fetch_visibility_schedule_exhibit_names_for_species(
            RequestConnectionProvider.get(),
            today=DateValues.today_date_key(),
            species=species )

      return AnimalVisibilityScheduleExhibitNameProvider.fetch_visibility_schedule_exhibit_names(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key() )


   @classmethod
   def get_animal_viewing_alert_options( cls, exhibit: str | None = None ) -> list[ str ]:
      if exhibit:
         return AnimalViewingAlertSpeciesNameProvider.fetch_viewing_alert_species_names_in_exhibit(
            RequestConnectionProvider.get(),
            today=DateValues.today_date_key(),
            exhibit=exhibit )

      return AnimalViewingAlertSpeciesNameProvider.fetch_viewing_alert_species_names(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key() )


   @classmethod
   def get_animal_viewing_alert_exhibit_options( cls, species: str ) -> list[ str ]:
      if species:
         return AnimalViewingAlertExhibitNameProvider.fetch_viewing_alert_exhibit_names_for_species(
            RequestConnectionProvider.get(),
            today=DateValues.today_date_key(),
            species=species )

      return AnimalViewingAlertExhibitNameProvider.fetch_viewing_alert_exhibit_names(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key() )


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
   def get_off_display_viewing_scope_options(
         cls,
         species: str,
         exhibit: str,
         for_season_only: bool ) -> list[ AnimalViewingScope ]:
      return AnimalOffDisplayViewingScopeProvider.fetch_off_display_viewing_scopes(
         RequestConnectionProvider.get(),
         today=DateValues.today_date_key(),
         species=species,
         exhibit=exhibit,
         for_season_only=for_season_only )


   @classmethod
   def set_animal_as_off_display(
         cls,
         species: str,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str,
         viewing_scopes: list[ AnimalViewingScope ],
         is_off_display_for_season: bool,
         closure_update_title: str | None,
         closure_update_start: Types.DateInput | None ) -> bool:
      status = AnimalOffDisplayStatusBuilder.build(
         species=species,
         exhibit=exhibit,
         viewing_scopes=viewing_scopes,
         start_date=start_date,
         end_date=end_date,
         message=message,
         is_off_display_for_season=is_off_display_for_season,
         closure_update_title=closure_update_title,
         closure_update_start=closure_update_start )

      return AnimalStatusProvider.save_animal_off_display_status(
         RequestConnectionProvider.get(),
         species=status.species,
         exhibit=status.exhibit,
         viewing_scopes=status.viewing_scopes,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message,
         is_off_display_for_season=status.is_off_display_for_season,
         closure_update_title=status.closure_update_title,
         closure_update_start=status.closure_update_start )


   @classmethod
   def set_off_display_for_season_until(
         cls,
         species: str,
         exhibit: str,
         today: date ) -> bool:
      until_month = EnclosureOffDisplayMonthProvider.fetch_until_month(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit )
      end_date = CalendarDates.next_month_end( until_month, today )
      viewing_scopes = AnimalViewingScopeProvider.fetch_animal_viewing_scopes(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit )

      return cls.set_animal_as_off_display(
         species=species,
         exhibit=exhibit,
         start_date=today,
         end_date=end_date,
         message='',
         viewing_scopes=viewing_scopes,
         is_off_display_for_season=True,
         closure_update_title=None,
         closure_update_start=None )


   @classmethod
   def set_animal_as_on_display(
         cls,
         species: str,
         exhibit: str,
         viewing_scopes: list[ AnimalViewingScope ] ) -> bool:
      return AnimalStatusProvider.save_animal_on_display_status(
         RequestConnectionProvider.get(),
         species=species,
         exhibit=exhibit,
         viewing_scopes=viewing_scopes )


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
