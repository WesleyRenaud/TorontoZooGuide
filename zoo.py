import calendar, math

class Animal:
   def __init__( self, species, latin_name=None, general_viewing_tips=None, seasonal_viewing_tips=None, identification=None,
                 habitat_and_range=None, diet_and_feeding=None, behaviour_and_life_cycle=None, adaptations=None,
                 reproduction_and_life_cycle=None, animals_at_the_zoo=None, exhibit=None, seasonal_viewing_summary=None,
                 seasonal_viewing_information=None, seasonally_off_display_message=None, enclosure_type=None, x_coord=None,y_coord=None,
                 likelihood=None ):
      self.species = species
      self.latin_name = latin_name
      self.general_viewing_tips = general_viewing_tips
      self.seasonal_viewing_tips = seasonal_viewing_tips
      self.identification = identification
      self.habitat_and_range = habitat_and_range
      self.diet_and_feeding = diet_and_feeding
      self.behaviour_and_life_cycle = behaviour_and_life_cycle
      self.adaptations = adaptations
      self.reproduction_and_life_cycle = reproduction_and_life_cycle
      self.animals_at_the_zoo = animals_at_the_zoo
      self.exhibit = exhibit
      self.seasonal_viewing_summary = seasonal_viewing_summary
      self.seasonal_viewing_information = seasonal_viewing_information
      self.seasonally_off_display_message = seasonally_off_display_message
      self.enclosure_type = enclosure_type
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'species': self.species,
         'latin_name': self.latin_name,
         'general_viewing_tips': self.general_viewing_tips,
         'seasonal_viewing_tips': self.seasonal_viewing_tips,
         'identification': self.identification,
         'habitat_and_range': self.habitat_and_range,
         'diet_and_feeding': self.diet_and_feeding,
         'behaviour_and_life_cycle': self.behaviour_and_life_cycle,
         'adaptations': self.adaptations,
         'reproduction_and_life_cycle': self.reproduction_and_life_cycle,
         'animals_at_the_zoo': self.animals_at_the_zoo,
         'exhibit': self.exhibit,
         'seasonal_viewing_summary': self.seasonal_viewing_summary,
         'seasonal_viewing_information': self.seasonal_viewing_information,
         'seasonally_off_display_message': self.seasonally_off_display_message,
         'enclosure_type': self.enclosure_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'likelihood': self.likelihood
      }
   

class Pavilion:
   def __init__( self, name, region, description=None, x_coord=None, y_coord=None ):
      self.name = name
      self.region = region
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'region': self.region,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   

class Restaurant:
   def __init__( self, name, location, sub_location, seasonal_schedule=None, description=None, menu_link=None, x_coord=None,
                 y_coord=None ):
      self.name = name
      self.location = location
      self.sub_location = sub_location
      self.seasonal_schedule = seasonal_schedule
      self.description = description
      self.menu_link = menu_link
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'sub_location': self.sub_location,
         'seasonal_schedule': self.seasonal_schedule,
         'description': self.description,
         'menu_link': self.menu_link,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   

class Restroom:
   def __init__( self, title, x_coord=None, y_coord=None ):
      self.title = title
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'title': self.title,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   

class GiftShop:
   def __init__( self, name, location, seasonal_schedule=None, description=None, x_coord=None, y_coord=None ):
      self.name = name
      self.location = location
      self.seasonal_schedule = seasonal_schedule
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'seasonal_schedule': self.seasonal_schedule,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   

class Attraction:
   def __init__( self, name, free_with_admission, seasonal_schedule=None, description=None, info_link=None, hyperlink_text=None,
                 x_coord=None, y_coord=None ):
      self.name = name
      self.free_with_admission = free_with_admission
      self.seasonal_schedule = seasonal_schedule
      self.description = description
      self.info_link = info_link
      self.hyperlink_text = hyperlink_text
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'free_with_admission': self.free_with_admission,
         'seasonal_schedule': self.seasonal_schedule,
         'description': self.description,
         'info_link': self.info_link,
         'hyperlink_text': self.hyperlink_text,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   

class ZoomobileStation:
   def __init__( self, name, description=None, x_coord=None, y_coord=None ):
      self.name = name
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   

class ZoomobileRouteMarker:
   def __init__( self, route_type, x_coord, y_coord ):
      self.route_type = route_type
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'route_type': self.route_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   
   
class MeetTheGuardiansTalk:
   def __init__( self, name, location, x_coord, y_coord, day_of_week=None, time_of_day=None ):
      self.name = name
      self.location = location
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.day_of_week = day_of_week
      self.time_of_day = time_of_day


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'day_of_week': self.day_of_week,
         'time_of_day': self.time_of_day
      }


class WildEncounterMeetingSpot:
   def __init__( self, name, x_coord, y_coord ):
      self.name = name
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
   

class WildEncounter:
   def __init__( self, name, meeting_spot, link, day_of_week=None, time_of_day=None, x_coord=None, y_coord=None ):
      self.name = name
      self.meeting_spot = meeting_spot
      self.link = link
      self.day_of_week = day_of_week
      self.time_of_day = time_of_day
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'meeting_spot': self.meeting_spot,
         'link': self.link,
         'day_of_week': self.day_of_week,
         'time_of_day': self.time_of_day,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
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


   def get_snow_likelihood( self, month, day ):
      month = self.get_month_int( month )

      MONTH_SNOW_BASE = {
         1: 0.90,
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
      progress = (day - 1) / (days_in_month - 1)

      if month == 12:
         base *= 0.6 + 0.4 * progress

      elif month == 3:
         # Snow usually persists through early March,
         # then melts quickly in the second half.
         melt_progress = max( 0, (progress - 0.35) / 0.65 )
         base *= 1.0 - 0.6 * melt_progress

      elif month == 11:
         base *= 0.3 + 0.7 * progress

      elif month == 4:
         base *= 1.0 - progress

      return max( 0.0, min( 1.0, round( base, 2 ) ) )


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
   

   def is_peak_season_month( self, month ):
      month = self.get_month_int( month )

      if month >= 5 and month <= 10:
         return True
      
      return False
