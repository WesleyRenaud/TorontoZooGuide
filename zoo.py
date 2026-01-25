import calendar, math
import database

class Animal:
   def __init__( self, species, exhibit, seasonal_viewing_summary, seasonal_viewing_tips, general_viewing_tips, animal_info,
                 specific_animal_info, enclosure_type, x_coord, y_coord, seasonal_viewing_information, likelihood=None ):
      self.species = species
      self.exhibit = exhibit
      self.seasonal_viewing_summary = seasonal_viewing_summary
      self.seasonal_viewing_tips = seasonal_viewing_tips
      self.general_viewing_tips = general_viewing_tips
      self.animal_info = animal_info
      self.specific_animal_info = specific_animal_info
      self.enclosure_type = enclosure_type
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.seasonal_viewing_information = seasonal_viewing_information
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'species': self.species,
         'exhibit': self.exhibit,
         'seasonal_viewing_summary': self.seasonal_viewing_summary,
         'seasonal_viewing_tips': self.seasonal_viewing_tips,
         'general_viewing_tips': self.general_viewing_tips,
         'animal_info': self.animal_info,
         'specific_animal_info': self.specific_animal_info,
         'enclosure_type': self.enclosure_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'seasonal_viewing_information': self.seasonal_viewing_information,
         'likelihood': self.likelihood
      }
   

class Zoo_Util:
   def get_average_temperature( self, month, day ):
      # Convert month/day to day-of-year
      month = self.get_month_int( month )
      day_of_year = sum( calendar.monthrange( 2024, m )[1] for m in range( 1, month ) ) + day

      # Month start temperatures (°C)
      month_base = {
         1: -5.0,   # January
         2: -4.0,   # February
         3:  1.0,   # March
         4:  8.0,   # April
         5: 14.0,   # May
         6: 22.0,   # June
         7: 26.0,   # July
         8: 24.0,   # August
         9: 21.0,   # September
         10: 17.0,  # October
         11: 10.0,   # November
         12: 1.0   # December
      }

      # Compute start-of-month day-of-year mapping
      month_start_doy = []
      cumulative = 1
      for m in range( 1, 13 ):
         month_start_doy.append( (cumulative, month_base[m]) )
         cumulative += calendar.monthrange( 2024, m )[1]

      # Find which interval the day-of-year falls into
      for i in range( len( month_start_doy ) - 1 ):
         start_day, start_temp = month_start_doy[i]
         end_day, end_temp = month_start_doy[i+1]
         if start_day <= day_of_year < end_day:
            progress = (day_of_year - start_day) / (end_day - start_day)
            temp = start_temp + (end_temp - start_temp) * progress
            return round( temp, 1 )

      # If day is in December
      temp = month_start_doy[-1][1]
      return round( temp, 1 )


   # Returns probability (0.0 – 1.0) that snow is on the ground in Toronto on the given month & day
   def get_snow_likelihood( self, month, day ):
      month = self.get_month_int( month )

      MONTH_SNOW_BASE = {
         1: 0.90,   # January
         2: 0.85,
         3: 0.50,
         4: 0.10,
         5: 0.01,
         6: 0.00,
         7: 0.00,
         8: 0.00,
         9: 0.00,
         10: 0.02,
         11: 0.20,
         12: 0.70
      }
      
      base = MONTH_SNOW_BASE.get( month, 0.0 )

      days_in_month = calendar.monthrange( 2024, month )[1]
      progress = (day - 1) / days_in_month   # 0 → 1 through the month

      # December: snow builds
      if month == 12:
         base *= 0.6 + 0.4 * progress

      # March: snow melts
      elif month == 3:
         base *= 1.0 - 0.7 * progress

      # November: snow builds
      elif month == 11:
         base *= 0.3 + 0.7 * progress

      # April: snow melts quickly
      elif month == 4:
         base *= 1.0 - progress

      return round( max( 0.0, min( 1.0, base ) ), 2 )


   def get_month_int( self, month ):
      if month in ('JAN', 'Jan'):
         return 1
      elif month in ('FEB', 'Feb'):
         return 2
      elif month in ('MAR', 'Mar'):
         return 3
      elif month in ('APR', 'Apr'):
         return 4
      elif month in ('MAY', 'May'):
         return 5
      elif month in ('JUN', 'Jun'):
         return 6
      elif month in ('JUL', 'Jul'):
         return 7
      elif month in ('AUG', 'Aug'):
         return 8
      elif month in ('SEP', 'Sep'):
         return 9
      elif month in ('OCT', 'Oct'):
         return 10
      elif month in ('NOV', 'Nov'):
         return 11
      elif month in ('DEC', 'Dec'):
         return 12

      return None
      

   def get_day_of_year(self, month, day ):
      month_index = {
         "JAN":0, "FEB":1, "MAR":2, "APR":3, "MAY":4, "JUN":5,
         "JUL":6, "AUG":7, "SEP":8, "OCT":9, "NOV":10, "DEC":11
      }

      days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

      doy = sum( days_in_month[:month_index[month]] )
      return doy + (day - 1)
   

   def get_next_month( self, month ):
      if month in ('JAN', 'Jan'):
         return 'Feb'
      elif month in ('FEB', 'Feb'):
         return 'Mar'
      elif month in ('MAR', 'Mar'):
         return 'Apr'
      elif month in ('APR', 'Apr'):
         return 'May'
      elif month in ('MAY', 'May'):
         return 'Jun'
      elif month in ('JUN', 'Jun'):
         return 'Jul'
      elif month in ('JUL', 'Jul'):
         return 'Aug'
      elif month in ('AUG', 'Aug'):
         return 'Sep'
      elif month in ('SEP', 'Sep'):
         return 'Oct'
      elif month in ('OCT', 'Oct'):
         return 'Nov'
      elif month in ('NOV', 'Nov'):
         return 'Dec'
      elif month in ('DEC', 'Dec'):
         return 'Jan'
      

   def get_number_of_days_in_month( self, month ):
      if month in ('JAN', 'Jan', 'MAR', 'Mar', 'MAY', 'May', 'JUL', 'Jul', 'AUG', 'Aug', 'OCT', 'Oct', 'DEC', 'Dec'):
         return 31
      elif month in ('APR', 'Apr', 'JUN', 'Jun', 'SEP', 'Sep', 'NOV', 'Nov'):
         return 30
      elif month in ('FEB', 'Feb'):
         return 28
      

   # Returns probability (between 0 and 1) that temperature is >= min_temperature, assuming a normal distribution N(mu, sigma)
   def get_temperature_probability( self, mu, sigma, min_temperature ):
      z = (min_temperature - mu) / sigma

      # Standard normal CDF via error function
      cdf = 0.5 * (1 + math.erf( z / math.sqrt( 2) ) )

      return round( 1.0 - cdf, 3 )