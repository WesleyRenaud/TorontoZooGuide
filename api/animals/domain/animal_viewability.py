from __future__ import annotations

from datetime import date

from .animal_viewability_context import AnimalViewabilityContext
from ..data_access.animal_viewability_record import AnimalViewabilityRecord
from .indoor_outdoor_viewing_visibility import apply_indoor_outdoor_viewing_visibility
from ...models import Animal
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...shared.enums import EnclosureType
from ...shared.enums import ScheduleStatus
from ...shared.value_conversion import ValueConversion
from ...shared.weather import Weather
from ...types import MonthInput, VisitDay, VisitYear
from ...walk_graph.resolve_viewing_walk_node_id import apply_viewing_walk_node_id_to_animal


def resolve_temperature_likelihood_context(
      month: int,
      day: int,
      temp: float | None = None ) -> tuple[ float, int ]:
   if temp is None:
      # Historical average temperatures are less precise than a user-supplied forecast/current temperature,
      # so the likelihood model uses a wider distribution when falling back to seasonal averages.
      return (
         Weather.get_average_temperature( month=month, day=day ),
         3 )

   return ( temp, 2 )


def resolve_animal_viewability_context(
      day: VisitDay,
      month: MonthInput,
      year: VisitYear,
      temp: float | None = None ) -> AnimalViewabilityContext:
   target_date = CalendarDates.visit_target_date( month, day, year )
   calendar_month = target_date.month
   day_of_month = target_date.day
   temp, sigma = resolve_temperature_likelihood_context(
      month=target_date.month,
      day=day_of_month,
      temp=temp )

   return AnimalViewabilityContext(
      calendar_month=calendar_month,
      day_of_month=day_of_month,
      target_date=target_date,
      temp=temp,
      sigma=sigma )


def get_active_off_display_status(
      animal: AnimalViewabilityRecord,
      target_date: date ) -> tuple[ bool, str | None ]:
   stored_is_off_display = bool( animal.is_off_display ) if animal.is_off_display != None else False

   if not stored_is_off_display:
      return False, None

   off_display_message = animal.off_display_message
   off_display_start = animal.off_display_start
   off_display_end = animal.off_display_end

   is_off_display = DateValues.is_date_in_range(
      target_date=target_date,
      start_date_value=off_display_start,
      end_date_value=off_display_end )

   if is_off_display:
      return True, off_display_message

   return False, None


def get_active_limited_viewing_status(
      animal: AnimalViewabilityRecord,
      target_date: date ) -> tuple[ bool, str | None ]:
   schedule_start_date = animal.schedule_start_date
   schedule_end_date = animal.schedule_end_date
   daily_start_time = animal.daily_start_time
   daily_end_time = animal.daily_end_time
   viewing_message = animal.viewing_message

   if daily_start_time == None or daily_end_time == None:
      return False, None

   is_active = DateValues.is_date_in_range( target_date=target_date, start_date_value=schedule_start_date, end_date_value=schedule_end_date )

   if is_active:
      return True, viewing_message

   return False, None


def get_active_viewing_alert_status(
      animal: AnimalViewabilityRecord,
      target_date: date ) -> tuple[ bool, str | None ]:
   alert_message = animal.alert_message
   alert_start_date = animal.alert_start_date
   alert_end_date = animal.alert_end_date

   if alert_message == None:
      return False, None

   is_active = DateValues.is_date_in_range( target_date=target_date, start_date_value=alert_start_date, end_date_value=alert_end_date )

   if is_active:
      return True, alert_message

   return False, None


def get_active_exhibit_status(
      animal: AnimalViewabilityRecord,
      target_date: date ) -> tuple[ ScheduleStatus, str | None ]:
   if animal.is_closed == None:
      return ScheduleStatus.UNKNOWN, None

   start_date = animal.closed_start
   end_date = animal.closed_end

   is_active = DateValues.is_date_in_range(
      target_date=target_date,
      start_date_value=start_date,
      end_date_value=end_date )

   if not is_active:
      return ScheduleStatus.UNKNOWN, None

   if bool( animal.is_closed ):
      return ScheduleStatus.CLOSED, animal.closed_message

   return ScheduleStatus.OPEN, None


def calculate_animal_likelihood(
      temp: float,
      sigma: int,
      enclosure_type: str | None,
      min_temperature: float | None,
      day_seasonal_multiplier: float | None,
      exhibit_day_seasonal_availability_multiplier: float = 1.0 ) -> int:
   if EnclosureType.is_indoor( enclosure_type ):
      temperature_likelihood = 1.0
      animal_seasonal_multiplier = 1.0
   else:
      if min_temperature is None:
         temperature_likelihood = 1.0
      else:
         temperature_likelihood = Weather.get_temperature_probability(
            mu=temp,
            sigma=sigma,
            min_temperature=min_temperature )

      animal_seasonal_multiplier = day_seasonal_multiplier if day_seasonal_multiplier is not None else 1.0

   exhibit_seasonal_multiplier = (
      exhibit_day_seasonal_availability_multiplier
      if exhibit_day_seasonal_availability_multiplier is not None
      else 1.0
   )
   likelihood = max(
      0.0,
      min(
         temperature_likelihood
         * animal_seasonal_multiplier
         * exhibit_seasonal_multiplier,
         1.0 ) )

   return max( round( likelihood * 100 ), 0 )


def build_viewable_animals_on_day(
      animal_records: list[ AnimalViewabilityRecord ],
      target_date: date,
      temp: float,
      sigma: int,
      include_off_display_animals: bool = False,
      threshold: int = 0 ) -> list[ Animal ]:
   built_animals = [
      build_viewable_animal_from_record(
         animal_record,
         target_date=target_date,
         temp=temp,
         sigma=sigma )
      for animal_record in animal_records
   ]
   visible_animals = apply_indoor_outdoor_viewing_visibility( built_animals )

   animals: list[ Animal ] = []

   for animal in visible_animals:
      if (
            animal.likelihood > threshold
            or ( include_off_display_animals and animal.likelihood == 0 ) ):
         animals.append( animal )

   return animals


def build_viewable_animal_from_record(
      animal: AnimalViewabilityRecord,
      target_date: date,
      temp: float,
      sigma: int ) -> Animal:
   exhibit_day_seasonal_availability_multiplier = animal.exhibit_day_seasonal_availability_multiplier

   is_off_display, off_display_message = get_active_off_display_status(
      animal=animal,
      target_date=target_date )

   has_limited_viewing_schedule, limited_viewing_message = get_active_limited_viewing_status(
      animal=animal,
      target_date=target_date )

   _, viewing_alert_message = get_active_viewing_alert_status(
      animal=animal,
      target_date=target_date )
   viewing_alert_messages = ValueConversion.as_singleton_list(
      viewing_alert_message )

   exhibit_status, exhibit_closed_message = get_active_exhibit_status(
      animal=animal,
      target_date=target_date )

   likelihood = calculate_viewable_animal_likelihood(
      animal,
      temp=temp,
      sigma=sigma,
      is_off_display=is_off_display,
      exhibit_status=exhibit_status )
   display_message = get_viewable_animal_display_message(
      animal,
      likelihood=likelihood,
      is_off_display=is_off_display,
      off_display_message=off_display_message,
      exhibit_status=exhibit_status,
      exhibit_closed_message=exhibit_closed_message,
      exhibit_day_seasonal_availability_multiplier=exhibit_day_seasonal_availability_multiplier )

   viewable_animal = Animal(
      species=animal.species,
      latin_name=animal.latin_name,
      general_viewing_tips=animal.general_viewing_tips,
      seasonal_viewing_tips=animal.seasonal_viewing_tips,
      identification=animal.identification,
      habitat_and_range=animal.habitat_and_range,
      diet_and_feeding=animal.diet_and_feeding,
      behaviour_and_life_cycle=animal.behaviour_and_social_life,
      adaptations=animal.adaptations,
      reproduction_and_life_cycle=animal.reproduction_and_life_cycle,
      animals_at_the_zoo=animal.animals_at_the_zoo,
      exhibit=animal.exhibit,
      seasonal_viewing_summary=animal.seasonal_viewing_summary,
      seasonal_viewing_information=animal.seasonal_viewing_information,
      off_display_message=display_message,
      enclosure_type=animal.enclosure_type,
      enclosure_name=animal.enclosure_name,
      x_coord=animal.x_coord,
      y_coord=animal.y_coord,
      likelihood=likelihood,
      has_limited_viewing_schedule=has_limited_viewing_schedule,
      limited_viewing_message=limited_viewing_message,
      viewing_alert_messages=viewing_alert_messages,
      include_all_viewing_spots=animal.include_all_viewing_spots )

   apply_viewing_walk_node_id_to_animal( viewable_animal )

   return viewable_animal


def calculate_viewable_animal_likelihood(
      animal: AnimalViewabilityRecord,
      temp: float,
      sigma: int,
      is_off_display: bool,
      exhibit_status: ScheduleStatus ) -> int:
   if is_off_display or exhibit_status == ScheduleStatus.CLOSED:
      return 0

   applied_exhibit_day_availability_multiplier = 1.0

   if exhibit_status == ScheduleStatus.UNKNOWN:
      applied_exhibit_day_availability_multiplier = animal.exhibit_day_seasonal_availability_multiplier

   return calculate_animal_likelihood(
      temp=temp,
      sigma=sigma,
      enclosure_type=animal.enclosure_type,
      min_temperature=animal.min_temperature,
      day_seasonal_multiplier=animal.animal_day_seasonal_multiplier,
      exhibit_day_seasonal_availability_multiplier=applied_exhibit_day_availability_multiplier )


def get_viewable_animal_display_message(
      animal: AnimalViewabilityRecord,
      likelihood: int,
      is_off_display: bool,
      off_display_message: str | None,
      exhibit_status: ScheduleStatus,
      exhibit_closed_message: str | None,
      exhibit_day_seasonal_availability_multiplier: float | None ) -> str | None:
   if is_off_display:
      return off_display_message

   if exhibit_status == ScheduleStatus.CLOSED:
      return exhibit_closed_message

   if likelihood != 0:
      return None

   if (
         exhibit_status == ScheduleStatus.UNKNOWN
         and exhibit_day_seasonal_availability_multiplier == 0 ):
      return f'The { animal.exhibit } is most likely closed on this day.'

   if animal.seasonally_off_display_message:
      return animal.seasonally_off_display_message

   return f'The { animal.species } is most likely off display on this day.'
