from __future__ import annotations

import calendar
import math

from ..types import MonthInput, VisitDay
from .calendar_dates import CalendarDates


class Weather:
   @staticmethod
   def get_average_temperature( month: MonthInput, day: VisitDay ) -> float:
      month = CalendarDates.normalize_month( month )
      day_of_year = sum( calendar.monthrange( 2024, m )[ 1 ] for m in range( 1, month ) ) + day

      month_base = {
         1: -5.0,
         2: -4.0,
         3:  1.0,
         4:  8.0,
         5: 14.0,
         6: 22.0,
         7: 26.0,
         8: 25.0,
         9: 22.0,
         10: 20.0,
         11: 10.0,
         12: 1.0
      }

      month_start_doy = []
      cumulative = 1
      for m in range( 1, 13 ):
         month_start_doy.append( ( cumulative, month_base[ m ] ) )
         cumulative += calendar.monthrange( 2024, m )[ 1 ]

      for i in range( len( month_start_doy ) - 1 ):
         start_day, start_temp = month_start_doy[ i ]
         end_day, end_temp = month_start_doy[ i + 1 ]
         if start_day <= day_of_year < end_day:
            progress = ( day_of_year - start_day ) / ( end_day - start_day )
            temp = start_temp + ( end_temp - start_temp ) * progress
            return round( temp, 1 )

      temp = month_start_doy[ -1 ][ 1 ]
      return round( temp, 1 )


   @staticmethod
   def get_temperature_probability( mu: float, sigma: float, min_temperature: float ) -> float:
      z = ( min_temperature - mu ) / sigma
      cdf = 0.5 * ( 1 + math.erf( z / math.sqrt( 2 ) ) )

      return round( 1.0 - cdf, 3 )
