from __future__ import annotations

from datetime import date

from api.animals.domain.animal_viewability_context_builder import AnimalViewabilityContextBuilder
from api.shared.weather import Weather


VISIT_DAY = 15
VISIT_MONTH = 6
VISIT_YEAR = 2026
FORECAST_TEMPERATURE = 24.0


def Test_Resolve_TestProvidedTemperature_ExpectForecastContext() -> None:
   context = AnimalViewabilityContextBuilder.resolve(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      temp=FORECAST_TEMPERATURE )

   assert context.target_date == date( VISIT_YEAR, VISIT_MONTH, VISIT_DAY )
   assert context.calendar_month == VISIT_MONTH
   assert context.day_of_month == VISIT_DAY
   assert context.temp == FORECAST_TEMPERATURE
   assert context.sigma == 2


def Test_Resolve_TestMissingTemperature_ExpectSeasonalAverageContext() -> None:
   context = AnimalViewabilityContextBuilder.resolve(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR )

   expected_temperature = Weather.get_average_temperature(
      month=VISIT_MONTH,
      day=VISIT_DAY )

   assert context.temp == expected_temperature
   assert context.sigma == 3
