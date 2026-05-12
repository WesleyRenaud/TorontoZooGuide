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

      is_off_display = zoo.ZooUtil.is_date_in_range(
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

      is_active = zoo.ZooUtil.is_date_in_range( target_date=target_date, start_date_value=schedule_start_date, end_date_value=schedule_end_date )

      if is_active:
         return True, viewing_message

      return False, None


   def get_active_viewing_alert_status( self, animal, target_date ):
      alert_message = animal[ 'ALERT_MESSAGE' ]
      alert_start_date = animal[ 'ALERT_START_DATE' ]
      alert_end_date = animal[ 'ALERT_END_DATE' ]

      if alert_message == None:
         return False, None

      is_active = zoo.ZooUtil.is_date_in_range( target_date=target_date, start_date_value=alert_start_date, end_date_value=alert_end_date )

      if is_active:
         return True, alert_message

      return False, None


   def get_active_exhibit_status( self, animal, target_date ):
      if animal[ 'IS_CLOSED' ] == None:
         return 'unknown', None

      start_date = animal[ 'CLOSED_START' ]
      end_date = animal[ 'CLOSED_END' ]

      is_active = zoo.ZooUtil.is_date_in_range(
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
         is_active = zoo.ZooUtil.is_date_in_range(
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
            status_is_active = zoo.ZooUtil.is_date_in_range(
               target_date=target_date,
               start_date_value=restroom[ 'CLOSED_START' ],
               end_date_value=restroom[ 'CLOSED_END' ] )

            is_closed = bool( restroom[ 'IS_CLOSED' ] ) and status_is_active

            if is_closed:
               closed_message = restroom[ 'CLOSED_MESSAGE' ]

         if restroom[ 'ALERT_MESSAGE' ] != None:
            alert_is_active = zoo.ZooUtil.is_date_in_range(
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
         is_active = zoo.ZooUtil.is_date_in_range(
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
         likelihood, closed_message = (
            self.get_attraction_likelihood_and_message_for_date(
               attraction,
               target_date ) )

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
         is_active = zoo.ZooUtil.is_date_in_range(
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


   def get_attraction_likelihood_and_message_for_date(
         self, attraction_row, target_date ):
      name = attraction_row[ 'NAME' ]
      weekday = target_date.weekday()
      is_weekend_or_holiday = (
         weekday >= 5
         or zoo.ZooUtil.is_holiday( d=target_date ) )

      attraction_day_seasonal_availability_multiplier = (
         attraction_row[ 'ATTRACTION_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ]
         if is_weekend_or_holiday
         else attraction_row[ 'ATTRACTION_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ]
      )

      likelihood = 100
      closed_message = None

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

      return likelihood, closed_message


   def get_attraction_row_for_calendar_day(
         self, attraction_name, month_int, day_int ):
      cur = self.conn.cursor()

      row = cur.execute(
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
                  AND adsam.DAY = ?
               WHERE a.NAME = ?;
         """,
         ( month_int, day_int, attraction_name )
      ).fetchone()

      cur.close()

      return row


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
               start_date = zoo.ZooUtil.parse_date_value( value=status[ 'CLOSED_START' ] )
               start_ok = target_date >= start_date

            if status[ 'CLOSED_END' ] != None:
               end_date = zoo.ZooUtil.parse_date_value( value=status[ 'CLOSED_END' ] )
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


   def get_guardians_talk_details( self, guardians_talks_to_include=None ):
      guardians_talks_filter = {
         talk_name.strip().lower()
         for talk_name in guardians_talks_to_include or []
      }

      if guardians_talks_to_include != None and not guardians_talks_filter:
         return []

      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  NAME,
                  LOCATION,
                  X_COORD,
                  Y_COORD,
                  MAXIMUM_DURATION
               FROM MeetTheGuardiansTalk;
         """ )

      rows = data.fetchall()
      cur.close()

      guardians_talks = []

      for row in rows:
         if guardians_talks_filter and (
               row[ 'NAME' ] or '' ).strip().lower() not in guardians_talks_filter:
            continue

         guardians_talks.append(
            zoo.GuardiansTalk(
               name=row[ 'NAME' ],
               location=row[ 'LOCATION' ],
               x_coord=row[ 'X_COORD' ],
               y_coord=row[ 'Y_COORD' ],
               maximum_duration=row[ 'MAXIMUM_DURATION' ] ) )

      guardians_talks.sort(
         key=lambda t: (
            ( t.name or '' ).lower(),
            ( t.location or '' ).lower()
         )
      )

      return guardians_talks


   def get_guardians_talk_schedule( self, month, day ):
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
                  t.MAXIMUM_DURATION,
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
            schedule_start_date = zoo.ZooUtil.parse_date_value(
               value=guardians_talk[ 'SCHEDULE_START_DATE' ] )
            start_ok = target_date >= schedule_start_date

         if guardians_talk[ 'SCHEDULE_END_DATE' ] != None:
            schedule_end_date = zoo.ZooUtil.parse_date_value(
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
                  start_time=talk_time,
                  maximum_duration=guardians_talk[ 'MAXIMUM_DURATION' ],
                  is_available=is_available,
                  unavailable_message=unavailable_message ) )

      cur.close()

      return guardians_talks


   def get_guardians_talk_schedule_for_talk_on_day(
         self,
         month,
         day,
         talk_name,
         day_schedule=None ):
      rows = (
         day_schedule
         if day_schedule is not None
         else self.get_guardians_talk_schedule( month=month, day=day )
      )

      key = ( talk_name or '' ).strip().lower()

      if not key:
         return []

      return [
         row for row in rows
         if ( row.name or '' ).strip().lower() == key
      ]


   def get_wild_encounter_details( self, wild_encounters_to_include=None ):
      wild_encounters_filter = {
         wild_encounter_name.strip().lower()
         for wild_encounter_name in wild_encounters_to_include or []
      }

      if wild_encounters_to_include != None and not wild_encounters_filter:
         return []

      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  w.NAME,
                  w.MEETING_SPOT,
                  w.LINK,
                  w.MAXIMUM_DURATION,
                  m.X_COORD,
                  m.Y_COORD
               FROM WildEncounter w
               JOIN WildEncounterMeetingSpot m
                  ON w.MEETING_SPOT = m.NAME;
         """ )

      rows = data.fetchall()
      cur.close()

      wild_encounters = []

      for row in rows:
         if wild_encounters_filter and (
               row[ 'NAME' ] or '' ).strip().lower() not in wild_encounters_filter:
            continue

         wild_encounters.append(
            zoo.WildEncounter(
               name=row[ 'NAME' ],
               meeting_spot=row[ 'MEETING_SPOT' ],
               link=row[ 'LINK' ],
               maximum_duration=row[ 'MAXIMUM_DURATION' ],
               x_coord=row[ 'X_COORD' ],
               y_coord=row[ 'Y_COORD' ] ) )

      wild_encounters.sort( key=lambda w: ( w.name or '' ).lower() )

      return wild_encounters


   def get_wild_encounter_schedule( self, month, day ):
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
                  w.MAXIMUM_DURATION,
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
            schedule_start_date = zoo.ZooUtil.parse_date_value(
               value=wild_encounter[ 'SCHEDULE_START_DATE' ] )
            start_ok = target_date >= schedule_start_date

         if wild_encounter[ 'SCHEDULE_END_DATE' ] != None:
            schedule_end_date = zoo.ZooUtil.parse_date_value(
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
               start_time=encounter_time,
               maximum_duration=wild_encounter[ 'MAXIMUM_DURATION' ],
               x_coord=wild_encounter[ 'X_COORD' ],
               y_coord=wild_encounter[ 'Y_COORD' ],
               is_available=is_available,
               unavailable_message=unavailable_message ) )

      cur.close()

      return wild_encounters


   def get_wild_encounter_schedule_for_encounter_on_day(
         self,
         month,
         day,
         encounter_name,
         day_schedule=None ):
      """Return schedule rows for *encounter_name* on the given day (subset of *day_schedule* when passed)."""
      rows = (
         day_schedule
         if day_schedule is not None
         else self.get_wild_encounter_schedule( month=month, day=day )
      )

      key = ( encounter_name or '' ).strip().lower()

      if not key:
         return []

      return [
         row for row in rows
         if ( row.name or '' ).strip().lower() == key
      ]


   def get_available_wild_encounters( self, month, day ):
      return [
         wild_encounter
         for wild_encounter in self.get_wild_encounter_schedule(
            month=month,
            day=day )
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

      if not zoo.ZooUtil.is_date_in_range(
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


   def get_emergency_intercoms( self ):
      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM EmergencyIntercom;
         """ )

      emergency_intercoms = [
         zoo.EmergencyIntercom(
            x_coord=row[ 'X_COORD' ],
            y_coord=row[ 'Y_COORD' ] )
         for row in data.fetchall()
      ]

      cur.close()

      return emergency_intercoms


   def get_guest_services( self ):
      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  SERVICE_TYPE,
                  X_COORD,
                  Y_COORD
               FROM GuestService;
         """ )

      guest_services = [
         zoo.GuestService(
            service_type=row[ 'SERVICE_TYPE' ],
            x_coord=row[ 'X_COORD' ],
            y_coord=row[ 'Y_COORD' ] )
         for row in data.fetchall()
      ]

      cur.close()

      return guest_services


   def get_picnic_sites( self ):
      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM PicnicSite;
         """ )

      picnic_sites = [
         zoo.PicnicSite(
            x_coord=row[ 'X_COORD' ],
            y_coord=row[ 'Y_COORD' ] )
         for row in data.fetchall()
      ]

      cur.close()

      return picnic_sites


   def get_event_sites( self ):
      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  NAME,
                  X_COORD,
                  Y_COORD
               FROM EventSite;
         """ )

      event_sites = [
         zoo.EventSite(
            name=row[ 'NAME' ],
            x_coord=row[ 'X_COORD' ],
            y_coord=row[ 'Y_COORD' ] )
         for row in data.fetchall()
      ]

      cur.close()

      return event_sites


   def get_updates( self, month=None, day=None ):
      if month != None and day != None:
         target_date = date(
            datetime.now().year,
            zoo.ZooUtil.normalize_month( month=month ),
            int( day ) )
      else:
         target_date = datetime.now().date()

      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  TITLE,
                  DESCRIPTION,
                  UPDATE_TYPE,
                  START_DATE,
                  END_DATE
               FROM ZooUpdate
               WHERE START_DATE <= ?
                  AND (
                     END_DATE IS NULL
                     OR END_DATE >= ?
                  )
               ORDER BY START_DATE DESC, TITLE ASC;
         """,
         (
            target_date.isoformat(),
            target_date.isoformat()
         ) )

      updates = [
         zoo.Update(
            title=row[ 'TITLE' ],
            description=row[ 'DESCRIPTION' ],
            update_type=row[ 'UPDATE_TYPE' ],
            start_date=row[ 'START_DATE' ],
            end_date=row[ 'END_DATE' ] )
         for row in data.fetchall()
      ]

      cur.close()

      return updates


   def get_active_update_options( self ):
      return [
         update.to_dict()
         for update in self.get_updates()
      ]


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
            closed_start = zoo.ZooUtil.parse_date_value(
               value=exhibit_status[ 'CLOSED_START' ] )
            start_ok = target_date >= closed_start

         if exhibit_status[ 'CLOSED_END' ] != None:
            closed_end = zoo.ZooUtil.parse_date_value(
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
      talks = self.get_guardians_talk_schedule( month=month, day=day )

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


   def get_itinerary_date( self ):
      cur = self.conn.cursor()

      date_row = cur.execute(
         """   SELECT ITINERARY_DATE
               FROM ItineraryDate
               LIMIT 1;
         """
      ).fetchone()

      cur.close()

      if date_row == None or date_row[ 'ITINERARY_DATE' ] == None:
         return None

      return zoo.ZooUtil.normalize_date_key( date_row[ 'ITINERARY_DATE' ] )


   def get_itinerary( self ):
      date_value = self.get_itinerary_date()

      if date_value == None:
         return zoo.Itinerary(
            date='',
            animals=[],
            attractions=[],
            guardians_talks=[],
            wild_encounters=[] )

      itinerary_date = zoo.ZooUtil.parse_date_value( date_value )

      date = itinerary_date.isoformat()
      month = itinerary_date.strftime( '%B' )
      day = itinerary_date.day

      cur = self.conn.cursor()

      animal_rows = cur.execute(
         """   SELECT
                  SPECIES,
                  EXHIBIT,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD
               FROM ItineraryAnimal;
         """ ).fetchall()

      species_exhibit_pairs = [
         {
            'species': row[ 'SPECIES' ],
            'exhibit': row[ 'EXHIBIT' ]
         }
         for row in animal_rows
      ]

      attraction_rows = cur.execute(
         """   SELECT
                  ATTRACTION,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD
               FROM ItineraryAttraction;
         """ ).fetchall()

      attractions_to_include = [
         row[ 'ATTRACTION' ]
         for row in attraction_rows
      ]

      guardians_talk_rows = cur.execute(
         """   SELECT
                  TALK_NAME,
                  START_TIME,
                  END_TIME,
                  IS_DELETED
               FROM ItineraryGuardiansTalk;
         """ ).fetchall()

      guardians_talks_to_include = [
         row[ 'TALK_NAME' ]
         for row in guardians_talk_rows
      ]

      wild_encounter_rows = cur.execute(
         """   SELECT
                  WILD_ENCOUNTER,
                  START_TIME,
                  END_TIME,
                  IS_DELETED
               FROM ItineraryWildEncounter;
         """ ).fetchall()

      wild_encounters_to_include = [
         row[ 'WILD_ENCOUNTER' ]
         for row in wild_encounter_rows
      ]

      animals = []
      attractions = []
      guardians_talks = []
      wild_encounters = []

      if species_exhibit_pairs:
         animals = self.get_animals_for_itinerary(
            month=month,
            day=day,
            temp=None,
            species_exhibit_pairs=species_exhibit_pairs,
            include_off_display_animals=True,
            saved_animal_rows=animal_rows )

      if attractions_to_include:
         attractions = self.get_attractions_for_itinerary(
            month=month,
            day=day,
            attractions_to_include=attractions_to_include,
            include_closed_attractions=True,
            saved_attraction_rows=attraction_rows )

      if guardians_talks_to_include:
         guardians_talks = self.get_guardians_talks_for_itinerary(
            guardians_talks_to_include=guardians_talks_to_include,
            saved_guardians_talk_rows=guardians_talk_rows )

      if wild_encounters_to_include:
         wild_encounters = self.get_wild_encounters_for_itinerary(
            wild_encounters_to_include=wild_encounters_to_include,
            saved_wild_encounter_rows=wild_encounter_rows )

      itinerary = zoo.Itinerary(
         date=date,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters )

      cur.close()

      return itinerary


   def get_zoo_hours( self, date_value ):
      operating_date = zoo.ZooUtil.parse_date_value( date_value ).isoformat()
      cur = self.conn.cursor()

      row = cur.execute(
         """   SELECT
                  OPERATING_DATE,
                  EARLY_ADMISSION_TIME,
                  OPEN_TIME,
                  LAST_ADMISSION_TIME,
                  CLOSE_TIME
               FROM ZooHours
               WHERE OPERATING_DATE = ?;
         """,
         ( operating_date, ) ).fetchone()

      cur.close()

      if row == None:
         return None

      return {
         'date': row[ 'OPERATING_DATE' ],
         'earlyAdmissionTime': row[ 'EARLY_ADMISSION_TIME' ],
         'openTime': row[ 'OPEN_TIME' ],
         'lastAdmissionTime': row[ 'LAST_ADMISSION_TIME' ],
         'closeTime': row[ 'CLOSE_TIME' ]
      }


   def get_guardians_talk_maximum_duration( self, cursor, talk_name ):
      row = cursor.execute(
         """   SELECT MAXIMUM_DURATION
               FROM MeetTheGuardiansTalk
               WHERE NAME = ?;
         """,
         ( talk_name, ) ).fetchone()

      return row[ 'MAXIMUM_DURATION' ] if row != None else None


   def get_wild_encounter_maximum_duration( self, cursor, wild_encounter_name ):
      row = cursor.execute(
         """   SELECT MAXIMUM_DURATION
               FROM WildEncounter
               WHERE NAME = ?;
         """,
         ( wild_encounter_name, ) ).fetchone()

      return row[ 'MAXIMUM_DURATION' ] if row != None else None


   def set_itinerary(
         self,
         date,
         animals,
         attractions,
         guardians_talks,
         wild_encounters ):
      animals = animals or []
      attractions = attractions or []
      guardians_talks = guardians_talks or []
      wild_encounters = wild_encounters or []

      itinerary_date = zoo.ZooUtil.parse_date_value( date )
      month = itinerary_date.strftime( '%B' )
      day = itinerary_date.day

      old_visit_date = self.get_itinerary_date()
      new_visit_date = date

      validation = self.validate_itinerary(
         month,
         day,
         animals,
         attractions,
         guardians_talks,
         wild_encounters,
         new_visit_date_temp=None,
         old_visit_date=old_visit_date,
         new_visit_date=new_visit_date )

      self.clear_itinerary()

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO ItineraryDate ( ITINERARY_DATE )
               VALUES ( ? );
         """,
         ( date, )
      )

      for animal in validation[ 'animals' ]:
         cur.execute(
            """   INSERT OR IGNORE INTO ItineraryAnimal (
                     SPECIES,
                     EXHIBIT,
                     OLD_LIKELIHOOD,
                     NEW_LIKELIHOOD
                  )
                  VALUES ( ?, ?, ?, ? );
            """,
            (
               animal.species,
               animal.exhibit,
               animal.old_likelihood,
               animal.new_likelihood,
            ) )

      for attraction in validation[ 'attractions' ]:
         cur.execute(
            """   INSERT OR IGNORE INTO ItineraryAttraction (
                     ATTRACTION,
                     OLD_LIKELIHOOD,
                     NEW_LIKELIHOOD
                  )
                  VALUES ( ?, ?, ? );
            """,
            (
               attraction.name,
               attraction.old_likelihood,
               attraction.new_likelihood,
            ) )

      for talk in validation[ 'guardians_talks' ]:
         cur.execute(
            """   INSERT OR IGNORE INTO ItineraryGuardiansTalk (
                     TALK_NAME,
                     START_TIME,
                     END_TIME,
                     IS_DELETED
                  )
                  VALUES ( ?, ?, ?, ? );
            """,
            (
               talk.name,
               talk.start_time,
               talk.end_time,
               1 if talk.is_deleted else 0,
            ) )

      for encounter in validation[ 'wild_encounters' ]:
         cur.execute(
            """   INSERT OR IGNORE INTO ItineraryWildEncounter (
                     WILD_ENCOUNTER,
                     START_TIME,
                     END_TIME,
                     IS_DELETED
                  )
                  VALUES ( ?, ?, ?, ? );
            """,
            (
               encounter.name,
               encounter.start_time,
               encounter.end_time,
               1 if encounter.is_deleted else 0,
            ) )

      self.conn.commit()
      cur.close()

      return True


   def clear_itinerary( self ):
      cur = self.conn.cursor()

      cur.execute( 'DELETE FROM ItineraryDate;' )

      cur.execute( 'DELETE FROM ItineraryAnimal;' )
      cur.execute( 'DELETE FROM ItineraryAttraction;' )
      cur.execute( 'DELETE FROM ItineraryGuardiansTalk;' )
      cur.execute( 'DELETE FROM ItineraryWildEncounter;' )

      self.conn.commit()
      cur.close()

      return True


   def get_animal_likelihood_for_date( self, month, day, temp, species, exhibit ):
      rows = self.get_animals_for_itinerary(
         month=month,
         day=day,
         temp=temp,
         species_exhibit_pairs=[
            {
               'species': species,
               'exhibit': exhibit,
            }
         ],
         include_off_display_animals=True,
      )

      if not rows:
         return None

      return rows[ 0 ].likelihood


   def get_attraction_likelihood_for_visit_date(
         self, visit_date_value, attraction_name ):
      name = ( attraction_name or '' ).strip()

      parsed = zoo.ZooUtil.parse_date_value( visit_date_value )

      row = self.get_attraction_row_for_calendar_day(
         name,
         parsed.month,
         parsed.day )

      if row == None:
         return None

      likelihood, _ = self.get_attraction_likelihood_and_message_for_date(
         row,
         parsed )

      return likelihood


   def validate_itinerary(
         self,
         month,
         day,
         animals,
         attractions,
         guardians_talks,
         wild_encounters,
         new_visit_date_temp=None,
         old_visit_date=None,
         new_visit_date=None ):
      guardians_talks = guardians_talks or []
      wild_encounters = wild_encounters or []

      saved_itinerary_animal_rows = []
      saved_itinerary_attraction_rows = []

      if old_visit_date != None:
         cur = self.conn.cursor()

         saved_itinerary_animal_rows = cur.execute(
            """   SELECT
                     SPECIES,
                     EXHIBIT,
                     NEW_LIKELIHOOD
                  FROM ItineraryAnimal;
            """
         ).fetchall()

         saved_itinerary_attraction_rows = cur.execute(
            """   SELECT
                     ATTRACTION,
                     NEW_LIKELIHOOD
                  FROM ItineraryAttraction;
            """
         ).fetchall()

         cur.close()

      return {
         'animals': (
            self.validate_animals(
               animals=animals,
               new_visit_date_temp=new_visit_date_temp,
               old_visit_date=old_visit_date,
               new_visit_date=new_visit_date,
               saved_itinerary_animal_rows=saved_itinerary_animal_rows )
            if animals
            else []
         ),
         'attractions': (
            self.validate_attractions(
               attractions=attractions,
               old_visit_date=old_visit_date,
               new_visit_date=new_visit_date,
               saved_itinerary_attraction_rows=saved_itinerary_attraction_rows )
            if attractions
            else []
         ),
         'guardians_talks': self.validate_guardians_talks(
            month=month,
            day=day,
            guardians_talks_to_include=guardians_talks ),
         'wild_encounters': self.validate_wild_encounters(
            month=month,
            day=day,
            wild_encounters_to_include=wild_encounters ),
      }


   def validate_animals(
         self,
         animals,
         new_visit_date_temp=None,
         old_visit_date=None,
         new_visit_date=None,
         saved_itinerary_animal_rows=None ):
      parsed_new = zoo.ZooUtil.parse_date_value( new_visit_date )
      new_month = parsed_new.strftime( '%B' )
      new_day = parsed_new.day

      old_likelihood_by_pair = {}

      if old_visit_date != None and saved_itinerary_animal_rows:
         for row in saved_itinerary_animal_rows:
            old_likelihood_by_pair[
               ( row[ 'SPECIES' ], row[ 'EXHIBIT' ] )
            ] = row[ 'NEW_LIKELIHOOD' ]

      diffs = []

      for item in animals:
         species = ( item.get( 'species' ) or '' ).strip()
         exhibit = ( item.get( 'exhibit' ) or '' ).strip()

         old_likelihood = (
            None
            if old_visit_date == None
            else old_likelihood_by_pair.get( ( species, exhibit ) ) )

         new_likelihood = self.get_animal_likelihood_for_date(
            new_month,
            new_day,
            new_visit_date_temp,
            species,
            exhibit )

         diffs.append(
            zoo.AnimalDiff(
               species=species,
               exhibit=exhibit,
               old_likelihood=old_likelihood,
               new_likelihood=new_likelihood,
            )
         )

      return diffs


   def validate_attractions(
         self,
         attractions,
         old_visit_date=None,
         new_visit_date=None,
         saved_itinerary_attraction_rows=None ):

      old_likelihood_by_name = {}

      if old_visit_date != None and saved_itinerary_attraction_rows:

         for row in saved_itinerary_attraction_rows:
            old_likelihood_by_name[ row[ 'ATTRACTION' ] ] = row[ 'NEW_LIKELIHOOD' ]

      diffs = []

      for attraction in attractions:
         attraction_name = str( attraction ).strip()

         old_likelihood = (
            None
            if old_visit_date == None
            else old_likelihood_by_name.get( attraction_name ) )

         new_likelihood = self.get_attraction_likelihood_for_visit_date(
            new_visit_date,
            attraction_name )

         diffs.append(
            zoo.AttractionDiff(
               name=attraction_name,
               old_likelihood=old_likelihood,
               new_likelihood=new_likelihood,
            )
         )

      return diffs


   def build_guardians_talk_diff_for_visit_day( self, talk_name, talk_schedule_rows ):
      has_available = any(
         getattr( row, 'is_available', True )
         for row in talk_schedule_rows
      )
      resolved_name = (
         talk_schedule_rows[ 0 ].name
         if talk_schedule_rows
         else str( talk_name ).strip()
      )

      start_time = None
      end_time = None

      if talk_schedule_rows and talk_schedule_rows[ 0 ].start_time:
         start_time = talk_schedule_rows[ 0 ].start_time
         cur = self.conn.cursor()

         try:
            end_time = zoo.ZooUtil.add_minutes_to_time(
               start_time,
               self.get_guardians_talk_maximum_duration( cur, resolved_name ) )
         finally:
            cur.close()

      return zoo.GuardiansTalkDiff(
         name=resolved_name,
         is_deleted=not has_available,
         start_time=start_time,
         end_time=end_time,
      )


   def build_wild_encounter_diff_for_visit_day( self, encounter_name, encounter_schedule_rows ):
      has_available = any(
         getattr( row, 'is_available', True )
         for row in encounter_schedule_rows
      )
      resolved_name = (
         encounter_schedule_rows[ 0 ].name
         if encounter_schedule_rows
         else str( encounter_name ).strip()
      )

      start_time = None
      end_time = None

      if encounter_schedule_rows and encounter_schedule_rows[ 0 ].start_time:
         start_time = encounter_schedule_rows[ 0 ].start_time
         cur = self.conn.cursor()

         try:
            end_time = zoo.ZooUtil.add_minutes_to_time(
               start_time,
               self.get_wild_encounter_maximum_duration( cur, resolved_name ) )
         finally:
            cur.close()

      return zoo.WildEncounterDiff(
         name=resolved_name,
         is_deleted=not has_available,
         start_time=start_time,
         end_time=end_time,
      )


   def validate_guardians_talks( self, month, day, guardians_talks_to_include=None ):
      day_schedule = self.get_guardians_talk_schedule( month=month, day=day )

      diffs = []

      for talk_name in guardians_talks_to_include or []:
         talk_schedule = self.get_guardians_talk_schedule_for_talk_on_day(
            month,
            day,
            talk_name,
            day_schedule=day_schedule )

         diffs.append(
            self.build_guardians_talk_diff_for_visit_day( talk_name, talk_schedule )
         )

      return diffs


   def validate_wild_encounters( self, month, day, wild_encounters_to_include=None ):
      day_schedule = self.get_wild_encounter_schedule( month=month, day=day )

      diffs = []

      for encounter_name in wild_encounters_to_include or []:
         encounter_schedule = self.get_wild_encounter_schedule_for_encounter_on_day(
            month,
            day,
            encounter_name,
            day_schedule=day_schedule )

         diffs.append(
            self.build_wild_encounter_diff_for_visit_day(
               encounter_name,
               encounter_schedule )
         )

      return diffs


   def get_regions_with_exhibits( self, month, day ):
      cur = self.conn.cursor()
      target_date = None

      if month != None and day != None:
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

         if row[ 'IS_CLOSED' ] and target_date != None:
            start_ok = True
            end_ok = True

            if row[ 'CLOSED_START' ] != None:
               closed_start = zoo.ZooUtil.parse_date_value(
                  value=row[ 'CLOSED_START' ] )
               start_ok = target_date >= closed_start

            if row[ 'CLOSED_END' ] != None:
               closed_end = zoo.ZooUtil.parse_date_value(
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
         parsed_start_date = zoo.ZooUtil.parse_date_value(
            value=guardians_talk_schedule[ 'SCHEDULE_START_DATE' ] )
         if parsed_start_date > schedule_start_date:
            schedule_start_date = parsed_start_date

      if guardians_talk_schedule[ 'SCHEDULE_END_DATE' ] != None:
         parsed_end_date = zoo.ZooUtil.parse_date_value(
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
         parsed_start_date = zoo.ZooUtil.parse_date_value(
            value=wild_encounter_schedule[ 'SCHEDULE_START_DATE' ] )
         if parsed_start_date > schedule_start_date:
            schedule_start_date = parsed_start_date

      if wild_encounter_schedule[ 'SCHEDULE_END_DATE' ] != None:
         parsed_end_date = zoo.ZooUtil.parse_date_value(
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
         exhibits_to_include=None,
         saved_animal_rows=None ):

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

      if saved_animal_rows is not None:
         saved_row_by_pair = {
            (
               ( row[ 'SPECIES' ] or '' ).strip().lower(),
               ( row[ 'EXHIBIT' ] or '' ).strip().lower()
            ): row
            for row in saved_animal_rows
         }

         for animal in filtered_animals:
            saved_row = saved_row_by_pair.get( (
               ( animal.species or '' ).strip().lower(),
               ( animal.exhibit or '' ).strip().lower()
            ) )

            if saved_row == None:
               continue

            animal.old_likelihood = saved_row[ 'OLD_LIKELIHOOD' ]
            animal.new_likelihood = saved_row[ 'NEW_LIKELIHOOD' ]

      return filtered_animals


   def get_attractions_for_itinerary(
         self,
         month,
         day,
         attractions_to_include=None,
         include_closed_attractions=True,
         saved_attraction_rows=None ):

      if saved_attraction_rows is not None:
         attractions_to_include = [
            row[ 'ATTRACTION' ]
            for row in saved_attraction_rows
         ]
      else:
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

      if saved_attraction_rows is not None:
         saved_row_by_name = {
            ( row[ 'ATTRACTION' ] or '' ).strip().lower(): row
            for row in saved_attraction_rows
         }

         for attraction in attractions:
            saved_row = saved_row_by_name.get(
               ( attraction.name or '' ).strip().lower() )

            if saved_row == None:
               continue

            attraction.old_likelihood = saved_row[ 'OLD_LIKELIHOOD' ]
            attraction.new_likelihood = saved_row[ 'NEW_LIKELIHOOD' ]

      attractions.sort( key=lambda a: ( a.name or '' ).lower() )

      return attractions


   def get_guardians_talks_for_itinerary(
         self,
         guardians_talks_to_include=None,
         saved_guardians_talk_rows=None ):

      guardians_talk_names = [
         row[ 'TALK_NAME' ]
         for row in saved_guardians_talk_rows or []
      ] or guardians_talks_to_include or []

      if not guardians_talk_names:
         return []

      guardians_talks = self.get_guardians_talk_details(
         guardians_talk_names )

      if saved_guardians_talk_rows:
         self.apply_saved_guardians_talk_times(
            guardians_talks,
            saved_guardians_talk_rows )

      guardians_talks.sort(
         key=lambda t: (
            ( t.name or '' ).lower(),
            t.start_time or ''
         )
      )

      return guardians_talks


   def apply_saved_guardians_talk_times( self, guardians_talks, saved_guardians_talk_rows ):
      guardians_talk_row_by_name = {
         ( row[ 'TALK_NAME' ] or '' ).strip().lower(): row
         for row in saved_guardians_talk_rows
      }

      for guardians_talk in guardians_talks:
         row = guardians_talk_row_by_name.get(
            ( guardians_talk.name or '' ).strip().lower() )

         if row == None:
            continue

         guardians_talk.start_time = row[ 'START_TIME' ]
         guardians_talk.end_time = row[ 'END_TIME' ]
         guardians_talk.is_deleted = bool( row[ 'IS_DELETED' ] )


   def get_wild_encounters_for_itinerary(
         self,
         wild_encounters_to_include=None,
         saved_wild_encounter_rows=None ):

      wild_encounter_names = [
         row[ 'WILD_ENCOUNTER' ]
         for row in saved_wild_encounter_rows or []
      ] or wild_encounters_to_include or []

      if not wild_encounter_names:
         return []

      wild_encounters = self.get_wild_encounter_details(
         wild_encounter_names )

      if saved_wild_encounter_rows:
         self.apply_saved_wild_encounter_times(
            wild_encounters,
            saved_wild_encounter_rows )

      wild_encounters.sort(
         key=lambda w: (
            ( w.name or '' ).lower(),
            w.start_time or ''
         )
      )

      return wild_encounters


   def apply_saved_wild_encounter_times( self, wild_encounters, saved_wild_encounter_rows ):
      wild_encounter_row_by_name = {
         ( row[ 'WILD_ENCOUNTER' ] or '' ).strip().lower(): row
         for row in saved_wild_encounter_rows
      }

      for wild_encounter in wild_encounters:
         row = wild_encounter_row_by_name.get(
            ( wild_encounter.name or '' ).strip().lower() )

         if row == None:
            continue

         wild_encounter.start_time = row[ 'START_TIME' ]
         wild_encounter.end_time = row[ 'END_TIME' ]
         wild_encounter.is_deleted = bool( row[ 'IS_DELETED' ] )


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


   def normalize_update_type( self, update_type ):
      update_type_labels = {
         'animal birth': 'Animal Birth',
         'animal_birth': 'Animal Birth',
         'animal passing': 'Animal Passing',
         'animal_passing': 'Animal Passing',
         'closure': 'Closure',
         'new arrival': 'New Arrival',
         'new_arrival': 'New Arrival',
         'departure': 'Departure'
      }

      normalized_key = str( update_type or '' ).strip().lower()

      return update_type_labels.get( normalized_key )


   def create_update( self, title, description, update_type, start_date, end_date ):
      title = str( title or '' ).strip()
      description = str( description or '' ).strip()
      normalized_update_type = self.normalize_update_type( update_type )

      if not title or not description or normalized_update_type == None:
         return None

      if not start_date:
         start_date = datetime.now().date().isoformat()

      parsed_end_date = None

      try:
         parsed_start_date = zoo.ZooUtil.parse_date_value( start_date )

         if end_date:
            parsed_end_date = zoo.ZooUtil.parse_date_value( end_date )
      except ValueError:
         return None

      if parsed_end_date != None and parsed_end_date < parsed_start_date:
         return None

      cur = self.conn.cursor()
      cur.execute(
         """   INSERT INTO ZooUpdate (
                  TITLE,
                  DESCRIPTION,
                  UPDATE_TYPE,
                  START_DATE,
                  END_DATE
               )
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(TITLE, START_DATE) DO NOTHING;
         """,
         (
            title,
            description,
            normalized_update_type,
            parsed_start_date.isoformat(),
            parsed_end_date.isoformat() if parsed_end_date != None else None
         ) )

      self.conn.commit()
      created = cur.rowcount
      cur.close()

      return created > 0


   def end_update( self, title, start_date, end_date ):
      if not title or not start_date:
         return False

      if not end_date:
         end_date = datetime.now().date().isoformat()

      try:
         parsed_end_date = zoo.ZooUtil.parse_date_value( end_date )
      except ValueError:
         return False

      cur = self.conn.cursor()
      cur.execute(
         """   UPDATE ZooUpdate
               SET END_DATE = ?
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         (
            parsed_end_date.isoformat(),
            title,
            start_date
         ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def edit_update( self, title, start_date, description=None, update_type=None, end_date=None ):
      if not title or not start_date:
         return False

      parsed_end_date = None
      should_update_end_date = end_date is not None
      normalized_update_type = None

      if update_type:
         normalized_update_type = self.normalize_update_type( update_type )

         if normalized_update_type == None:
            return False

      if should_update_end_date and end_date:
         try:
            parsed_end_date = zoo.ZooUtil.parse_date_value( end_date )
         except ValueError:
            return False

      cur = self.conn.cursor()
      data = cur.execute(
         """   SELECT
                  START_DATE,
                  END_DATE
               FROM ZooUpdate
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         (
            title,
            start_date
         ) )
      current_update = data.fetchone()

      if current_update == None:
         cur.close()
         return False

      current_start_date = zoo.ZooUtil.parse_date_value( current_update[ 'START_DATE' ] )

      if should_update_end_date and parsed_end_date == None:
         next_end_date = None
      else:
         next_end_date = parsed_end_date.isoformat() if parsed_end_date != None else current_update[ 'END_DATE' ]

      if parsed_end_date != None and parsed_end_date < current_start_date:
         cur.close()
         return False

      update_fields = []
      update_values = []

      if description != None and str( description ).strip():
         update_fields.append( 'DESCRIPTION = ?' )
         update_values.append( str( description ).strip() )

      if normalized_update_type != None:
         update_fields.append( 'UPDATE_TYPE = ?' )
         update_values.append( normalized_update_type )

      if should_update_end_date:
         update_fields.append( 'END_DATE = ?' )
         update_values.append( next_end_date )

      if not update_fields:
         cur.close()
         return False

      update_values.extend( [ title, start_date ] )

      cur.execute(
         f"""  UPDATE ZooUpdate
               SET { ', '.join( update_fields ) }
               WHERE TITLE = ?
                  AND START_DATE = ?;
         """,
         tuple( update_values ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


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
            zoo.ZooUtil.parse_date_value( value=start_date ).isoformat()
            if start_date
            else datetime.now().date().isoformat()
         )
      except ValueError:
         return False

      normalized_end_date = None

      if end_date:
         try:
            normalized_end_date = zoo.ZooUtil.parse_date_value( value=end_date ).isoformat()
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
