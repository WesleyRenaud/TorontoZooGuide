from __future__ import annotations

from api.shared.weather import Weather


def Test_GetAverageTemperature_TestMonthStartAnchors_ExpectJanuaryColdestAndJulyWarmest() -> None:
   month_start_temperatures = [
      Weather.get_average_temperature( month, 1 )
      for month in range( 1, 13 )
   ]

   assert month_start_temperatures[ 0 ] == min( month_start_temperatures )
   assert month_start_temperatures[ 6 ] == max( month_start_temperatures )


def Test_GetAverageTemperature_TestMidMonth_ExpectInterpolatesBetweenAdjacentMonthStarts() -> None:
   january_start = Weather.get_average_temperature( 'January', 1 )
   february_start = Weather.get_average_temperature( 'February', 1 )
   mid_january = Weather.get_average_temperature( 'January', 15 )

   assert january_start < mid_january < february_start


def Test_GetAverageTemperature_TestMidJune_ExpectInterpolatesTowardJuly() -> None:
   june_start = Weather.get_average_temperature( 'June', 1 )
   july_start = Weather.get_average_temperature( 'July', 1 )
   mid_june = Weather.get_average_temperature( 'June', 15 )

   assert june_start < mid_june < july_start


def Test_GetTemperatureProbability_TestAtMean_ExpectHalf() -> None:
   assert Weather.get_temperature_probability( mu=20, sigma=2, min_temperature=20 ) == 0.5


def Test_GetTemperatureProbability_TestWellAboveMean_ExpectNearCertain() -> None:
   assert Weather.get_temperature_probability( mu=25, sigma=2, min_temperature=20 ) > 0.99
