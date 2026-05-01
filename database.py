import sqlite3
import zoo
from datetime import date, datetime, timedelta


################################################################################

class Database():
   def __init__( self, db_path='animals.db' ):
      self.conn = sqlite3.connect( db_path )
      self.conn.row_factory = sqlite3.Row


   def close( self ):
      if self.conn is None:
         return

      self.conn.close()
      self.conn = None


   # Returns all animals which may be viewable in the given month with their likelihoods (0 to 100)
   def get_animals_viewable_on_day(
         self,
         month,
         day,
         temp=None,
         include_off_display_animals=False,
         threshold=0,
         exhibits_to_include=None ):

      exhibits_to_include = exhibits_to_include or []

      month = zoo.ZooUtil.get_month_abbreviation( month )
      normalized_month = zoo.ZooUtil.normalize_month( month=month )
      normalized_day = int( day )
      cur = self.conn.cursor()

      if temp is None:
         temp = zoo.ZooUtil.get_average_temperature( month=month, day=day )
         sigma = 3
      else:
         sigma = 2

      target_date = date(
         datetime.now().year,
         normalized_month,
         normalized_day )

      data = cur.execute(
         """   SELECT
                  a.SPECIES,
                  a.LATIN_NAME,
                  a.MIN_TEMPERATURE,
                  a.GENERAL_VIEWING_TIPS,
                  a.SEASONAL_VIEWING_TIPS,
                  a.IDENTIFICATION,
                  a.HABITAT_AND_RANGE,
                  a.DIET_AND_FEEDING,
                  a.BEHAVIOUR_AND_SOCIAL_LIFE,
                  a.ADAPTATIONS,
                  a.REPRODUCTION_AND_LIFE_CYCLE,
                  a.ANIMALS_AT_THE_ZOO,
                  e.EXHIBIT,
                  e.SEASONAL_VIEWING_SUMMARY,
                  e.SEASONAL_VIEWING_INFORMATION,
                  v.ENCLOSURE_TYPE,
                  v.SEASONALLY_OFF_DISPLAY_MESSAGE,
                  v.X_COORD,
                  v.Y_COORD,
                  s.IS_OFF_DISPLAY,
                  s.OFF_DISPLAY_MESSAGE,
                  s.OFF_DISPLAY_START,
                  s.OFF_DISPLAY_END,
                  vs.SCHEDULE_START_DATE,
                  vs.SCHEDULE_END_DATE,
                  vs.DAILY_START_TIME,
                  vs.DAILY_END_TIME,
                  vs.VIEWING_MESSAGE,
                  va.ALERT_MESSAGE,
                  va.ALERT_START_DATE,
                  va.ALERT_END_DATE,
                  es.IS_CLOSED,
                  es.CLOSED_MESSAGE,
                  es.CLOSED_START,
                  es.CLOSED_END,
                  COALESCE( adsvm.VALUE, 1.0 ) AS ANIMAL_DAY_SEASONAL_MULTIPLIER,
                  COALESCE( edsam.VALUE, 1.0 ) AS EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               JOIN EnclosureViewing v
                  ON e.SPECIES = v.SPECIES
                  AND e.EXHIBIT = v.EXHIBIT
               LEFT JOIN AnimalStatus s
                  ON e.SPECIES = s.SPECIES
                  AND e.EXHIBIT = s.EXHIBIT
               LEFT JOIN AnimalVisibilitySchedule vs
                  ON e.SPECIES = vs.SPECIES
                  AND e.EXHIBIT = vs.EXHIBIT
               LEFT JOIN AnimalViewingAlert va
                  ON e.SPECIES = va.SPECIES
                  AND e.EXHIBIT = va.EXHIBIT
               LEFT JOIN ExhibitStatus es
                  ON e.EXHIBIT = es.EXHIBIT
               LEFT JOIN AnimalDaySeasonalViewabilityMultiplier adsvm
                  ON e.SPECIES = adsvm.SPECIES
                  AND e.EXHIBIT = adsvm.EXHIBIT
                  AND adsvm.MONTH = ?
                  AND adsvm.DAY = ?
               LEFT JOIN ExhibitDaySeasonalAvailabilityMultiplier edsam
                  ON e.EXHIBIT = edsam.EXHIBIT
                  AND edsam.MONTH = ?
                  AND edsam.DAY = ?;
         """, ( normalized_month, normalized_day, normalized_month, normalized_day ) )

      animal_data = data.fetchall()
      animals = []

      exhibits_filter = set(
         exhibit.strip() for exhibit in exhibits_to_include
         if isinstance( exhibit, str ) and exhibit.strip() != '' )

      for animal in animal_data:
         species = animal[ 'SPECIES' ]
         exhibit = animal[ 'EXHIBIT' ]

         if exhibits_filter and exhibit not in exhibits_filter:
            continue

         min_temperature = animal[ 'MIN_TEMPERATURE' ]
         enclosure_type = animal[ 'ENCLOSURE_TYPE' ]
         seasonally_off_display_message = animal[ 'SEASONALLY_OFF_DISPLAY_MESSAGE' ]
         animal_day_seasonal_multiplier = animal[ 'ANIMAL_DAY_SEASONAL_MULTIPLIER' ]
         exhibit_day_seasonal_availability_multiplier = animal[ 'EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER' ]

         is_off_display, off_display_message = self.get_active_off_display_status(
            animal=animal,
            target_date=target_date )

         has_limited_viewing_schedule, limited_viewing_message = self.get_active_limited_viewing_status(
            animal=animal,
            target_date=target_date )

         has_viewing_alert, viewing_alert_message = self.get_active_viewing_alert_status(
            animal=animal,
            target_date=target_date )

         exhibit_status, exhibit_closed_message = self.get_active_exhibit_status(
            animal=animal,
            target_date=target_date )

         if is_off_display or exhibit_status == 'closed':
            likelihood = 0
         else:
            applied_exhibit_day_availability_multiplier = 1.0

            if exhibit_status == 'unknown':
               applied_exhibit_day_availability_multiplier = exhibit_day_seasonal_availability_multiplier

            likelihood = self.calculate_animal_likelihood(
               temp=temp,
               sigma=sigma,
               enclosure_type=enclosure_type,
               min_temperature=min_temperature,
               day_seasonal_multiplier=animal_day_seasonal_multiplier,
               exhibit_day_seasonal_availability_multiplier=applied_exhibit_day_availability_multiplier )

         should_include = (
            ( likelihood > threshold )
            or ( include_off_display_animals and likelihood == 0 )
         )

         if should_include:
            display_message = None

            if is_off_display:
               display_message = off_display_message
            elif exhibit_status == 'closed':
               display_message = exhibit_closed_message
            elif likelihood == 0:
               if exhibit_status == 'unknown' and exhibit_day_seasonal_availability_multiplier == 0:
                  display_message = f'The { exhibit } is most likely closed on this day.'
               elif seasonally_off_display_message:
                  display_message = seasonally_off_display_message
               else:
                  display_message = f'The { species } is most likely off display on this day.'

            animals.append(
               zoo.Animal(
                  species=species,
                  latin_name=animal[ 'LATIN_NAME' ],
                  general_viewing_tips=animal[ 'GENERAL_VIEWING_TIPS' ],
                  seasonal_viewing_tips=animal[ 'SEASONAL_VIEWING_TIPS' ],
                  identification=animal[ 'IDENTIFICATION' ],
                  habitat_and_range=animal[ 'HABITAT_AND_RANGE' ],
                  diet_and_feeding=animal[ 'DIET_AND_FEEDING' ],
                  behaviour_and_life_cycle=animal[ 'BEHAVIOUR_AND_SOCIAL_LIFE' ],
                  adaptations=animal[ 'ADAPTATIONS' ],
                  reproduction_and_life_cycle=animal[ 'REPRODUCTION_AND_LIFE_CYCLE' ],
                  animals_at_the_zoo=animal[ 'ANIMALS_AT_THE_ZOO' ],
                  exhibit=exhibit,
                  seasonal_viewing_summary=animal[ 'SEASONAL_VIEWING_SUMMARY' ],
                  seasonal_viewing_information=animal[ 'SEASONAL_VIEWING_INFORMATION' ],
                  off_display_message=display_message,
                  enclosure_type=enclosure_type,
                  x_coord=animal[ 'X_COORD' ],
                  y_coord=animal[ 'Y_COORD' ],
                  likelihood=likelihood,
                  has_limited_viewing_schedule=has_limited_viewing_schedule,
                  limited_viewing_message=limited_viewing_message,
                  has_viewing_alert=has_viewing_alert,
                  viewing_alert_message=viewing_alert_message ) )

      cur.close()

      return animals


   def get_active_off_display_status( self, animal, target_date ):
      stored_is_off_display = bool( animal[ 'IS_OFF_DISPLAY' ] ) if animal[ 'IS_OFF_DISPLAY' ] != None else False

      if not stored_is_off_display:
         return False, None

      off_display_message = animal[ 'OFF_DISPLAY_MESSAGE' ]
      off_display_start = animal[ 'OFF_DISPLAY_START' ]
      off_display_end = animal[ 'OFF_DISPLAY_END' ]

      is_off_display = self.is_date_in_range(
         target_date=target_date,
         start_date_value=off_display_start,
         end_date_value=off_display_end )

      if is_off_display:
         return True, off_display_message

      return False, None


   def get_active_limited_viewing_status( self, animal, target_date ):
      schedule_start_date = animal[ 'SCHEDULE_START_DATE' ]
      schedule_end_date = animal[ 'SCHEDULE_END_DATE' ]
      daily_start_time = animal[ 'DAILY_START_TIME' ]
      daily_end_time = animal[ 'DAILY_END_TIME' ]
      viewing_message = animal[ 'VIEWING_MESSAGE' ]

      if daily_start_time == None or daily_end_time == None:
         return False, None

      is_active = self.is_date_in_range( target_date=target_date, start_date_value=schedule_start_date, end_date_value=schedule_end_date )

      if is_active:
         return True, viewing_message

      return False, None


   def get_active_viewing_alert_status( self, animal, target_date ):
      alert_message = animal[ 'ALERT_MESSAGE' ]
      alert_start_date = animal[ 'ALERT_START_DATE' ]
      alert_end_date = animal[ 'ALERT_END_DATE' ]

      if alert_message == None:
         return False, None

      is_active = self.is_date_in_range( target_date=target_date, start_date_value=alert_start_date, end_date_value=alert_end_date )

      if is_active:
         return True, alert_message

      return False, None


   def get_active_exhibit_status( self, animal, target_date ):
      if animal[ 'IS_CLOSED' ] == None:
         return 'unknown', None

      start_date = animal[ 'CLOSED_START' ]
      end_date = animal[ 'CLOSED_END' ]

      is_active = self.is_date_in_range(
         target_date=target_date,
         start_date_value=start_date,
         end_date_value=end_date )

      if not is_active:
         return 'unknown', None

      if bool( animal[ 'IS_CLOSED' ] ):
         return 'closed', animal[ 'CLOSED_MESSAGE' ]

      return 'open', None


   def calculate_animal_likelihood(
         self,
         temp,
         sigma,
         enclosure_type,
         min_temperature,
         day_seasonal_multiplier,
         exhibit_day_seasonal_availability_multiplier=1.0 ):
      normalized_enclosure_type = str( enclosure_type ).strip().lower() if enclosure_type is not None else None

      if normalized_enclosure_type == 'indoor':
         temperature_likelihood = 1.0
         animal_seasonal_multiplier = 1.0
      else:
         if min_temperature is None:
            temperature_likelihood = 1.0
         else:
            temperature_likelihood = zoo.ZooUtil.get_temperature_probability(
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


   def is_date_in_range( self, target_date, start_date_value, end_date_value ):
      start_ok = True
      end_ok = True

      if start_date_value != None:
         start_date = self.parse_date_value( value=start_date_value )
         start_ok = target_date >= start_date

      if end_date_value != None:
         end_date = self.parse_date_value( value=end_date_value )
         end_ok = target_date <= end_date

      return start_ok and end_ok


   def parse_datetime_value( self, value ):
      if value == None:
         return None

      for fmt in (
         '%Y-%m-%d %I:%M %p',
         '%Y-%m-%d %H:%M:%S',
         '%Y-%m-%d %H:%M'
      ):

         try:
            return datetime.strptime( value, fmt )
         except ValueError:
            pass

      raise ValueError( f'Unsupported datetime format: { value }' )


   def parse_date_value( self, value ):
      if value == None:
         return None

      if isinstance( value, date ) and not isinstance( value, datetime ):
         return value

      if isinstance( value, datetime ):
         return value.date()

      value = str( value ).strip()

      try:
         return date.fromisoformat( value )
      except ValueError:
         pass

      date_part = value.split( ' ' )[ 0 ]

      try:
         return date.fromisoformat( date_part )
      except ValueError:
         pass

      raise ValueError( f'Unsupported date format: { value }' )


   def get_exhibits_in_region( self, region ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  e.NAME
               FROM Exhibit e
               WHERE e.REGION = ?;
         """, ( region, ) )

      exhibits = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return exhibits


   def get_regions( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  r.NAME AS REGION_NAME,
                  e.NAME AS EXHIBIT_NAME
               FROM Region r
               LEFT JOIN Exhibit e
                  ON e.REGION = r.NAME
               ORDER BY r.NAME, e.NAME;
         """ )

      rows = data.fetchall()
      regions = []
      current_region = None

      for row in rows:
         region_name = row[ 'REGION_NAME' ]
         exhibit_name = row[ 'EXHIBIT_NAME' ]

         if current_region == None or current_region[ 'name' ] != region_name:
            current_region = {
               'name': region_name,
               'exhibits': [],
            }
            regions.append( current_region )

         if exhibit_name != None:
            current_region[ 'exhibits' ].append( exhibit_name )

      cur.close()

      regions = [
         region for region in regions
         if len( region[ 'exhibits' ] ) > 0
      ]

      return [
         {
            'name': region[ 'name' ],
            'hasExhibits': not (
               len( region[ 'exhibits' ] ) == 1
               and region[ 'exhibits' ][ 0 ] == region[ 'name' ]
            ),
         }
         for region in regions
      ]


   def get_animals_in_exhibit( self, exhibit ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  a.SPECIES
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               WHERE e.EXHIBIT = ?
         """, ( exhibit, ) )

      animals = [ row[ 0 ] for row in data.fetchall() ]

      cur.close()

      return animals


   def get_animal_information( self, species ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  a.LATIN_NAME,
                  a.GENERAL_VIEWING_TIPS,
                  a.SEASONAL_VIEWING_TIPS,
                  a.IDENTIFICATION,
                  a.HABITAT_AND_RANGE,
                  a.DIET_AND_FEEDING,
                  a.BEHAVIOUR_AND_SOCIAL_LIFE,
                  a.ADAPTATIONS,
                  a.REPRODUCTION_AND_LIFE_CYCLE,
                  a.ANIMALS_AT_THE_ZOO,
                  e.EXHIBIT,
                  e.SEASONAL_VIEWING_SUMMARY,
                  e.SEASONAL_VIEWING_INFORMATION
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               WHERE a.SPECIES = ?;
         """,
         ( species, ) )

      animal = data.fetchone()

      if animal is None:
         return None

      animal_info = zoo.Animal(
         species = species,
         latin_name = animal[ 'LATIN_NAME' ],
         general_viewing_tips = animal[ 'GENERAL_VIEWING_TIPS' ],
         seasonal_viewing_tips = animal[ 'SEASONAL_VIEWING_TIPS' ],
         identification = animal[ 'IDENTIFICATION' ],
         habitat_and_range = animal[ 'HABITAT_AND_RANGE' ],
         diet_and_feeding = animal[ 'DIET_AND_FEEDING' ],
         behaviour_and_life_cycle = animal[ 'BEHAVIOUR_AND_SOCIAL_LIFE' ],
         adaptations = animal[ 'ADAPTATIONS' ],
         reproduction_and_life_cycle = animal[ 'REPRODUCTION_AND_LIFE_CYCLE' ],
         animals_at_the_zoo = animal[ 'ANIMALS_AT_THE_ZOO' ],
         exhibit = animal[ 'EXHIBIT' ],
         seasonal_viewing_summary = animal[ 'SEASONAL_VIEWING_SUMMARY' ],
         seasonal_viewing_information = animal[ 'SEASONAL_VIEWING_INFORMATION' ] )

      cur.close()

      return animal_info


   def get_pavilions( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  p.NAME,
                  p.REGION,
                  p.DESCRIPTION,
                  p.X_COORD,
                  p.Y_COORD
               FROM Pavilion p;
         """ )

      pavilion_data = data.fetchall()

      pavilions = []

      for pavilion in pavilion_data:
         pavilions.append(
            zoo.Pavilion(
               name=pavilion[ 'NAME' ],
               region=pavilion[ 'REGION' ],
               description=pavilion[ 'DESCRIPTION' ],
               x_coord=pavilion[ 'X_COORD' ],
               y_coord=pavilion[ 'Y_COORD' ] ) )

      cur.close()

      return pavilions


   def get_restaurants( self, month, day, include_closed_restaurants, restaurants_to_include=[] ):
      cur = self.conn.cursor()

      normalized_month = zoo.ZooUtil.normalize_month( month=month )
      normalized_day = int( day )

      target_date = date( datetime.now().year, normalized_month, normalized_day )
      weekday = target_date.weekday()
      is_weekend_or_holiday = (
         weekday >= 5
         or zoo.ZooUtil.is_holiday( d=target_date ) )

      data = cur.execute(
         """   SELECT
                  r.NAME,
                  r.LOCATION,
                  r.SUB_LOCATION,
                  r.DESCRIPTION,
                  r.MENU_LINK,
                  r.X_COORD,
                  r.Y_COORD,
                  COALESCE( rdsam.WEEKDAY_VALUE, 1.0 ) AS RESTAURANT_DAY_SEASONAL_WEEKDAY_MULTIPLIER,
                  COALESCE( rdsam.WEEKEND_HOLIDAY_VALUE, 1.0 ) AS RESTAURANT_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER
               FROM Restaurant r
               LEFT JOIN RestaurantDaySeasonalAvailabilityMultiplier rdsam
                  ON r.NAME = rdsam.RESTAURANT
                  AND rdsam.MONTH = ?
                  AND rdsam.DAY = ?;
         """, ( normalized_month, normalized_day ) )

      restaurant_data = data.fetchall()

      restaurants = []

      for restaurant in restaurant_data:
         name = restaurant[ 'NAME' ]
         likelihood = 100
         closed_message = None
         restaurant_day_seasonal_availability_multiplier = (
            restaurant[ 'RESTAURANT_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ]
            if is_weekend_or_holiday
            else restaurant[ 'RESTAURANT_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ]
         )

         schedule_status, schedule_message = self.get_active_restaurant_schedule_status(
            restaurant_name=name,
            target_date=target_date,
            weekday=weekday )

         if schedule_status == 'closed':
            likelihood = 0
            closed_message = schedule_message
         elif schedule_status == 'unknown':
            likelihood = self.calculate_restaurant_likelihood(
               day_seasonal_availability_multiplier=restaurant_day_seasonal_availability_multiplier )

            if likelihood == 0:
               closed_message = f'The { name } is most likely not open on this day.'

         is_closed = likelihood <= 0

         if include_closed_restaurants or not is_closed or name in restaurants_to_include:
            restaurants.append(
               zoo.Restaurant(
                  name=name,
                  location=restaurant[ 'LOCATION' ],
                  sub_location=restaurant[ 'SUB_LOCATION' ],
                  description=restaurant[ 'DESCRIPTION' ],
                  menu_link=restaurant[ 'MENU_LINK' ],
                  x_coord=restaurant[ 'X_COORD' ],
                  y_coord=restaurant[ 'Y_COORD' ],
                  is_closed=is_closed,
                  closed_message=closed_message,
                  likelihood=likelihood ) )

      cur.close()

      return restaurants


   def get_active_restaurant_schedule_status( self, restaurant_name, target_date, weekday ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.HOLIDAYS_ONLY,
                  s.SCHEDULE_MESSAGE
               FROM RestaurantOpeningSchedule s
               WHERE s.RESTAURANT = ?;
         """, ( restaurant_name, ) )

      schedule_rows = data.fetchall()
      cur.close()

      if len( schedule_rows ) == 0:
         return 'unknown', None

      for schedule in schedule_rows:
         is_active = self.is_date_in_range(
            target_date=target_date,
            start_date_value=schedule[ 'SCHEDULE_START_DATE' ],
            end_date_value=schedule[ 'SCHEDULE_END_DATE' ] )

         if not is_active:
            continue

         is_holiday = zoo.ZooUtil.is_holiday( d=target_date )

         open_on_day = False

         if weekday == 0 and schedule[ 'MONDAY' ]:
            open_on_day = True
         elif weekday == 1 and schedule[ 'TUESDAY' ]:
            open_on_day = True
         elif weekday == 2 and schedule[ 'WEDNESDAY' ]:
            open_on_day = True
         elif weekday == 3 and schedule[ 'THURSDAY' ]:
            open_on_day = True
         elif weekday == 4 and schedule[ 'FRIDAY' ]:
            open_on_day = True
         elif weekday == 5 and schedule[ 'SATURDAY' ]:
            open_on_day = True
         elif weekday == 6 and schedule[ 'SUNDAY' ]:
            open_on_day = True

         if is_holiday and schedule[ 'HOLIDAYS_ONLY' ]:
            open_on_day = True

         if open_on_day:
            return 'open', None

         return 'closed', schedule[ 'SCHEDULE_MESSAGE' ]

      return 'unknown', None


   def calculate_restaurant_likelihood( self, day_seasonal_availability_multiplier ):
      seasonal_multiplier = (
         day_seasonal_availability_multiplier
         if day_seasonal_availability_multiplier is not None
         else 1.0
      )
      likelihood = max( 0.0, min( seasonal_multiplier, 1.0 ) )

      return max( round( likelihood * 100 ), 0 )


   def get_restrooms( self, month=None, day=None, include_closed_restrooms=False ):
      cur = self.conn.cursor()

      if month is not None and day is not None:
         target_date = date(
            datetime.now().year,
            zoo.ZooUtil.normalize_month( month=month ),
            int( day ) )
      else:
         target_date = datetime.now().date()

      data = cur.execute(
         """   SELECT
                  r.TITLE,
                  r.X_COORD,
                  r.Y_COORD,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE,
                  s.CLOSED_START,
                  s.CLOSED_END,
                  a.ALERT_MESSAGE,
                  a.ALERT_START_DATE,
                  a.ALERT_END_DATE
               FROM Restroom r
               LEFT JOIN RestroomStatus s
                  ON s.RESTROOM = r.TITLE
               LEFT JOIN RestroomAlert a
                  ON a.RESTROOM = r.TITLE;
         """ )

      restroom_data = data.fetchall()

      restrooms = []

      for restroom in restroom_data:
         is_closed = False
         closed_message = None
         has_alert = False
         alert_message = None

         if restroom[ 'IS_CLOSED' ] != None:
            status_is_active = self.is_date_in_range(
               target_date=target_date,
               start_date_value=restroom[ 'CLOSED_START' ],
               end_date_value=restroom[ 'CLOSED_END' ] )

            is_closed = bool( restroom[ 'IS_CLOSED' ] ) and status_is_active

            if is_closed:
               closed_message = restroom[ 'CLOSED_MESSAGE' ]

         if restroom[ 'ALERT_MESSAGE' ] != None:
            alert_is_active = self.is_date_in_range(
               target_date=target_date,
               start_date_value=restroom[ 'ALERT_START_DATE' ],
               end_date_value=restroom[ 'ALERT_END_DATE' ] )

            has_alert = alert_is_active

            if has_alert:
               alert_message = restroom[ 'ALERT_MESSAGE' ]

         if is_closed and not include_closed_restrooms:
            continue

         restrooms.append(
            zoo.Restroom(
               title=restroom[ 'TITLE' ],
               x_coord=restroom[ 'X_COORD' ],
               y_coord=restroom[ 'Y_COORD' ],
               is_closed=is_closed,
               closed_message=closed_message,
               has_alert=has_alert,
               alert_message=alert_message ) )

      cur.close()

      return restrooms


   def get_gift_shops( self, month, day, include_closed_gift_shops, gift_shops_to_include=[] ):
      cur = self.conn.cursor()

      normalized_month = zoo.ZooUtil.normalize_month( month )
      normalized_day = int( day )

      target_date = date( datetime.now().year, normalized_month, normalized_day )
      weekday = target_date.weekday()
      is_weekend_or_holiday = (
         weekday >= 5
         or zoo.ZooUtil.is_holiday( d=target_date ) )

      data = cur.execute(
         """   SELECT
                  g.NAME,
                  g.LOCATION,
                  g.DESCRIPTION,
                  g.X_COORD,
                  g.Y_COORD,
                  COALESCE( gdsam.WEEKDAY_VALUE, 1.0 ) AS GIFT_SHOP_DAY_SEASONAL_WEEKDAY_MULTIPLIER,
                  COALESCE( gdsam.WEEKEND_HOLIDAY_VALUE, 1.0 ) AS GIFT_SHOP_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER
               FROM GiftShop g
               LEFT JOIN GiftShopDaySeasonalAvailabilityMultiplier gdsam
                  ON g.NAME = gdsam.GIFT_SHOP
                  AND gdsam.MONTH = ?
                  AND gdsam.DAY = ?;
         """, ( normalized_month, normalized_day ) )

      gift_shop_data = data.fetchall()

      gift_shops = []

      for gift_shop in gift_shop_data:
         name = gift_shop[ 'NAME' ]
         likelihood = 100
         closed_message = None
         gift_shop_day_seasonal_availability_multiplier = (
            gift_shop[ 'GIFT_SHOP_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ]
            if is_weekend_or_holiday
            else gift_shop[ 'GIFT_SHOP_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ]
         )

         schedule_status, schedule_message = self.get_active_gift_shop_schedule_status(
            gift_shop_name=name,
            target_date=target_date,
            weekday=weekday )

         if schedule_status == 'closed':
            likelihood = 0
            closed_message = schedule_message
         elif schedule_status == 'unknown':
            likelihood = self.calculate_gift_shop_likelihood(
               day_seasonal_availability_multiplier=gift_shop_day_seasonal_availability_multiplier )

            if likelihood == 0:
               closed_message = f'The { name } is most likely not open on this day.'

         is_closed = likelihood <= 0

         if include_closed_gift_shops or not is_closed or name in gift_shops_to_include:
            gift_shops.append(
               zoo.GiftShop(
                  name=name,
                  location=gift_shop[ 'LOCATION' ],
                  description=gift_shop[ 'DESCRIPTION' ],
                  x_coord=gift_shop[ 'X_COORD' ],
                  y_coord=gift_shop[ 'Y_COORD' ],
                  is_closed=is_closed,
                  closed_message=closed_message,
                  likelihood=likelihood ) )

      cur.close()

      return gift_shops


   def get_active_gift_shop_schedule_status( self, gift_shop_name, target_date, weekday ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.HOLIDAYS_ONLY,
                  s.SCHEDULE_MESSAGE
               FROM GiftShopOpeningSchedule s
               WHERE s.GIFT_SHOP = ?;
         """, ( gift_shop_name, ) )

      schedule_rows = data.fetchall()
      cur.close()

      if len( schedule_rows ) == 0:
         return 'unknown', None

      for schedule in schedule_rows:
         is_active = self.is_date_in_range(
            target_date=target_date,
            start_date_value=schedule[ 'SCHEDULE_START_DATE' ],
            end_date_value=schedule[ 'SCHEDULE_END_DATE' ] )

         if not is_active:
            continue

         is_holiday = zoo.ZooUtil.is_holiday( d=target_date )

         open_on_day = False

         if weekday == 0 and schedule[ 'MONDAY' ]:
            open_on_day = True
         elif weekday == 1 and schedule[ 'TUESDAY' ]:
            open_on_day = True
         elif weekday == 2 and schedule[ 'WEDNESDAY' ]:
            open_on_day = True
         elif weekday == 3 and schedule[ 'THURSDAY' ]:
            open_on_day = True
         elif weekday == 4 and schedule[ 'FRIDAY' ]:
            open_on_day = True
         elif weekday == 5 and schedule[ 'SATURDAY' ]:
            open_on_day = True
         elif weekday == 6 and schedule[ 'SUNDAY' ]:
            open_on_day = True

         if is_holiday and schedule[ 'HOLIDAYS_ONLY' ]:
            open_on_day = True

         if open_on_day:
            return 'open', None

         return 'closed', schedule[ 'SCHEDULE_MESSAGE' ]

      return 'unknown', None


   def calculate_gift_shop_likelihood( self, day_seasonal_availability_multiplier ):
      seasonal_multiplier = (
         day_seasonal_availability_multiplier
         if day_seasonal_availability_multiplier is not None
         else 1.0
      )
      likelihood = max( 0.0, min( seasonal_multiplier, 1.0 ) )

      return max( round( likelihood * 100 ), 0 )


   def get_attractions( self, month, day, include_closed_attractions=False ):
      cur = self.conn.cursor()
      normalized_month = zoo.ZooUtil.normalize_month( month )
      normalized_day = int( day )

      target_date = date(
         datetime.now().year,
         normalized_month,
         normalized_day )

      weekday = target_date.weekday()
      is_weekend_or_holiday = (
         weekday >= 5
         or zoo.ZooUtil.is_holiday( d=target_date ) )

      data = cur.execute(
         """   SELECT
                  a.NAME,
                  a.FREE_WITH_ADMISSION,
                  a.DESCRIPTION,
                  a.INFO_LINK,
                  a.HYPERLINK_TEXT,
                  a.X_COORD,
                  a.Y_COORD,
                  COALESCE( adsam.WEEKDAY_VALUE, 1.0 ) AS ATTRACTION_DAY_SEASONAL_WEEKDAY_MULTIPLIER,
                  COALESCE( adsam.WEEKEND_HOLIDAY_VALUE, 1.0 ) AS ATTRACTION_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER
               FROM Attraction a
               LEFT JOIN AttractionDaySeasonalAvailabilityMultiplier adsam
                  ON a.NAME = adsam.ATTRACTION
                  AND adsam.MONTH = ?
                  AND adsam.DAY = ?;
         """, ( normalized_month, normalized_day ) )

      attraction_data = data.fetchall()

      attractions = []

      for attraction in attraction_data:
         name = attraction[ 'NAME' ]
         likelihood = 100
         closed_message = None
         attraction_day_seasonal_availability_multiplier = (
            attraction[ 'ATTRACTION_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ]
            if is_weekend_or_holiday
            else attraction[ 'ATTRACTION_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ]
         )

         schedule_status, schedule_message = self.get_active_attraction_schedule_status(
            attraction_name=name,
            target_date=target_date,
            weekday=weekday )

         if schedule_status == 'closed':
            likelihood = 0
            closed_message = schedule_message
         elif schedule_status == 'unknown':
            likelihood = self.calculate_attraction_likelihood(
               day_seasonal_availability_multiplier=attraction_day_seasonal_availability_multiplier )

            if likelihood == 0:
               closed_message = f'The { name } is most likely not operating on this day.'

         is_closed = likelihood <= 0

         should_include = (
            ( not is_closed )
            or include_closed_attractions
         )

         if not should_include:
            continue

         attractions.append(
            zoo.Attraction(
               name=name,
               free_with_admission=attraction[ 'FREE_WITH_ADMISSION' ],
               description=attraction[ 'DESCRIPTION' ],
               info_link=attraction[ 'INFO_LINK' ],
               hyperlink_text=attraction[ 'HYPERLINK_TEXT' ],
               x_coord=attraction[ 'X_COORD' ],
               y_coord=attraction[ 'Y_COORD' ],
               is_closed=is_closed,
               closed_message=closed_message,
               likelihood=likelihood ) )

      cur.close()

      return attractions


   def get_active_attraction_schedule_status( self, attraction_name, target_date, weekday ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.HOLIDAYS_ONLY,
                  s.SCHEDULE_MESSAGE
               FROM AttractionOpeningSchedule s
               WHERE s.ATTRACTION = ?;
         """, ( attraction_name, ) )

      schedule_rows = data.fetchall()
      cur.close()

      if len( schedule_rows ) == 0:
         return 'unknown', None

      for schedule in schedule_rows:
         is_active = self.is_date_in_range(
            target_date=target_date,
            start_date_value=schedule[ 'SCHEDULE_START_DATE' ],
            end_date_value=schedule[ 'SCHEDULE_END_DATE' ] )

         if not is_active:
            continue

         is_holiday = zoo.ZooUtil.is_holiday( d=target_date )

         open_on_day = False

         if weekday == 0 and schedule[ 'MONDAY' ]:
            open_on_day = True
         elif weekday == 1 and schedule[ 'TUESDAY' ]:
            open_on_day = True
         elif weekday == 2 and schedule[ 'WEDNESDAY' ]:
            open_on_day = True
         elif weekday == 3 and schedule[ 'THURSDAY' ]:
            open_on_day = True
         elif weekday == 4 and schedule[ 'FRIDAY' ]:
            open_on_day = True
         elif weekday == 5 and schedule[ 'SATURDAY' ]:
            open_on_day = True
         elif weekday == 6 and schedule[ 'SUNDAY' ]:
            open_on_day = True
         elif schedule[ 'HOLIDAYS_ONLY' ] and is_holiday:
            open_on_day = True

         if open_on_day:
            return 'open', None

         message = schedule[ 'SCHEDULE_MESSAGE' ]

         if not message:
            if schedule[ 'SATURDAY' ] and schedule[ 'SUNDAY' ] and schedule[ 'HOLIDAYS_ONLY' ]:
               message = f'The { attraction_name } is open on weekends and holidays only.'
            else:
               message = f'The { attraction_name } is not scheduled to be open today.'

         return 'closed', message

      return 'unknown', None


   def calculate_attraction_likelihood( self, day_seasonal_availability_multiplier ):
      seasonal_multiplier = (
         day_seasonal_availability_multiplier
         if day_seasonal_availability_multiplier is not None
         else 1.0
      )
      likelihood = max( 0.0, min( seasonal_multiplier, 1.0 ) )

      return max( round( likelihood * 100 ), 0 )


   def get_zoomobile_stations( self, route, month, day, zoomobile_stations_to_include=None ):
      if zoomobile_stations_to_include is None:
         zoomobile_stations_to_include = []

      target_date = date(
         datetime.now().year,
         zoo.ZooUtil.normalize_month( month ),
         int( day ) )

      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  s.NAME,
                  s.ON_WINTER_ROUTE,
                  s.DESCRIPTION,
                  s.X_COORD,
                  s.Y_COORD
               FROM ZoomobileStation s;
         """ )

      zoomobile_station_data = data.fetchall()

      zoomobile_stations = []

      for zoomobile_station in zoomobile_station_data:
         name = zoomobile_station[ 'NAME' ]
         on_winter_route = zoomobile_station[ 'ON_WINTER_ROUTE' ]

         if not (
            route == 'summer'
            or on_winter_route
            or name in zoomobile_stations_to_include
         ):
            continue

         status_data = cur.execute(
            """   SELECT
                     s.CLOSED_START,
                     s.CLOSED_END,
                     s.IS_CLOSED,
                     s.CLOSED_MESSAGE
                  FROM ZoomobileStationStatus s
                  WHERE s.ZOOMOBILE_STATION = ?;
            """, ( name, ) )

         status_rows = status_data.fetchall()

         is_closed = False

         for status in status_rows:
            start_ok = True
            end_ok = True

            if status[ 'CLOSED_START' ] != None:
               start_date = self.parse_date_value( value=status[ 'CLOSED_START' ] )
               start_ok = target_date >= start_date

            if status[ 'CLOSED_END' ] != None:
               end_date = self.parse_date_value( value=status[ 'CLOSED_END' ] )
               end_ok = target_date <= end_date

            if not ( start_ok and end_ok ):
               continue

            if status[ 'IS_CLOSED' ]:
               is_closed = True
               break

         if is_closed:
            continue

         zoomobile_stations.append(
            zoo.ZoomobileStation(
               name=name,
               description=zoomobile_station[ 'DESCRIPTION' ],
               x_coord=zoomobile_station[ 'X_COORD' ],
               y_coord=zoomobile_station[ 'Y_COORD' ] ) )

      cur.close()

      return zoomobile_stations


   def get_zoomobile_route( self, route, month, day, zoomobile_stations_to_include=None ):
      if zoomobile_stations_to_include is None:
         zoomobile_stations_to_include = []

      normalized_month = zoo.ZooUtil.normalize_month( month )
      normalized_day = int( day )
      target_date = date(
         datetime.now().year,
         normalized_month,
         normalized_day )
      route_source = 'manual'

      if route == 'current':
         route = self.get_active_zoomobile_route( target_date=target_date )

         if route in [ 'summer', 'winter' ]:
            route_source = 'override'
         else:
            route = self.get_zoomobile_day_route(
               month=normalized_month,
               day=normalized_day )
            route_source = 'fallback'

      if route not in [ 'summer', 'winter' ]:
         route = 'summer'

      zoomobile_stations = self.get_zoomobile_stations(
         route=route,
         month=normalized_month,
         day=normalized_day,
         zoomobile_stations_to_include=zoomobile_stations_to_include )

      return {
         'route': route,
         'route_source': route_source,
         'zoomobile_stations': zoomobile_stations
      }


   def get_active_zoomobile_route( self, target_date ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  z.ROUTE
               FROM ZoomobileRouteSchedule z
               WHERE z.SCHEDULE_START_DATE <= ?
               AND (
                  z.SCHEDULE_END_DATE IS NULL
                  OR z.SCHEDULE_END_DATE >= ?
               )
               ORDER BY z.SCHEDULE_START_DATE DESC
               LIMIT 1;
         """, ( target_date.isoformat(), target_date.isoformat() ) )

      route_data = data.fetchone()
      cur.close()

      if route_data is None:
         return None

      route = route_data[ 'ROUTE' ]

      if route not in [ 'summer', 'winter' ]:
         return None

      return route


   def get_zoomobile_day_route( self, month, day ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  z.ROUTE
               FROM ZoomobileDayRoute z
               WHERE z.MONTH = ?
               AND z.DAY = ?;
         """, ( month, day ) )

      route_data = data.fetchone()
      cur.close()

      if route_data is None:
         return None

      route = route_data[ 'ROUTE' ]

      if route not in [ 'summer', 'winter' ]:
         return None

      return route


   def get_guardians_talks( self, month, day ):
      cur = self.conn.cursor()

      target_date = date(
         datetime.now().year,
         zoo.ZooUtil.normalize_month( month ),
         int( day ) )

      target_weekday = target_date.weekday()
      target_date_str = target_date.isoformat()

      data = cur.execute(
         """   SELECT
                  t.NAME,
                  t.LOCATION,
                  t.X_COORD,
                  t.Y_COORD,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.TALK_TIME
               FROM MeetTheGuardiansTalk t
               JOIN GuardiansTalkSchedule s
                  ON t.NAME = s.TALK_NAME
                  AND t.LOCATION = s.LOCATION;
         """ )

      guardians_talk_data = data.fetchall()

      guardians_talks = []

      for guardians_talk in guardians_talk_data:
         name = guardians_talk[ 'NAME' ]
         location = guardians_talk[ 'LOCATION' ]
         talk_time = guardians_talk[ 'TALK_TIME' ]

         start_ok = True
         end_ok = True
         unavailable_message = None

         if guardians_talk[ 'SCHEDULE_START_DATE' ] != None:
            schedule_start_date = self.parse_date_value(
               value=guardians_talk[ 'SCHEDULE_START_DATE' ] )
            start_ok = target_date >= schedule_start_date

         if guardians_talk[ 'SCHEDULE_END_DATE' ] != None:
            schedule_end_date = self.parse_date_value(
               value=guardians_talk[ 'SCHEDULE_END_DATE' ] )
            end_ok = target_date <= schedule_end_date

         weekday_ok = False

         if target_weekday == 0:
            weekday_ok = bool( guardians_talk[ 'MONDAY' ] )
         elif target_weekday == 1:
            weekday_ok = bool( guardians_talk[ 'TUESDAY' ] )
         elif target_weekday == 2:
            weekday_ok = bool( guardians_talk[ 'WEDNESDAY' ] )
         elif target_weekday == 3:
            weekday_ok = bool( guardians_talk[ 'THURSDAY' ] )
         elif target_weekday == 4:
            weekday_ok = bool( guardians_talk[ 'FRIDAY' ] )
         elif target_weekday == 5:
            weekday_ok = bool( guardians_talk[ 'SATURDAY' ] )
         elif target_weekday == 6:
            weekday_ok = bool( guardians_talk[ 'SUNDAY' ] )

         cancellation_data = cur.execute(
            """   SELECT 1
                  FROM GuardiansTalkCancellation
                  WHERE TALK_NAME = ?
                  AND LOCATION = ?
                  AND CANCELLATION_DATE = ?
                  AND TALK_TIME = ?;
            """,
            (
               name,
               location,
               target_date_str,
               talk_time
            ) )

         is_cancelled = cancellation_data.fetchone() != None
         is_available = start_ok and end_ok and weekday_ok and not is_cancelled

         if not is_available:
            if not start_ok or not end_ok:
               unavailable_message = f'{ name } is not scheduled on { target_date.strftime( "%B" ) } { target_date.day }.'
            elif not weekday_ok:
               unavailable_message = f'{ name } is not offered on this day of the week.'
            elif is_cancelled:
               unavailable_message = f'{ name } has been cancelled for this date.'

         if is_available:
            guardians_talks.append(
               zoo.GuardiansTalk(
                  name=name,
                  location=location,
                  x_coord=guardians_talk[ 'X_COORD' ],
                  y_coord=guardians_talk[ 'Y_COORD' ],
                  time_of_day=talk_time,
                  is_available=is_available,
                  unavailable_message=unavailable_message ) )

      cur.close()

      return guardians_talks


   def get_wild_encounters( self, month, day ):
      cur = self.conn.cursor()

      target_date = date(
         datetime.now().year,
         zoo.ZooUtil.normalize_month( month=month ),
         int( day ) )

      target_weekday = target_date.weekday()
      target_date_str = target_date.isoformat()

      data = cur.execute(
         """   SELECT
                  w.NAME,
                  w.MEETING_SPOT,
                  w.LINK,
                  m.X_COORD,
                  m.Y_COORD,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.ENCOUNTER_TIME
               FROM WildEncounter w
               JOIN WildEncounterMeetingSpot m
                  ON w.MEETING_SPOT = m.NAME
               JOIN WildEncounterSchedule s
                  ON w.NAME = s.WILD_ENCOUNTER;
         """ )

      wild_encounter_data = data.fetchall()

      wild_encounters = []

      for wild_encounter in wild_encounter_data:
         name = wild_encounter[ 'NAME' ]
         encounter_time = wild_encounter[ 'ENCOUNTER_TIME' ]

         start_ok = True
         end_ok = True
         unavailable_message = None

         if wild_encounter[ 'SCHEDULE_START_DATE' ] != None:
            schedule_start_date = self.parse_date_value(
               value=wild_encounter[ 'SCHEDULE_START_DATE' ] )
            start_ok = target_date >= schedule_start_date

         if wild_encounter[ 'SCHEDULE_END_DATE' ] != None:
            schedule_end_date = self.parse_date_value(
               value=wild_encounter[ 'SCHEDULE_END_DATE' ] )
            end_ok = target_date <= schedule_end_date

         weekday_ok = False

         if target_weekday == 0:
            weekday_ok = bool( wild_encounter[ 'MONDAY' ] )
         elif target_weekday == 1:
            weekday_ok = bool( wild_encounter[ 'TUESDAY' ] )
         elif target_weekday == 2:
            weekday_ok = bool( wild_encounter[ 'WEDNESDAY' ] )
         elif target_weekday == 3:
            weekday_ok = bool( wild_encounter[ 'THURSDAY' ] )
         elif target_weekday == 4:
            weekday_ok = bool( wild_encounter[ 'FRIDAY' ] )
         elif target_weekday == 5:
            weekday_ok = bool( wild_encounter[ 'SATURDAY' ] )
         elif target_weekday == 6:
            weekday_ok = bool( wild_encounter[ 'SUNDAY' ] )

         cancellation_data = cur.execute(
            """   SELECT 1
                  FROM WildEncounterCancellation
                  WHERE WILD_ENCOUNTER = ?
                  AND CANCELLATION_DATE = ?
                  AND ENCOUNTER_TIME = ?;
            """,
            (
               name,
               target_date_str,
               encounter_time
            ) )

         is_cancelled = cancellation_data.fetchone() != None
         is_available = start_ok and end_ok and weekday_ok and not is_cancelled

         if not is_available:
            if not start_ok or not end_ok:
               unavailable_message = f'{ name } is not scheduled on { target_date.strftime( "%B" ) } { target_date.day }.'
            elif not weekday_ok:
               unavailable_message = f'{ name } is not offered on this day of the week.'
            elif is_cancelled:
               unavailable_message = f'{ name } has been cancelled for this date.'

         wild_encounters.append(
            zoo.WildEncounter(
               name=name,
               meeting_spot=wild_encounter[ 'MEETING_SPOT' ],
               link=wild_encounter[ 'LINK' ],
               time_of_day=encounter_time,
               x_coord=wild_encounter[ 'X_COORD' ],
               y_coord=wild_encounter[ 'Y_COORD' ],
               is_available=is_available,
               unavailable_message=unavailable_message ) )

      cur.close()

      return wild_encounters


   def get_available_wild_encounters( self, month, day ):
      return [
         wild_encounter
         for wild_encounter in self.get_wild_encounters( month=month, day=day )
         if getattr( wild_encounter, 'is_available', True )
      ]


   def get_drinking_fountain_status( self, month=None, day=None ):
      if month is not None and day is not None:
         target_date = date(
            datetime.now().year,
            zoo.ZooUtil.normalize_month( month=month ),
            int( day ) )
      else:
         target_date = datetime.now().date()

      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               FROM DrinkingFountainStatus
               LIMIT 1;
         """ )

      status = data.fetchone()
      cur.close()

      if status is None:
         return self.get_drinking_fountain_seasonal_status(
            target_date=target_date )

      if not self.is_date_in_range(
            target_date=target_date,
            start_date_value=status[ 'START_DATE' ],
            end_date_value=status[ 'END_DATE' ] ):
         return self.get_drinking_fountain_seasonal_status(
            target_date=target_date )

      is_closed = bool( status[ 'IS_CLOSED' ] )
      closed_message = status[ 'CLOSED_MESSAGE' ]
      likelihood = 0.0 if is_closed else 1.0

      return is_closed, closed_message, likelihood


   def get_drinking_fountain_seasonal_status( self, target_date ):
      likelihood = self.get_drinking_fountain_seasonal_likelihood(
         target_date=target_date )
      is_closed = likelihood <= 0

      return is_closed, None, likelihood


   def get_drinking_fountain_seasonal_likelihood( self, target_date ):
      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  LIKELIHOOD
               FROM DrinkingFountainDaySeasonalAvailabilityMultiplier
               WHERE MONTH = ?
                  AND DAY = ?;
         """,
         (
            target_date.month,
            target_date.day
         ) )

      row = data.fetchone()
      cur.close()

      return row[ 'LIKELIHOOD' ] if row else 1.0


   def get_drinking_fountains( self, month=None, day=None ):
      is_closed, closed_message, likelihood = self.get_drinking_fountain_status(
         month=month,
         day=day )

      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM DrinkingFountain;
         """ )

      drinking_fountains = [
         zoo.DrinkingFountain(
            x_coord=row[ 'X_COORD' ],
            y_coord=row[ 'Y_COORD' ],
            is_closed=is_closed,
            closed_message=closed_message if is_closed else None,
            likelihood=likelihood )
         for row in data.fetchall()
      ]

      cur.close()

      return drinking_fountains


   def get_defibrillators( self ):
      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM Defibrillator;
         """ )

      defibrillators = [
         zoo.Defibrillator(
            x_coord=row[ 'X_COORD' ],
            y_coord=row[ 'Y_COORD' ] )
         for row in data.fetchall()
      ]

      cur.close()

      return defibrillators


   def get_closed_exhibits( self, month, day ):
      cur = self.conn.cursor()

      target_date = date(
         datetime.now().year,
         zoo.ZooUtil.normalize_month( month=month ),
         int( day ) )

      data = cur.execute(
         """   SELECT
                  e.EXHIBIT,
                  e.IS_CLOSED,
                  e.CLOSED_START,
                  e.CLOSED_END
               FROM ExhibitStatus e
               WHERE e.IS_CLOSED = 1;
         """ )

      exhibit_status_data = data.fetchall()

      closed_exhibits = []

      for exhibit_status in exhibit_status_data:
         exhibit = exhibit_status[ 'EXHIBIT' ]

         start_ok = True
         end_ok = True

         if exhibit_status[ 'CLOSED_START' ] != None:
            closed_start = self.parse_date_value(
               value=exhibit_status[ 'CLOSED_START' ] )
            start_ok = target_date >= closed_start

         if exhibit_status[ 'CLOSED_END' ] != None:
            closed_end = self.parse_date_value(
               value=exhibit_status[ 'CLOSED_END' ] )
            end_ok = target_date <= closed_end

         if start_ok and end_ok:
            closed_exhibits.append( exhibit )

      cur.close()

      return closed_exhibits


   def get_animals_matching_query( self, query, month, day, temp, include_off_display_animals ):
      animals = self.get_animals_viewable_on_day( month=month, day=day, temp=temp, include_off_display_animals=include_off_display_animals )

      if query:
         query_lower = query.lower()
         animals = [
            a for a in animals
            if a.species and query_lower in a.species.lower()
         ]

      best_by_species = {}

      for a in animals:

         species = a.species
         if not species:
            continue

         current = best_by_species.get( species )

         if current is None or ( a.likelihood or 0 ) > ( current.likelihood or 0 ):
            best_by_species[ species ] = a

      unique_animals = list( best_by_species.values() )

      unique_animals.sort( key=lambda a: a.species.lower() )

      return unique_animals


   def get_pavilions_matching_query( self, query ):
      if not query:
         return self.get_pavilions()

      query_lower = query.lower()

      return [
         p for p in self.get_pavilions()
         if p.name and query_lower in p.name.lower()
      ]


   def get_restaurants_matching_query( self, query, month, day, include_closed_restaurants ):
      if not query:
         return self.get_restaurants( month=month, day=day, include_closed_restaurants=include_closed_restaurants )

      query_lower = query.lower()

      return [
         r for r in self.get_restaurants( month=month, day=day, include_closed_restaurants=include_closed_restaurants )
         if r.name and query_lower in r.name.lower()
      ]


   def get_restrooms_matching_query( self, query, month=None, day=None, include_closed_restrooms=True ):
      if not query:
         return self.get_restrooms(
            month=month,
            day=day,
            include_closed_restrooms=include_closed_restrooms )

      query_lower = query.lower()

      return [
         r for r in self.get_restrooms(
            month=month,
            day=day,
            include_closed_restrooms=include_closed_restrooms )
         if r.title and query_lower in r.title.lower()
      ]


   def get_gift_shops_matching_query( self, query, month, day ):
      if not query:
         return self.get_gift_shops( month=month, day=day, include_closed_gift_shops=True )

      query_lower = query.lower()

      return [
         g for g in self.get_gift_shops( month=month, day=day, include_closed_gift_shops=True )
         if g.name and query_lower in g.name.lower()
      ]


   def get_attractions_matching_query( self, query, month, day, include_closed_attractions ):
      if not query:
         return self.get_attractions( month=month, day=day, include_closed_attractions=include_closed_attractions )

      query_lower = query.lower()

      return [
         a for a in self.get_attractions( month=month, day=day, include_closed_attractions=include_closed_attractions )
         if a.name and query_lower in a.name.lower()
      ]


   def get_zoomobile_stations_matching_query( self, query, route, month, day ):
      if not query:
         return self.get_zoomobile_stations( route=route, month=month, day=day )

      query_lower = query.lower()

      return [
         s for s in self.get_zoomobile_stations( route=route, month=month, day=day )
         if s.name and query_lower in s.name.lower()
      ]


   def get_guardians_talks_matching_query( self, query, month, day ):
      talks = self.get_guardians_talks( month=month, day=day )

      if not query:
         return talks

      query_lower = query.lower()

      return [
         t for t in talks
         if (
            t.name
            and query_lower in t.name.lower()
         )
      ]


   def get_wild_encounters_matching_query( self, query, month, day ):
      wild_encounters = self.get_available_wild_encounters( month=month, day=day )

      if not query:
         return wild_encounters

      query_lower = query.lower()

      return [
         w for w in wild_encounters
         if w.name and query_lower in w.name.lower()
      ]


   def get_species( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  a.SPECIES
               FROM Animal a;
         """ )

      species = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return species


   def get_itinerary( self ):
      cur = self.conn.cursor()

      itinerary_row = cur.execute(
         """   SELECT
                  ID,
                  IS_ACTIVE,
                  ITINERARY_DATE
               FROM Itinerary
               WHERE ID = 1;
         """ ).fetchone()

      if itinerary_row == None:
         cur.close()
         return None

      date = ''
      month = None
      day = None

      if itinerary_row[ 'ITINERARY_DATE' ] != None:
         itinerary_date = self.parse_date_value(
            value=itinerary_row[ 'ITINERARY_DATE' ] )

         date = itinerary_date.isoformat()
         month = itinerary_date.strftime( '%B' )
         day = itinerary_date.day

      animal_rows = cur.execute(
         """   SELECT
                  SPECIES,
                  EXHIBIT
               FROM ItineraryAnimal;
         """ ).fetchall()

      species_exhibit_pairs = [
         {
            'species': row[ 'SPECIES' ],
            'exhibit': row[ 'EXHIBIT' ]
         }
         for row in animal_rows
      ]

      attractions_to_include = [
         row[ 'ATTRACTION' ]
         for row in cur.execute(
            """   SELECT
                     ATTRACTION
                  FROM ItineraryAttraction;
            """ ).fetchall()
      ]

      guardians_talks_to_include = [
         row[ 'TALK_NAME' ]
         for row in cur.execute(
            """   SELECT
                     TALK_NAME
                  FROM ItineraryGuardiansTalk;
            """ ).fetchall()
      ]

      wild_encounters_to_include = [
         row[ 'WILD_ENCOUNTER' ]
         for row in cur.execute(
            """   SELECT
                     WILD_ENCOUNTER
                  FROM ItineraryWildEncounter;
            """ ).fetchall()
      ]

      animals = []
      attractions = []
      guardians_talks = []
      wild_encounters = []

      if bool( itinerary_row[ 'IS_ACTIVE' ] ) and month and day:
         if species_exhibit_pairs:
            animals = self.get_animals_for_itinerary(
               month=month,
               day=day,
               temp=None,
               species_exhibit_pairs=species_exhibit_pairs,
               include_off_display_animals=True )

         if attractions_to_include:
            attractions = self.get_attractions_for_itinerary(
               month=month,
               day=day,
               attractions_to_include=attractions_to_include,
               include_closed_attractions=True )

         if guardians_talks_to_include:
            guardians_talks = self.get_guardians_talks_for_itinerary(
               month=month,
               day=day,
               guardians_talks_to_include=guardians_talks_to_include )

         if wild_encounters_to_include:
            wild_encounters = self.get_wild_encounters_for_itinerary(
               month=month,
               day=day,
               wild_encounters_to_include=wild_encounters_to_include )

      itinerary = zoo.Itinerary(
         date=date,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters )

      cur.close()

      return itinerary


   def set_itinerary(
         self,
         date,
         animals,
         attractions,
         guardians_talks,
         wild_encounters,
         is_active ):
      cur = self.conn.cursor()

      if not date:
         date = None

      if animals == None:
         animals = []

      if attractions == None:
         attractions = []

      if guardians_talks == None:
         guardians_talks = []

      if wild_encounters == None:
         wild_encounters = []

      cur.execute(
         """   UPDATE Itinerary
               SET IS_ACTIVE = ?,
                   ITINERARY_DATE = ?
               WHERE ID = 1;
         """,
         (
            int( bool( is_active ) ),
            date
         ) )

      cur.execute( 'DELETE FROM ItineraryAnimal;' )
      cur.execute( 'DELETE FROM ItineraryAttraction;' )
      cur.execute( 'DELETE FROM ItineraryGuardiansTalk;' )
      cur.execute( 'DELETE FROM ItineraryWildEncounter;' )

      for animal in animals:
         species = None
         exhibit = None

         if isinstance( animal, dict ):
            species = animal.get( 'species' )
            exhibit = animal.get( 'exhibit' )

         if species and exhibit:
            cur.execute(
               """   INSERT OR IGNORE INTO ItineraryAnimal (
                        SPECIES,
                        EXHIBIT
                     )
                     VALUES ( ?, ? );
               """,
               (
                  species,
                  exhibit
               ) )

      for attraction in attractions:
         attraction_name = attraction

         if isinstance( attraction, dict ):
            attraction_name = attraction.get( 'name' )

         if attraction_name:
            cur.execute(
               """   INSERT OR IGNORE INTO ItineraryAttraction (
                        ATTRACTION
                     )
                     VALUES ( ? );
               """,
               ( attraction_name, ) )

      for guardians_talk in guardians_talks:
         talk_name = guardians_talk

         if isinstance( guardians_talk, dict ):
            talk_name = guardians_talk.get( 'name' )

         if talk_name:
            cur.execute(
               """   INSERT OR IGNORE INTO ItineraryGuardiansTalk (
                        TALK_NAME
                     )
                     VALUES ( ? );
               """,
               ( talk_name, ) )

      for wild_encounter in wild_encounters:
         wild_encounter_name = wild_encounter

         if isinstance( wild_encounter, dict ):
            wild_encounter_name = wild_encounter.get( 'name' )

         if wild_encounter_name:
            cur.execute(
               """   INSERT OR IGNORE INTO ItineraryWildEncounter (
                        WILD_ENCOUNTER
                     )
                     VALUES ( ? );
               """,
               ( wild_encounter_name, ) )

      self.conn.commit()
      cur.close()

      return True


   def clear_itinerary( self ):
      cur = self.conn.cursor()

      cur.execute(
         """   UPDATE Itinerary
               SET IS_ACTIVE = 0,
                   ITINERARY_DATE = NULL
               WHERE ID = 1;
         """ )

      cur.execute( 'DELETE FROM ItineraryAnimal;' )
      cur.execute( 'DELETE FROM ItineraryAttraction;' )
      cur.execute( 'DELETE FROM ItineraryGuardiansTalk;' )
      cur.execute( 'DELETE FROM ItineraryWildEncounter;' )

      self.conn.commit()
      cur.close()

      return True


   def validate_animals( self, month, day, temp, animals_to_include=None ):
      animals_to_include = animals_to_include or []

      animals = self.get_animals_for_itinerary(
         month=month,
         day=day,
         temp=temp,
         species_exhibit_pairs=animals_to_include,
         include_off_display_animals=True )

      best_valid_by_species = {}
      removed_by_species = {}

      for animal in animals:
         species = animal.species

         if animal.likelihood <= 0:
            removed_by_species[ species ] = animal
            continue

         current = best_valid_by_species.get( species )

         if current is None or animal.likelihood > current.likelihood:
            best_valid_by_species[ species ] = animal

      valid_animals = list( best_valid_by_species.values() )
      valid_animals.sort( key=lambda a: a.species.lower() )

      removed_animals = []

      for species, animal in removed_by_species.items():
         if species not in best_valid_by_species:
            removed_animals.append( animal )

      removed_animals.sort( key=lambda a: a.species.lower() )

      return {
         'valid_animals': valid_animals,
         'removed_animals': removed_animals
      }


   def validate_attractions( self, month, day, attractions_to_include=None ):
      attractions_to_include = attractions_to_include or []

      attractions = self.get_attractions_for_itinerary(
         month=month,
         day=day,
         attractions_to_include=attractions_to_include,
         include_closed_attractions=True )

      valid_attractions = []
      removed_attractions = []

      for attraction in attractions:
         if attraction.is_closed:
            removed_attractions.append( attraction )
         else:
            valid_attractions.append( attraction )

      valid_attractions.sort( key=lambda a: a.name.lower() )
      removed_attractions.sort( key=lambda a: a.name.lower() )

      return {
         'valid_attractions': valid_attractions,
         'removed_attractions': removed_attractions
      }


   def validate_guardians_talks( self, month, day, guardians_talks_to_include=None ):
      guardians_talks_to_include = guardians_talks_to_include or []

      guardians_talks = self.get_guardians_talks_for_itinerary(
         month=month,
         day=day,
         guardians_talks_to_include=guardians_talks_to_include )

      valid_guardians_talks = []
      removed_guardians_talks = []

      for guardians_talk in guardians_talks:
         if getattr( guardians_talk, 'is_available', True ):
            valid_guardians_talks.append( guardians_talk )
         else:
            removed_guardians_talks.append( guardians_talk )

      valid_guardians_talks.sort(
         key=lambda t: ( t.name.lower(), t.time_of_day )
      )

      removed_guardians_talks.sort(
         key=lambda t: ( t.name.lower(), t.time_of_day )
      )

      return {
         'valid_guardians_talks': valid_guardians_talks,
         'removed_guardians_talks': removed_guardians_talks
      }


   def validate_wild_encounters( self, month, day, wild_encounters_to_include=None ):
      wild_encounters_to_include = wild_encounters_to_include or []

      wild_encounters = self.get_wild_encounters_for_itinerary(
         month=month,
         day=day,
         wild_encounters_to_include=wild_encounters_to_include )

      valid_wild_encounters = []
      removed_wild_encounters = []

      for wild_encounter in wild_encounters:
         if getattr( wild_encounter, 'is_available', True ):
            valid_wild_encounters.append( wild_encounter )
         else:
            removed_wild_encounters.append( wild_encounter )

      valid_wild_encounters.sort(
         key=lambda w: ( w.name.lower(), w.time_of_day )
      )

      removed_wild_encounters.sort(
         key=lambda w: ( w.name.lower(), w.time_of_day )
      )

      return {
         'valid_wild_encounters': valid_wild_encounters,
         'removed_wild_encounters': removed_wild_encounters
      }


   def get_regions_with_exhibits( self, month, day ):
      cur = self.conn.cursor()

      target_date = date(
         datetime.now().year,
         zoo.ZooUtil.normalize_month( month ),
         int( day ) )

      data = cur.execute(
         """   SELECT
                  r.NAME AS REGION_NAME,
                  e.NAME AS EXHIBIT_NAME,
                  s.IS_CLOSED,
                  s.CLOSED_START,
                  s.CLOSED_END
               FROM Region r
               LEFT JOIN Exhibit e
                  ON e.REGION = r.NAME
               LEFT JOIN ExhibitStatus s
                  ON e.NAME = s.EXHIBIT
               ORDER BY r.NAME, e.NAME;
         """ )

      rows = data.fetchall()
      regions = []
      current_region = None

      for row in rows:
         region_name = row[ 'REGION_NAME' ]
         exhibit_name = row[ 'EXHIBIT_NAME' ]

         if current_region == None or current_region[ 'name' ] != region_name:
            current_region = {
               'name': region_name,
               'exhibits': []
            }
            regions.append( current_region )

         if exhibit_name == None:
            continue

         is_closed = False

         if row[ 'IS_CLOSED' ]:
            start_ok = True
            end_ok = True

            if row[ 'CLOSED_START' ] != None:
               closed_start = self.parse_date_value(
                  value=row[ 'CLOSED_START' ] )
               start_ok = target_date >= closed_start

            if row[ 'CLOSED_END' ] != None:
               closed_end = self.parse_date_value(
                  value=row[ 'CLOSED_END' ] )
               end_ok = target_date <= closed_end

            is_closed = start_ok and end_ok

         if not is_closed:
            current_region[ 'exhibits' ].append( exhibit_name )

      cur.close()

      regions = [
         region for region in regions
         if len( region[ 'exhibits' ] ) > 0
      ]

      return regions


   def get_exhibits( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  e.NAME
               FROM Exhibit e;
         """ )

      exhibits = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return exhibits


   def get_restaurant_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  r.NAME
               FROM Restaurant r;
         """ )

      restaurants = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return restaurants


   def get_restroom_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  r.TITLE
               FROM Restroom r;
         """ )

      restrooms = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return restrooms


   def get_gift_shop_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  g.NAME
               FROM GiftShop g;
         """ )

      gift_shops = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return gift_shops


   def get_attraction_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  a.NAME
               FROM Attraction a;
         """ )

      attractions = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return attractions


   def get_zoomobile_station_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  s.NAME
               FROM ZoomobileStation s;
         """ )

      zoomobile_stations = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return zoomobile_stations


   def get_guardians_talk_locations( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT DISTINCT
                  t.LOCATION
               FROM MeetTheGuardiansTalk t
               WHERE t.LOCATION IS NOT NULL
               ORDER BY t.LOCATION;
         """ )

      guardians_talk_locations = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return guardians_talk_locations


   def get_guardians_talk_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  t.NAME
               FROM MeetTheGuardiansTalk t;
         """ )

      guardians_talks = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return guardians_talks


   def get_guardians_talk_names_at_location( self, location ):
      cur = self.conn.cursor()

      data = cur.execute(
         """  SELECT
                  t.NAME
              FROM MeetTheGuardiansTalk t
              WHERE t.LOCATION = ?;
         """,
         ( location, ) )

      guardians_talks = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return guardians_talks


   def get_guardians_talk_occurrences( self, talk, location, days_ahead=60 ):
      if not talk or not location:
         return []

      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  TALK_TIME
               FROM GuardiansTalkSchedule
               WHERE TALK_NAME = ?
               AND LOCATION = ?;
         """,
         (
            talk,
            location
         ) )

      guardians_talk_schedule = data.fetchone()

      if guardians_talk_schedule == None:
         cur.close()
         return []

      today = datetime.now().date()

      schedule_start_date = today
      schedule_end_date = today + timedelta( days=days_ahead )

      if guardians_talk_schedule[ 'SCHEDULE_START_DATE' ] != None:
         parsed_start_date = self.parse_date_value(
            value=guardians_talk_schedule[ 'SCHEDULE_START_DATE' ] )
         if parsed_start_date > schedule_start_date:
            schedule_start_date = parsed_start_date

      if guardians_talk_schedule[ 'SCHEDULE_END_DATE' ] != None:
         parsed_end_date = self.parse_date_value(
            value=guardians_talk_schedule[ 'SCHEDULE_END_DATE' ] )
         if parsed_end_date < schedule_end_date:
            schedule_end_date = parsed_end_date

      if schedule_end_date < schedule_start_date:
         cur.close()
         return []

      talk_time = guardians_talk_schedule[ 'TALK_TIME' ]

      cancellation_data = cur.execute(
         """   SELECT
                  CANCELLATION_DATE,
                  TALK_TIME
               FROM GuardiansTalkCancellation
               WHERE TALK_NAME = ?
               AND LOCATION = ?;
         """,
         (
            talk,
            location
         ) )

      cancelled_occurrence_keys = {
         (
            row[ 'CANCELLATION_DATE' ],
            row[ 'TALK_TIME' ]
         )
         for row in cancellation_data.fetchall()
      }

      guardians_talk_occurrences = []

      current_date = schedule_start_date

      while current_date <= schedule_end_date:
         weekday_ok = False
         target_weekday = current_date.weekday()

         if target_weekday == 0:
            weekday_ok = bool( guardians_talk_schedule[ 'MONDAY' ] )
         elif target_weekday == 1:
            weekday_ok = bool( guardians_talk_schedule[ 'TUESDAY' ] )
         elif target_weekday == 2:
            weekday_ok = bool( guardians_talk_schedule[ 'WEDNESDAY' ] )
         elif target_weekday == 3:
            weekday_ok = bool( guardians_talk_schedule[ 'THURSDAY' ] )
         elif target_weekday == 4:
            weekday_ok = bool( guardians_talk_schedule[ 'FRIDAY' ] )
         elif target_weekday == 5:
            weekday_ok = bool( guardians_talk_schedule[ 'SATURDAY' ] )
         elif target_weekday == 6:
            weekday_ok = bool( guardians_talk_schedule[ 'SUNDAY' ] )

         current_date_str = current_date.isoformat()

         if weekday_ok and ( current_date_str, talk_time ) not in cancelled_occurrence_keys:
            guardians_talk_occurrences.append(
               {
                  'date': current_date_str,
                  'time': talk_time
               } )

         current_date += timedelta( days=1 )

      cur.close()

      return guardians_talk_occurrences


   def get_wild_encounter_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  w.NAME
               FROM WildEncounter w;
         """ )

      wild_encounters = [ row[ 0 ] for row in data.fetchall() ]
      cur.close()

      return wild_encounters


   def get_wild_encounter_occurrences( self, wild_encounter, days_ahead=60 ):
      if not wild_encounter:
         return []

      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  ENCOUNTER_TIME
               FROM WildEncounterSchedule
               WHERE WILD_ENCOUNTER = ?;
         """,
         ( wild_encounter, ) )

      wild_encounter_schedule = data.fetchone()

      if wild_encounter_schedule == None:
         cur.close()
         return []

      today = datetime.now().date()

      schedule_start_date = today
      schedule_end_date = today + timedelta( days=days_ahead )

      if wild_encounter_schedule[ 'SCHEDULE_START_DATE' ] != None:
         parsed_start_date = self.parse_date_value(
            value=wild_encounter_schedule[ 'SCHEDULE_START_DATE' ] )
         if parsed_start_date > schedule_start_date:
            schedule_start_date = parsed_start_date

      if wild_encounter_schedule[ 'SCHEDULE_END_DATE' ] != None:
         parsed_end_date = self.parse_date_value(
            value=wild_encounter_schedule[ 'SCHEDULE_END_DATE' ] )
         if parsed_end_date < schedule_end_date:
            schedule_end_date = parsed_end_date

      if schedule_end_date < schedule_start_date:
         cur.close()
         return []

      encounter_time = wild_encounter_schedule[ 'ENCOUNTER_TIME' ]

      cancellation_data = cur.execute(
         """   SELECT
                  CANCELLATION_DATE,
                  ENCOUNTER_TIME
               FROM WildEncounterCancellation
               WHERE WILD_ENCOUNTER = ?;
         """,
         ( wild_encounter, ) )

      cancelled_occurrence_keys = {
         (
            row[ 'CANCELLATION_DATE' ],
            row[ 'ENCOUNTER_TIME' ]
         )
         for row in cancellation_data.fetchall()
      }

      wild_encounter_occurrences = []

      current_date = schedule_start_date

      while current_date <= schedule_end_date:
         weekday_ok = False
         target_weekday = current_date.weekday()

         if target_weekday == 0:
            weekday_ok = bool( wild_encounter_schedule[ 'MONDAY' ] )
         elif target_weekday == 1:
            weekday_ok = bool( wild_encounter_schedule[ 'TUESDAY' ] )
         elif target_weekday == 2:
            weekday_ok = bool( wild_encounter_schedule[ 'WEDNESDAY' ] )
         elif target_weekday == 3:
            weekday_ok = bool( wild_encounter_schedule[ 'THURSDAY' ] )
         elif target_weekday == 4:
            weekday_ok = bool( wild_encounter_schedule[ 'FRIDAY' ] )
         elif target_weekday == 5:
            weekday_ok = bool( wild_encounter_schedule[ 'SATURDAY' ] )
         elif target_weekday == 6:
            weekday_ok = bool( wild_encounter_schedule[ 'SUNDAY' ] )

         current_date_str = current_date.isoformat()

         if weekday_ok and ( current_date_str, encounter_time ) not in cancelled_occurrence_keys:
            wild_encounter_occurrences.append(
               {
                  'date': current_date_str,
                  'time': encounter_time
               } )

         current_date += timedelta( days=1 )

      cur.close()

      return wild_encounter_occurrences


   def get_animals_for_itinerary(
         self,
         month,
         day,
         temp=None,
         species_exhibit_pairs=None,
         include_off_display_animals=True,
         exhibits_to_include=None ):

      species_exhibit_pairs = species_exhibit_pairs or []

      pairs_filter = set()

      for pair in species_exhibit_pairs:

         if not isinstance( pair, dict ):
            continue

         species = ( pair.get( 'species' ) or '' ).strip().lower()
         exhibit = ( pair.get( 'exhibit' ) or '' ).strip().lower()

         if species and exhibit:
            pairs_filter.add( ( species, exhibit ) )

      if not pairs_filter:
         return []

      animals = self.get_animals_viewable_on_day(
         month=month,
         day=day,
         temp=temp,
         include_off_display_animals=include_off_display_animals,
         threshold=0,
         exhibits_to_include=exhibits_to_include )

      animals = [
         a for a in animals
         if (
            ( a.species or '' ).strip().lower(),
            ( a.exhibit or '' ).strip().lower()
         ) in pairs_filter
      ]

      has_positive_by_species = set()

      for animal in animals:
         if ( animal.likelihood or 0 ) > 0:
            has_positive_by_species.add(
               ( animal.species or '' ).strip().lower()
            )

      filtered_animals = []

      for animal in animals:
         species = ( animal.species or '' ).strip().lower()
         likelihood = animal.likelihood or 0

         if likelihood <= 0 and species in has_positive_by_species:
            continue

         filtered_animals.append( animal )

      filtered_animals.sort(
         key=lambda a: (
            ( a.species or '' ).lower(),
            ( a.exhibit or '' ).lower()
         )
      )

      return filtered_animals


   def get_attractions_for_itinerary(
         self,
         month,
         day,
         attractions_to_include=None,
         include_closed_attractions=True ):

      attractions_to_include = attractions_to_include or []

      attractions_filter = set()

      for attraction_name in attractions_to_include:

         if not isinstance( attraction_name, str ):
            continue

         attraction_name = attraction_name.strip().lower()

         if attraction_name:
            attractions_filter.add( attraction_name )

      if not attractions_filter:
         return []

      attractions = self.get_attractions(
         month=month,
         day=day,
         include_closed_attractions=include_closed_attractions )

      attractions = [
         attraction for attraction in attractions
         if ( attraction.name or '' ).strip().lower() in attractions_filter
      ]

      attractions.sort( key=lambda a: ( a.name or '' ).lower() )

      return attractions


   def get_guardians_talks_for_itinerary(
         self,
         month,
         day,
         guardians_talks_to_include=None ):

      guardians_talks_to_include = guardians_talks_to_include or []

      guardians_talks_filter = set()

      for talk_name in guardians_talks_to_include:

         if not isinstance( talk_name, str ):
            continue

         talk_name = talk_name.strip().lower()

         if talk_name:
            guardians_talks_filter.add( talk_name )

      if not guardians_talks_filter:
         return []

      guardians_talks = self.get_guardians_talks(
         month=month,
         day=day )

      guardians_talks = [
         guardians_talk for guardians_talk in guardians_talks
         if ( guardians_talk.name or '' ).strip().lower() in guardians_talks_filter
      ]

      guardians_talks.sort(
         key=lambda t: (
            ( t.name or '' ).lower(),
            t.time_of_day or ''
         )
      )

      return guardians_talks


   def get_wild_encounters_for_itinerary(
         self,
         month,
         day,
         wild_encounters_to_include=None ):

      wild_encounters_to_include = wild_encounters_to_include or []

      wild_encounters_filter = set()

      for wild_encounter_name in wild_encounters_to_include:

         if not isinstance( wild_encounter_name, str ):
            continue

         wild_encounter_name = wild_encounter_name.strip().lower()

         if wild_encounter_name:
            wild_encounters_filter.add( wild_encounter_name )

      if not wild_encounters_filter:
         return []

      wild_encounters = self.get_wild_encounters(
         month=month,
         day=day )

      wild_encounters = [
         wild_encounter for wild_encounter in wild_encounters
         if ( wild_encounter.name or '' ).strip().lower() in wild_encounters_filter
      ]

      wild_encounters.sort(
         key=lambda w: (
            ( w.name or '' ).lower(),
            w.time_of_day or ''
         )
      )

      return wild_encounters


   def set_animal_as_off_display( self, species, exhibit, start_date, end_date, message ):
      if not message:
         message = f'The { species } is temporarily off-display.'

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if end_date == '':
         end_date = None

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_MESSAGE
               )
               VALUES (?, ?, 1, ?, ?, ?)
               ON CONFLICT(SPECIES, EXHIBIT) DO UPDATE SET
                  IS_OFF_DISPLAY = 1,
                  OFF_DISPLAY_START = excluded.OFF_DISPLAY_START,
                  OFF_DISPLAY_END = excluded.OFF_DISPLAY_END,
                  OFF_DISPLAY_MESSAGE = excluded.OFF_DISPLAY_MESSAGE;
         """,
         ( species, exhibit, start_date, end_date, message ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_animal_as_on_display( self, species, exhibit ):
      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_MESSAGE
               )
               VALUES (?, ?, 0, NULL)
               ON CONFLICT(SPECIES, EXHIBIT) DO UPDATE SET
                  IS_OFF_DISPLAY = 0,
                  OFF_DISPLAY_MESSAGE = NULL;
         """, ( species, exhibit, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_animal_limited_viewing_schedule( self, species, exhibit, start_date, end_date, daily_start_time,
                                            daily_end_time, message ):
      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not daily_start_time or not daily_end_time:
         return False

      if not message:

         formatted_daily_start_time = datetime.strptime( daily_start_time, '%H:%M' ).strftime( '%I:%M %p' ).lstrip( '0' )
         formatted_daily_end_time = datetime.strptime( daily_end_time, '%H:%M' ).strftime( '%I:%M %p' ).lstrip( '0' )

         if end_date != None:

            formatted_end_date = datetime.strptime( end_date, '%Y-%m-%d' ).strftime( '%A, %B %d, %Y' )

            message = (
               f'The { species } is viewable daily only from { formatted_daily_start_time } to { formatted_daily_end_time }'
               f'until { formatted_end_date }.'
            )

         else:
            message = (
               f'The { species } is viewable daily only from { formatted_daily_start_time } to { formatted_daily_end_time }.'
            )

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO AnimalVisibilitySchedule (
                  SPECIES,
                  EXHIBIT,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  DAILY_START_TIME,
                  DAILY_END_TIME,
                  VIEWING_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(SPECIES, EXHIBIT) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  DAILY_START_TIME = excluded.DAILY_START_TIME,
                  DAILY_END_TIME = excluded.DAILY_END_TIME,
                  VIEWING_MESSAGE = excluded.VIEWING_MESSAGE;
         """, ( species, exhibit, start_date, end_date, daily_start_time, daily_end_time, message ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def remove_animal_visibility_schedule( self, species, exhibit ):
      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM AnimalVisibilitySchedule
            WHERE SPECIES = ?
               AND EXHIBIT = ?;
         """,
         ( species, exhibit ) )

      self.conn.commit()
      deleted = cur.rowcount
      cur.close()

      return deleted > 0


   def set_animal_viewing_alert( self, species, exhibit, alert_start_date, alert_end_date, message ):
      if not alert_start_date:
         alert_start_date = datetime.now().date().isoformat()

      if not alert_end_date:
         alert_end_date = None

      if not message:
         message = f'The { species } may be less visible than usual at this time.'

      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM AnimalViewingAlert
             WHERE SPECIES = ?
             AND EXHIBIT = ?;
         """,
         ( species, exhibit ) )

      cur.execute(
         """   INSERT INTO AnimalViewingAlert (
                  SPECIES,
                  EXHIBIT,
                  ALERT_MESSAGE,
                  ALERT_START_DATE,
                  ALERT_END_DATE
               )
               VALUES (?, ?, ?, ?, ?)
         """, ( species, exhibit, message, alert_start_date, alert_end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def remove_animal_viewing_alert( self, species, exhibit ):
      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM AnimalViewingAlert
            WHERE SPECIES = ?
            AND EXHIBIT = ?;
         """,
         ( species, exhibit ) )

      self.conn.commit()
      removed = cur.rowcount
      cur.close()

      return removed > 0


   def set_exhibit_as_closed( self, exhibit, start_date, end_date, message ):
      if not exhibit:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { exhibit } is temporarily closed.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO ExhibitStatus (
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(EXHIBIT) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( exhibit, message, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_exhibit_as_open( self, exhibit, start_date, end_date ):
      if not exhibit:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO ExhibitStatus (
                  EXHIBIT,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 0, NULL, ?, ?)
               ON CONFLICT(EXHIBIT) DO UPDATE SET
                  IS_CLOSED = 0,
                  CLOSED_MESSAGE = NULL,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( exhibit, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_restroom_as_closed( self, restroom, start_date, end_date, message ):
      if not restroom:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { restroom } is temporarily closed.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO RestroomStatus (
                  RESTROOM,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(RESTROOM) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( restroom, message, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_restroom_as_open( self, restroom, start_date, end_date ):
      if not restroom:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO RestroomStatus (
                  RESTROOM,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 0, NULL, ?, ?)
               ON CONFLICT(RESTROOM) DO UPDATE SET
                  IS_CLOSED = 0,
                  CLOSED_MESSAGE = NULL,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( restroom, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_restroom_alert( self, restroom, alert_start_date, alert_end_date, message ):
      if not restroom or not message:
         return False

      if not alert_start_date:
         alert_start_date = datetime.now().date().isoformat()

      if not alert_end_date:
         alert_end_date = None

      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM RestroomAlert
             WHERE RESTROOM = ?;
         """, ( restroom, ) )

      cur.execute(
         """   INSERT INTO RestroomAlert (
                  RESTROOM,
                  ALERT_MESSAGE,
                  ALERT_START_DATE,
                  ALERT_END_DATE
               )
               VALUES (?, ?, ?, ?)
         """, ( restroom, message, alert_start_date, alert_end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def remove_restroom_alert( self, restroom ):
      if not restroom:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM RestroomAlert
             WHERE RESTROOM = ?;
         """, ( restroom, ) )

      self.conn.commit()
      removed = cur.rowcount
      cur.close()

      return removed > 0


   def set_restaurant_as_closed( self, restaurant, start_date, end_date, message ):
      if not restaurant:
         return False

      if not message:
         message = f'The { restaurant } is temporarily closed.'

      return self.set_restaurant_opening_schedule(
         restaurant=restaurant,
         start_date=start_date,
         end_date=end_date,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
         message=message )


   def set_restaurant_opening_schedule(
         self,
         restaurant,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message ):
      if not restaurant:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { restaurant } is not scheduled to be open today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO RestaurantOpeningSchedule (
                  RESTAURANT,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(RESTAURANT) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            restaurant,
            start_date,
            end_date,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            int( bool( holidays_only ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_gift_shop_as_closed( self, gift_shop, start_date, end_date, message ):
      if not gift_shop:
         return False

      if not message:
         message = f'The { gift_shop } is temporarily closed.'

      return self.set_gift_shop_opening_schedule(
         gift_shop=gift_shop,
         start_date=start_date,
         end_date=end_date,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
         message=message )


   def set_gift_shop_opening_schedule(
         self,
         gift_shop,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message ):
      if not gift_shop:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { gift_shop } is not scheduled to be open today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO GiftShopOpeningSchedule (
                  GIFT_SHOP,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(GIFT_SHOP) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            gift_shop,
            start_date,
            end_date,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            int( bool( holidays_only ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_attraction_as_closed( self, attraction, start_date, end_date, message ):
      if not attraction:
         return False

      if not message:
         message = f'The { attraction } is temporarily closed.'

      return self.set_attraction_opening_schedule(
         attraction=attraction,
         start_date=start_date,
         end_date=end_date,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
         message=message )


   def set_attraction_opening_schedule(
         self,
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message ):
      if not attraction:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { attraction } is not scheduled to be open today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO AttractionOpeningSchedule (
                  ATTRACTION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(ATTRACTION) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  HOLIDAYS_ONLY = excluded.HOLIDAYS_ONLY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            attraction,
            start_date,
            end_date,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            int( bool( holidays_only ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_zoomobile_station_as_closed( self, zoomobile_station, start_date, end_date, message ):
      if not zoomobile_station:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { zoomobile_station } is temporarily closed.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO ZoomobileStationStatus (
                  ZOOMOBILE_STATION,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(ZOOMOBILE_STATION) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( zoomobile_station, message, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_zoomobile_station_as_open( self, zoomobile_station ):
      if not zoomobile_station:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM ZoomobileStationStatus
               WHERE ZOOMOBILE_STATION = ?;
         """, ( zoomobile_station, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_current_zoomobile_route( self, route, start_date, end_date ):
      if route not in ( 'summer', 'winter' ):
         return False

      try:
         normalized_start_date = (
            self.parse_date_value( value=start_date ).isoformat()
            if start_date
            else datetime.now().date().isoformat()
         )
      except ValueError:
         return False

      normalized_end_date = None

      if end_date:
         try:
            normalized_end_date = self.parse_date_value( value=end_date ).isoformat()
         except ValueError:
            return False

         if normalized_end_date < normalized_start_date:
            return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM ZoomobileRouteSchedule;
         """ )

      cur.execute(
         """   INSERT INTO ZoomobileRouteSchedule (
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ROUTE
               )
               VALUES ( ?, ?, ? )
         """, ( normalized_start_date, normalized_end_date, route ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_guardians_talk_schedule(
         self,
         talk,
         location,
         start_date,
         end_date,
         talk_time,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         message ):
      if not talk or not location:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { talk } at { location } is not scheduled today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO GuardiansTalkSchedule (
                  TALK_NAME,
                  LOCATION,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  TALK_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(TALK_NAME, LOCATION) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  TALK_TIME = excluded.TALK_TIME,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            talk,
            location,
            start_date,
            end_date,
            talk_time,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def end_guardians_talk_schedule( self, talk, location, schedule_end_date ):
      if not talk or not location:
         return False

      if not schedule_end_date:
         schedule_end_date = datetime.now().date().isoformat()

      cur = self.conn.cursor()

      cur.execute(
         """   UPDATE GuardiansTalkSchedule
               SET SCHEDULE_END_DATE = ?
               WHERE TALK_NAME = ?
               AND LOCATION = ?;
         """,
         (
            schedule_end_date,
            talk,
            location
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def cancel_guardians_talk_occurrence( self, talk, location, date, time ):
      if not talk or not location or not date or not time:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO GuardiansTalkCancellation (
                  TALK_NAME,
                  LOCATION,
                  CANCELLATION_DATE,
                  TALK_TIME
               )
               VALUES (?, ?, ?, ?)
               ON CONFLICT(TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME)
               DO NOTHING;
         """,
         (
            talk,
            location,
            date,
            time
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_wild_encounter_schedule(
         self,
         wild_encounter,
         start_date,
         end_date,
         encounter_time,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         message ):
      if not wild_encounter:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The { wild_encounter } is not scheduled today.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO WildEncounterSchedule (
                  WILD_ENCOUNTER,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ENCOUNTER_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(WILD_ENCOUNTER) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  ENCOUNTER_TIME = excluded.ENCOUNTER_TIME,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            wild_encounter,
            start_date,
            end_date,
            encounter_time,
            int( bool( monday ) ),
            int( bool( tuesday ) ),
            int( bool( wednesday ) ),
            int( bool( thursday ) ),
            int( bool( friday ) ),
            int( bool( saturday ) ),
            int( bool( sunday ) ),
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def end_wild_encounter_schedule( self, wild_encounter, schedule_end_date ):
      if not wild_encounter:
         return False

      if not schedule_end_date:
         schedule_end_date = datetime.now().date().isoformat()

      cur = self.conn.cursor()

      cur.execute(
         """   UPDATE WildEncounterSchedule
               SET SCHEDULE_END_DATE = ?
               WHERE WILD_ENCOUNTER = ?;
         """,
         (
            schedule_end_date,
            wild_encounter
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def cancel_wild_encounter_occurrence( self, wild_encounter, date, time ):
      if not wild_encounter or not date or not time:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO WildEncounterCancellation (
                  WILD_ENCOUNTER,
                  CANCELLATION_DATE,
                  ENCOUNTER_TIME
               )
               VALUES (?, ?, ?)
               ON CONFLICT(WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME)
               DO NOTHING;
         """,
         (
            wild_encounter,
            date,
            time
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_drinking_fountains_as_closed( self, start_date=None, end_date=None, message=None ):
      if not message:
         message = 'The drinking fountains are closed for the season.'

      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM DrinkingFountainStatus;
         """ )

      cur.execute(
         """   INSERT INTO DrinkingFountainStatus (
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               )
               VALUES (1, ?, ?, ?);
         """, (
            start_date,
            end_date,
            message
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_drinking_fountains_as_open( self, start_date=None, end_date=None ):
      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM DrinkingFountainStatus;
         """ )

      cur.execute(
         """   INSERT INTO DrinkingFountainStatus (
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               )
               VALUES (0, ?, ?, NULL);
         """, (
            start_date,
            end_date
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
