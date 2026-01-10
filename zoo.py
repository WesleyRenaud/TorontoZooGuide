import calendar, math

class Animal:
   def __init__( self, species, location, exhibit_type, likelihood=None ):
      self.species = species
      self.location = location
      self.exhibit_type = exhibit_type
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'species': self.species,
         'location': self.location,
         'exhibit_type': self.exhibit_type,
         'likelihood': self.likelihood
      }
   

class Zoo_Util:
   def species_viewable_inside_and_outside( self, species ):
      species_viewable_inside_and_outside =\
      [
         'African penguin', 'Golden lion tamarin', 'Southern hairy-nosed wombat', 'Sumatran orangutan', 'Two-toed sloth',
         'Western lowland gorilla', 'White-faced saki'
      ]
      
      if species in species_viewable_inside_and_outside:
         return True
      else:
         return False
      

   # Returns probability (0.0 – 1.0) that snow is on the ground in Toronto on the given month & day
   def snow_probability( self, month, day ):
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
   

   def get_estimated_temp( self, month, day ):
      TORONTO_MONTHLY_AVG = {
         "JAN": -4,
         "FEB": -3,
         "MAR":  2,
         "APR":  8,
         "MAY": 14,
         "JUN": 19,
         "JUL": 22,
         "AUG": 21,
         "SEP": 17,
         "OCT": 11,
         "NOV":  5,
         "DEC": -1
      }

      month = month.upper()

      avg_month_temp = TORONTO_MONTHLY_AVG[month]
      day_of_year = self.get_day_of_year( month, day )

      # Peak summer ≈ July 24 (Toronto warmest day)
      phase_shift = 205
      radians = 2 * math.pi * ( day_of_year - phase_shift ) / 365

      # Toronto seasonal swing (°C)
      seasonal_swing = 14

      # Toronto annual mean temp
      annual_mean = 9

      # Smooth seasonal curve
      seasonal_temp = annual_mean + seasonal_swing * math.sin( radians )

      # Blend monthly climate normals with smooth curve
      temp = seasonal_temp * 0.6 + avg_month_temp * 0.4

      return round( temp, 1 )
   

   def get_day_of_year(self, month, day ):
      month_index = {
         "JAN":0, "FEB":1, "MAR":2, "APR":3, "MAY":4, "JUN":5,
         "JUL":6, "AUG":7, "SEP":8, "OCT":9, "NOV":10, "DEC":11
      }

      days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

      doy = sum( days_in_month[:month_index[month]] )
      return doy + (day - 1)
      