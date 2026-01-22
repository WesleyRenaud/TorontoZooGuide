import calendar, math

class Animal:
   def __init__( self, species, location, seasonal_viewing_summary, seasonal_viewing_tips, general_viewing_tips, animal_info,
                 specific_animal_info, exhibit_type, x_coord, y_coord, likelihood=None ):
      self.species = species
      self.location = location
      self.seasonal_viewing_summary = seasonal_viewing_summary
      self.seasonal_viewing_tips = seasonal_viewing_tips
      self.general_viewing_tips = general_viewing_tips
      self.animal_info = animal_info
      self.specific_animal_info = specific_animal_info
      self.exhibit_type = exhibit_type
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'species': self.species,
         'location': self.location,
         'seasonal_viewing_summary': self.seasonal_viewing_summary,
         'seasonal_viewing_tips': self.seasonal_viewing_tips,
         'general_viewing_tips': self.general_viewing_tips,
         'animal_info': self.animal_info,
         'specific_animal_info': self.specific_animal_info,
         'exhibit_type': self.exhibit_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'likelihood': self.likelihood
      }
   

class Zoo_Util:
   def species_viewable_inside_and_outside( self, species ):
      species_viewable_inside_and_outside =\
      [
         'African penguin', 'Golden lion tamarin', 'Southern hairy-nosed wombat', 'Sumatran orangutan', 'Two-toed sloth',
         'Western lowland gorilla', 'White-breasted cormorant', 'White-faced saki'
      ]
      
      if species in species_viewable_inside_and_outside:
         return True
      else:
         return False
      

   def get_average_temperature( self, month, day ):
      # Convert month/day to day-of-year
      month = self.get_month_int( month )
      day_of_year = sum( calendar.monthrange( 2024, m )[1] for m in range( 1, month ) ) + day

      # Month start temperatures (°C)
      month_base = {
         1: -1.0,   # January
         2:  0.0,   # February
         3:  5.0,   # March
         4: 12.0,   # April
         5: 18.0,   # May
         6: 23.0,   # June
         7: 26.0,   # July
         8: 25.0,   # August
         9: 21.0,   # September
         10:15.0,  # October
         11: 9.0,  # November
         12: 2.0   # December
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
      if month == 'JAN':
         return 1
      elif month == 'FEB':
         return 2
      elif month == 'MAR':
         return 3
      elif month == 'APR':
         return 4
      elif month == 'MAY':
         return 5
      elif month == 'JUN':
         return 6
      elif month == 'JUL':
         return 7
      elif month == 'AUG':
         return 8
      elif month == 'SEP':
         return 9
      elif month == 'OCT':
         return 10
      elif month == 'NOV':
         return 11
      elif month == 'DEC':
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
      