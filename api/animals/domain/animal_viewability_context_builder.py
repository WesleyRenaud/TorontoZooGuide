from __future__ import annotations

from .animal_viewability_context import AnimalViewabilityContext
from ...shared.calendar_dates import CalendarDates
from ...shared.weather import Weather
from ...types import MonthInput, VisitDay, VisitYear


class AnimalViewabilityContextBuilder():
   @classmethod
   def _resolve_temperature_likelihood_context(
         cls,
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


   @classmethod
   def resolve(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         temp: float | None = None ) -> AnimalViewabilityContext:
      target_date = CalendarDates.visit_target_date( month, day, year )
      calendar_month = target_date.month
      day_of_month = target_date.day
      temp, sigma = cls._resolve_temperature_likelihood_context(
         month=target_date.month,
         day=day_of_month,
         temp=temp )

      return AnimalViewabilityContext(
         calendar_month=calendar_month,
         day_of_month=day_of_month,
         target_date=target_date,
         temp=temp,
         sigma=sigma )
