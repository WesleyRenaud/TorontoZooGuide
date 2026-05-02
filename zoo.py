from datetime import date, timedelta
import calendar
import math

class Animal:
   def __init__( self, species, latin_name=None, general_viewing_tips=None, seasonal_viewing_tips=None, identification=None,
                 habitat_and_range=None, diet_and_feeding=None, behaviour_and_life_cycle=None, adaptations=None,
                 reproduction_and_life_cycle=None, animals_at_the_zoo=None, exhibit=None, seasonal_viewing_summary=None,
                 seasonal_viewing_information=None, off_display_message=None, enclosure_type=None, x_coord=None,y_coord=None,
                 likelihood=None, has_limited_viewing_schedule=None, limited_viewing_message=None, has_viewing_alert=None,
                 viewing_alert_message=None ):
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
      self.off_display_message = off_display_message
      self.enclosure_type = enclosure_type
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.likelihood = likelihood
      self.has_limited_viewing_schedule = has_limited_viewing_schedule
      self.limited_viewing_message = limited_viewing_message
      self.has_viewing_alert = has_viewing_alert
      self.viewing_alert_message = viewing_alert_message


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
         'off_display_message': self.off_display_message,
         'enclosure_type': self.enclosure_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'likelihood': self.likelihood,
         'has_limited_viewing_schedule': ZooUtil.as_boolean( self.has_limited_viewing_schedule ),
         'limited_viewing_message': self.limited_viewing_message,
         'has_viewing_alert': ZooUtil.as_boolean( self.has_viewing_alert ),
         'viewing_alert_message': self.viewing_alert_message
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
   def __init__( self, name, location, sub_location, description=None, menu_link=None, x_coord=None, y_coord=None, is_closed=None,
                 closed_message=None, likelihood=None ):
      self.name = name
      self.location = location
      self.sub_location = sub_location
      self.description = description
      self.menu_link = menu_link
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'sub_location': self.sub_location,
         'description': self.description,
         'menu_link': self.menu_link,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood
      }


class Restroom:
   def __init__(
         self,
         title,
         x_coord=None,
         y_coord=None,
         is_closed=None,
         closed_message=None,
         has_alert=None,
         alert_message=None ):
      self.title = title
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.has_alert = has_alert
      self.alert_message = alert_message


   def to_dict( self ):
      return {
         'title': self.title,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'has_alert': ZooUtil.as_boolean( self.has_alert ),
         'alert_message': self.alert_message
      }


class GiftShop:
   def __init__( self, name, location, description=None, x_coord=None, y_coord=None, is_closed=None, closed_message=None,
                 likelihood=None ):
      self.name = name
      self.location = location
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood,
      }


class Attraction:
   def __init__( self, name, free_with_admission, description=None, info_link=None, hyperlink_text=None, x_coord=None, y_coord=None,
                 is_closed=False, closed_message=None, likelihood=None ):
      self.name = name
      self.free_with_admission = free_with_admission
      self.description = description
      self.info_link = info_link
      self.hyperlink_text = hyperlink_text
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'name': self.name,
         'free_with_admission': ZooUtil.as_boolean( self.free_with_admission ),
         'description': self.description,
         'info_link': self.info_link,
         'hyperlink_text': self.hyperlink_text,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood
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


class GuardiansTalk:
   def __init__( self, name, location, x_coord, y_coord, time_of_day=None, is_available=True, unavailable_message=None ):
      self.name = name
      self.location = location
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.time_of_day = time_of_day
      self.is_available = is_available
      self.unavailable_message = unavailable_message


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'time_of_day': self.time_of_day,
         'is_available': ZooUtil.as_boolean( self.is_available ),
         'unavailable_message': self.unavailable_message
      }


class WildEncounter:
   def __init__( self, name, meeting_spot, link, time_of_day=None, x_coord=None, y_coord=None, is_available=True, unavailable_message=None ):
      self.name = name
      self.meeting_spot = meeting_spot
      self.link = link
      self.time_of_day = time_of_day
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_available = is_available
      self.unavailable_message = unavailable_message


   def to_dict( self ):
      return {
         'name': self.name,
         'meeting_spot': self.meeting_spot,
         'link': self.link,
         'time_of_day': self.time_of_day,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_available': ZooUtil.as_boolean( self.is_available ),
         'unavailable_message': self.unavailable_message
      }


class DrinkingFountain:
   def __init__(
         self,
         x_coord,
         y_coord,
         is_closed=False,
         closed_message=None,
         likelihood=None ):
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood
      }


class Defibrillator:
   def __init__( self, x_coord, y_coord ):
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }


class EmergencyIntercom:
   def __init__( self, x_coord, y_coord ):
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }


class Itinerary:
   def __init__( self, date, animals=[], attractions=[], guardians_talks=[], wild_encounters=[] ):
      self.date = date
      self.animals = animals
      self.attractions = attractions
      self.guardians_talks = guardians_talks
      self.wild_encounters = wild_encounters


   def to_dict( self ):
      return {
         'date': self.date,
         'animals': [
            self._to_dict_with_type(a, 'animal') for a in self.animals
         ],
         'attractions': [
            self._to_dict_with_type(a, 'attraction') for a in self.attractions
         ],
         'guardians_talks': [
            self._to_dict_with_type(g, 'guardiansTalk') for g in self.guardians_talks
         ],
         'wild_encounters': [
            self._to_dict_with_type(w, 'wildEncounter') for w in self.wild_encounters
         ]
      }

   def _to_dict_with_type( self, obj, fallback_type ):
      if hasattr(obj, 'to_dict'):
         d = obj.to_dict()
      else:
         d = dict(obj) if isinstance(obj, dict) else {}

      d[ 'type' ] = d.get('type', fallback_type)
      return d


class ZooUtil:
   @staticmethod
   def as_boolean( value ):
      if isinstance( value, bool ):
         return value

      if isinstance( value, int ):
         return value != 0

      return False


   @staticmethod
   def get_average_temperature( month, day ):
      # Convert month/day to day-of-year
      month = ZooUtil.normalize_month( month )
      day_of_year = sum( calendar.monthrange( 2024, m )[ 1 ] for m in range( 1, month ) ) + day

      # Month start temperatures (°C)
      month_base = {
         1: -5.0,   # January
         2: -4.0,   # February
         3:  1.0,   # March
         4:  8.0,   # April
         5: 14.0,   # May
         6: 22.0,   # June
         7: 26.0,   # July
         8: 25.0,   # August
         9: 22.0,   # September
         10: 20.0,  # October
         11: 10.0,  # November
         12: 1.0    # December
      }

      # Compute start-of-month day-of-year mapping
      month_start_doy = []
      cumulative = 1
      for m in range( 1, 13 ):
         month_start_doy.append( (cumulative, month_base[ m ]) )
         cumulative += calendar.monthrange( 2024, m )[ 1 ]

      # Find which interval the day-of-year falls into
      for i in range( len( month_start_doy ) - 1 ):
         start_day, start_temp = month_start_doy[ i ]
         end_day, end_temp = month_start_doy[ i + 1 ]
         if start_day <= day_of_year < end_day:
            progress = (day_of_year - start_day) / (end_day - start_day)
            temp = start_temp + (end_temp - start_temp) * progress
            return round( temp, 1 )

      # If day is in December
      temp = month_start_doy[ -1 ][ 1 ]
      return round( temp, 1 )


   @staticmethod
   def normalize_month( month ):
      if not month:
         return None

      if isinstance( month, int ):
         if 1 <= month <= 12:
            return month
         return None

      m = str( month ).strip()

      if m in ( 'JAN', 'Jan' ) or m.startswith( 'Jan' ) or m.startswith( 'JAN' ):
         return 1
      elif m in ( 'FEB', 'Feb' ) or m.startswith( 'Feb' ) or m.startswith( 'FEB' ):
         return 2
      elif m in ( 'MAR', 'Mar' ) or m.startswith( 'Mar' ) or m.startswith( 'MAR' ):
         return 3
      elif m in ( 'APR', 'Apr' ) or m.startswith( 'Apr' ) or m.startswith( 'APR' ):
         return 4
      elif m in ( 'MAY', 'May' ) or m.startswith( 'May' ) or m.startswith( 'MAY' ):
         return 5
      elif m in ( 'JUN', 'Jun' ) or m.startswith( 'Jun' ) or m.startswith( 'JUN' ):
         return 6
      elif m in ( 'JUL', 'Jul' ) or m.startswith( 'Jul' ) or m.startswith( 'JUL' ):
         return 7
      elif m in ( 'AUG', 'Aug' ) or m.startswith( 'Aug' ) or m.startswith( 'AUG' ):
         return 8
      elif m in ( 'SEP', 'Sep' ) or m.startswith( 'Sep' ) or m.startswith( 'SEP' ):
         return 9
      elif m in ( 'OCT', 'Oct' ) or m.startswith( 'Oct' ) or m.startswith( 'OCT' ):
         return 10
      elif m in ( 'NOV', 'Nov' ) or m.startswith( 'Nov' ) or m.startswith( 'NOV' ):
         return 11
      elif m in ( 'DEC', 'Dec' ) or m.startswith( 'Dec' ) or m.startswith( 'DEC' ):
         return 12

      return None


   @staticmethod
   def get_month_abbreviation( month ):
      month_map = {
         1: 'Jan',
         2: 'Feb',
         3: 'Mar',
         4: 'Apr',
         5: 'May',
         6: 'Jun',
         7: 'Jul',
         8: 'Aug',
         9: 'Sep',
         10: 'Oct',
         11: 'Nov',
         12: 'Dec',
      }

      full_name_map = {
         'january': 'Jan',
         'february': 'Feb',
         'march': 'Mar',
         'april': 'Apr',
         'may': 'May',
         'june': 'Jun',
         'july': 'Jul',
         'august': 'Aug',
         'september': 'Sep',
         'october': 'Oct',
         'november': 'Nov',
         'december': 'Dec',
      }

      if isinstance( month, int ):
         if month not in month_map:
            raise ValueError( f'Invalid month: {month}' )
         return month_map[ month ]

      if isinstance( month, str ):
         month = month.strip()

         if month.isdigit():
            month_num = int( month )
            if month_num not in month_map:
               raise ValueError( f'Invalid month: {month}' )
            return month_map[ month_num ]

         lowered = month.lower()

         if lowered in full_name_map:
            return full_name_map[ lowered ]

         abbrev = month[ :3 ].title()
         if abbrev in month_map.values():
            return abbrev

      raise ValueError( f'Invalid month: {month}' )


   @staticmethod
   def get_day_of_year( month, day ):
      month_index = {
         "JAN":0, "FEB":1, "MAR":2, "APR":3, "MAY":4, "JUN":5,
         "JUL":6, "AUG":7, "SEP":8, "OCT":9, "NOV":10, "DEC":11
      }

      days_in_month = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

      doy = sum( days_in_month[ :month_index[ month ] ] )
      return doy + (day - 1)


   @staticmethod
   def get_next_month( month ):
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


   @staticmethod
   def get_number_of_days_in_month( month ):
      if month in ('JAN', 'Jan', 'MAR', 'Mar', 'MAY', 'May', 'JUL', 'Jul', 'AUG', 'Aug', 'OCT', 'Oct', 'DEC', 'Dec'):
         return 31
      elif month in ('APR', 'Apr', 'JUN', 'Jun', 'SEP', 'Sep', 'NOV', 'Nov'):
         return 30
      elif month in ('FEB', 'Feb'):
         return 28


   # Returns probability (between 0 and 1) that temperature is >= min_temperature, assuming a normal distribution N(mu, sigma)
   @staticmethod
   def get_temperature_probability( mu, sigma, min_temperature ):
      z = (min_temperature - mu) / sigma

      # Standard normal CDF via error function
      cdf = 0.5 * (1 + math.erf( z / math.sqrt( 2) ) )

      return round( 1.0 - cdf, 3 )


   @staticmethod
   def is_peak_season_month( month ):
      month = ZooUtil.normalize_month( month )

      if month >= 5 and month <= 10:
         return True

      return False


   @staticmethod
   def is_holiday( d ):
      year = d.year

      holidays = {
         date( year, 1, 1 ),               # New Year's Day
         ZooUtil.get_family_day( year ),
         ZooUtil.get_good_friday( year ),
         ZooUtil.get_victoria_day( year ),
         date( year, 7, 1 ),               # Canada Day
         ZooUtil.get_civic_holiday( year ),
         ZooUtil.get_labour_day( year ),
         ZooUtil.get_thanksgiving( year ),
         date( year, 12, 25 )              # Christmas Day
      }

      return d in holidays


   @staticmethod
   def get_family_day( year ):
      d = date( year, 2, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=14 )


   @staticmethod
   def get_good_friday( year ):
      easter = ZooUtil.get_easter_date( year )
      return easter - timedelta( days=2 )


   @staticmethod
   def get_easter_date( year ):
      a = year % 19
      b = year // 100
      c = year % 100
      d = b // 4
      e = b % 4
      f = ( b + 8 ) // 25
      g = ( b - f + 1 ) // 3
      h = ( 19 * a + b - d - g + 15 ) % 30
      i = c // 4
      k = c % 4
      weekday_offset = ( 32 + 2 * e + 2 * i - h - k ) % 7
      m = ( a + 11 * h + 22 * weekday_offset ) // 451
      month = ( h + weekday_offset - 7 * m + 114 ) // 31
      day = ( ( h + weekday_offset - 7 * m + 114 ) % 31 ) + 1

      return date( year, month, day )


   @staticmethod
   def get_victoria_day( year ):
      d = date( year, 5, 24 )

      while d.weekday() != 0:
         d -= timedelta( days=1 )

      return d


   @staticmethod
   def get_civic_holiday( year ):
      d = date( year, 8, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_labour_day( year ):
      d = date( year, 9, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d


   @staticmethod
   def get_thanksgiving( year ):
      d = date( year, 10, 1 )

      while d.weekday() != 0:
         d += timedelta( days=1 )

      return d + timedelta( days=7 )
