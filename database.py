import sqlite3
import zoo
from datetime import date, datetime


################################################################################

class Database():
   def __init__( self ):
      self.conn = sqlite3.connect( 'animals.db' )
      self.conn.row_factory = sqlite3.Row
      self.zoo_util = zoo.Zoo_Util()


   # Returns all animals which may be viewable in the given month with their likelihoods (probability from 0 to 1)
   def get_animals_viewable_on_day(
         self,
         month,
         day,
         temp=None,
         include_off_display_animals=False,
         threshold=0,
         species_to_include=[],
         itinerary_mode=False ):
      cur = self.conn.cursor()

      if temp is None:
         temp = self.zoo_util.get_average_temperature( month=month, day=day )
         sigma = 3
      else:
         sigma = 2

      snow_likelihood = self.zoo_util.get_snow_likelihood( month=month, day=day )

      target_date = date( datetime.now().year, self.zoo_util.get_month_int( month=month ), int( day ) )

      data = cur.execute(
         """   SELECT
                  a.SPECIES,
                  a.LATIN_NAME,
                  a.MIN_TEMPERATURE,
                  a.SNOW_RESISTANCE,
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
                  e.PART_OF_SEASONAL_EXHIBIT,
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
                  es.CLOSED_END
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
                  ON e.EXHIBIT = es.EXHIBIT;
         """ )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         species = animal['SPECIES']
         exhibit = animal['EXHIBIT']

         min_temperature = animal['MIN_TEMPERATURE']
         snow_resistance = animal['SNOW_RESISTANCE']
         part_of_seasonal_exhibit = animal['PART_OF_SEASONAL_EXHIBIT']
         enclosure_type = animal['ENCLOSURE_TYPE']
         seasonally_off_display_message = animal['SEASONALLY_OFF_DISPLAY_MESSAGE']

         is_off_display, off_display_message = self.get_active_off_display_status( animal=animal, target_date=target_date )

         has_limited_viewing_schedule, limited_viewing_message = self.get_active_limited_viewing_status(
            animal=animal,
            target_date=target_date )

         has_viewing_alert, viewing_alert_message = self.get_active_viewing_alert_status(
            animal=animal,
            target_date=target_date )

         is_exhibit_closed, exhibit_closed_message = self.get_active_exhibit_closed_status( animal=animal, target_date=target_date )

         if is_off_display or is_exhibit_closed:
            likelihood = 0
         else:
            likelihood = self.calculate_animal_likelihood(
               month=month,
               day=day,
               temp=temp,
               sigma=sigma,
               snow_likelihood=snow_likelihood,
               min_temperature=min_temperature,
               snow_resistance=snow_resistance,
               enclosure_type=enclosure_type,
               part_of_seasonal_exhibit=part_of_seasonal_exhibit,
               exhibit=exhibit )

         should_include = False

         if not itinerary_mode:

            should_include = (
               (likelihood > threshold)
               or (include_off_display_animals and likelihood == 0)
               or species in species_to_include
            )

         else:
            should_include = species in species_to_include

         if should_include:
            display_message = None

            if is_off_display:
               display_message = off_display_message
            elif is_exhibit_closed:
               display_message = exhibit_closed_message
            elif likelihood == 0:
               if seasonally_off_display_message:
                  display_message = seasonally_off_display_message
               else:
                  display_message = f'The {species} is off display due to cold weather.'

            animals.append(
               zoo.Animal(
                  species=species,
                  latin_name=animal['LATIN_NAME'],
                  general_viewing_tips=animal['GENERAL_VIEWING_TIPS'],
                  seasonal_viewing_tips=animal['SEASONAL_VIEWING_TIPS'],
                  identification=animal['IDENTIFICATION'],
                  habitat_and_range=animal['HABITAT_AND_RANGE'],
                  diet_and_feeding=animal['DIET_AND_FEEDING'],
                  behaviour_and_life_cycle=animal['BEHAVIOUR_AND_SOCIAL_LIFE'],
                  adaptations=animal['ADAPTATIONS'],
                  reproduction_and_life_cycle=animal['REPRODUCTION_AND_LIFE_CYCLE'],
                  animals_at_the_zoo=animal['ANIMALS_AT_THE_ZOO'],
                  exhibit=exhibit,
                  seasonal_viewing_summary=animal['SEASONAL_VIEWING_SUMMARY'],
                  seasonal_viewing_information=animal['SEASONAL_VIEWING_INFORMATION'],
                  off_display_message=display_message,
                  enclosure_type=enclosure_type,
                  x_coord=animal['X_COORD'],
                  y_coord=animal['Y_COORD'],
                  likelihood=likelihood,
                  has_limited_viewing_schedule=has_limited_viewing_schedule,
                  limited_viewing_message=limited_viewing_message,
                  has_viewing_alert=has_viewing_alert,
                  viewing_alert_message=viewing_alert_message ) )
            
      cur.close()

      return animals


   def get_active_off_display_status( self, animal, target_date ):
      stored_is_off_display = bool( animal['IS_OFF_DISPLAY'] ) if animal['IS_OFF_DISPLAY'] != None else False

      if not stored_is_off_display:
         return False, None

      off_display_message = animal['OFF_DISPLAY_MESSAGE']
      off_display_start = animal['OFF_DISPLAY_START']
      off_display_end = animal['OFF_DISPLAY_END']

      is_off_display = self.is_date_in_range(
         target_date=target_date,
         start_date_value=off_display_start,
         end_date_value=off_display_end )

      if is_off_display:
         return True, off_display_message

      return False, None


   def get_active_limited_viewing_status( self, animal, target_date ):
      schedule_start_date = animal['SCHEDULE_START_DATE']
      schedule_end_date = animal['SCHEDULE_END_DATE']
      daily_start_time = animal['DAILY_START_TIME']
      daily_end_time = animal['DAILY_END_TIME']
      viewing_message = animal['VIEWING_MESSAGE']

      if daily_start_time == None or daily_end_time == None:
         return False, None

      is_active = self.is_date_in_range( target_date=target_date, start_date_value=schedule_start_date, end_date_value=schedule_end_date )

      if is_active:
         return True, viewing_message

      return False, None


   def get_active_viewing_alert_status( self, animal, target_date ):
      alert_message = animal['ALERT_MESSAGE']
      alert_start_date = animal['ALERT_START_DATE']
      alert_end_date = animal['ALERT_END_DATE']

      if alert_message == None:
         return False, None

      is_active = self.is_date_in_range( target_date=target_date, start_date_value=alert_start_date, end_date_value=alert_end_date )

      if is_active:
         return True, alert_message

      return False, None


   def get_active_exhibit_closed_status( self, animal, target_date ):
      stored_is_closed = bool( animal['IS_CLOSED'] ) if animal['IS_CLOSED'] != None else False

      if not stored_is_closed:
         return False, None

      closed_message = animal['CLOSED_MESSAGE']
      closed_start = animal['CLOSED_START']
      closed_end = animal['CLOSED_END']

      is_closed = self.is_date_in_range( target_date=target_date, start_date_value=closed_start, end_date_value=closed_end )

      if is_closed:
         return True, closed_message

      return False, None


   def calculate_animal_likelihood(
         self,
         month,
         day,
         temp,
         sigma,
         snow_likelihood,
         min_temperature,
         snow_resistance,
         enclosure_type,
         part_of_seasonal_exhibit,
         exhibit ):
      if enclosure_type == 'Outdoor':

         avg_temp = self.zoo_util.get_average_temperature( month=month, day=day )
         effective_temp = avg_temp + 0.5 * (temp - avg_temp)

         likelihood = self.zoo_util.get_temperature_probability( mu=effective_temp, sigma=sigma, min_temperature=min_temperature )
         likelihood = likelihood - (1.0 - snow_resistance) * snow_likelihood

      else:
         likelihood = 1

      if part_of_seasonal_exhibit:
         likelihood = likelihood * self.get_exhibit_likelihood( exhibit=exhibit, month=month, day=day )

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

      raise ValueError( f'Unsupported datetime format: {value}' )
   

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

      date_part = value.split( ' ' )[0]

      try:
         return date.fromisoformat( date_part )
      except ValueError:
         pass

      raise ValueError( f'Unsupported date format: {value}' )


   def get_exhibit_likelihood( self, exhibit, month, day ):
      next_month = self.zoo_util.get_next_month( month=month )

      month_likelihood = self.get_exhibit_month_likelihood( exhibit=exhibit, month=month )
      next_month_likelihood = self.get_exhibit_month_likelihood( exhibit=exhibit, month=next_month )

      days_in_month = self.zoo_util.get_number_of_days_in_month( month=month )
      
      return month_likelihood + (next_month_likelihood - month_likelihood) / (days_in_month - 1) * (day - 1)
      

   def get_exhibit_month_likelihood( self, exhibit, month ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  e.{month}_PROBABILITY
               FROM Exhibit e
               WHERE e.NAME = ?;
         """, (exhibit, ) )
            
      exhibit_probability = data.fetchone()[0]
      cur.close()

      return exhibit_probability
   

   def get_exhibits_in_region( self, region ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  e.NAME
               FROM Exhibit e
               WHERE e.REGION = ?;
         """, (region, ) )
      
      exhibits = [row[0] for row in data.fetchall()]
      cur.close()

      return exhibits
   

   def get_animals_in_exhibit( self, exhibit ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  a.SPECIES
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               WHERE e.EXHIBIT = ?
         """, (exhibit, ) )

      animals = [row[0] for row in data.fetchall()]

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
         latin_name = animal['LATIN_NAME'],
         general_viewing_tips = animal['GENERAL_VIEWING_TIPS'],
         seasonal_viewing_tips = animal['SEASONAL_VIEWING_TIPS'],
         identification = animal['IDENTIFICATION'],
         habitat_and_range = animal['HABITAT_AND_RANGE'],
         diet_and_feeding = animal['DIET_AND_FEEDING'],
         behaviour_and_life_cycle = animal['BEHAVIOUR_AND_SOCIAL_LIFE'],
         adaptations = animal['ADAPTATIONS'],
         reproduction_and_life_cycle = animal['REPRODUCTION_AND_LIFE_CYCLE'],
         animals_at_the_zoo = animal['ANIMALS_AT_THE_ZOO'],
         exhibit = animal['EXHIBIT'],
         seasonal_viewing_summary = animal['SEASONAL_VIEWING_SUMMARY'],
         seasonal_viewing_information = animal['SEASONAL_VIEWING_INFORMATION'] )

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
               name=pavilion['NAME'],
               region=pavilion['REGION'],
               description=pavilion['DESCRIPTION'],
               x_coord=pavilion['X_COORD'],
               y_coord=pavilion['Y_COORD'] ) )

      cur.close()

      return pavilions
   

   def get_restaurants( self, month, day, include_closed_restaurants, restaurants_to_include=[] ):
      cur = self.conn.cursor()

      target_date = date( datetime.now().year, self.zoo_util.get_month_int( month=month ), int( day ) )

      data = cur.execute(
         """   SELECT
                  r.NAME,
                  r.LOCATION,
                  r.SUB_LOCATION,
                  r.DESCRIPTION,
                  r.MENU_LINK,
                  r.X_COORD,
                  r.Y_COORD,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE,
                  s.CLOSED_START,
                  s.CLOSED_END,
                  os.SCHEDULE_START_DATE,
                  os.SCHEDULE_END_DATE,
                  os.MONDAY,
                  os.TUESDAY,
                  os.WEDNESDAY,
                  os.THURSDAY,
                  os.FRIDAY,
                  os.SATURDAY,
                  os.SUNDAY,
                  os.HOLIDAYS_ONLY,
                  os.SCHEDULE_MESSAGE
               FROM Restaurant r
               LEFT JOIN RestaurantStatus s
                  ON r.NAME = s.RESTAURANT
               LEFT JOIN RestaurantOpeningSchedule os
                  ON r.NAME = os.RESTAURANT;
         """ )

      restaurant_data = data.fetchall()

      restaurants = []

      for restaurant in restaurant_data:
         name = restaurant['NAME']

         stored_is_closed = bool( restaurant['IS_CLOSED'] ) if restaurant['IS_CLOSED'] != None else False

         is_closed = False
         closed_message = None

         if stored_is_closed:
            start_ok = True
            end_ok = True

            if restaurant['CLOSED_START'] != None:
               start_date = self.parse_date_value( value=restaurant['CLOSED_START'] )
               start_ok = target_date >= start_date

            if restaurant['CLOSED_END'] != None:
               end_date = self.parse_date_value( value=restaurant['CLOSED_END'] )
               end_ok = target_date <= end_date

            if start_ok and end_ok:
               is_closed = True
               closed_message = restaurant['CLOSED_MESSAGE']

         if not is_closed and restaurant['SCHEDULE_START_DATE'] != None:
            schedule_start_ok = True
            schedule_end_ok = True

            if restaurant['SCHEDULE_START_DATE'] != None:
               schedule_start_date = self.parse_date_value( value=restaurant['SCHEDULE_START_DATE'] )
               schedule_start_ok = target_date >= schedule_start_date

            if restaurant['SCHEDULE_END_DATE'] != None:
               schedule_end_date = self.parse_date_value( value=restaurant['SCHEDULE_END_DATE'] )
               schedule_end_ok = target_date <= schedule_end_date

            if schedule_start_ok and schedule_end_ok:
               is_open_today = False

               if self.zoo_util.is_holiday( d=target_date ):
                  is_open_today = bool( restaurant['HOLIDAYS_ONLY'] )

               if not is_open_today:
                  day_of_week = target_date.weekday()

                  if day_of_week == 0:
                     is_open_today = bool( restaurant['MONDAY'] )
                  elif day_of_week == 1:
                     is_open_today = bool( restaurant['TUESDAY'] )
                  elif day_of_week == 2:
                     is_open_today = bool( restaurant['WEDNESDAY'] )
                  elif day_of_week == 3:
                     is_open_today = bool( restaurant['THURSDAY'] )
                  elif day_of_week == 4:
                     is_open_today = bool( restaurant['FRIDAY'] )
                  elif day_of_week == 5:
                     is_open_today = bool( restaurant['SATURDAY'] )
                  elif day_of_week == 6:
                     is_open_today = bool( restaurant['SUNDAY'] )

               if not is_open_today:
                  is_closed = True
                  closed_message = restaurant['SCHEDULE_MESSAGE']

         if include_closed_restaurants or not is_closed or name in restaurants_to_include:
            restaurants.append(
               zoo.Restaurant(
                  name=name,
                  location=restaurant['LOCATION'],
                  sub_location=restaurant['SUB_LOCATION'],
                  description=restaurant['DESCRIPTION'],
                  menu_link=restaurant['MENU_LINK'],
                  x_coord=restaurant['X_COORD'],
                  y_coord=restaurant['Y_COORD'],
                  is_closed=is_closed,
                  closed_message=closed_message ) )

      cur.close()

      return restaurants
   

   def get_restrooms( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  r.TITLE,
                  r.X_COORD,
                  r.Y_COORD
               FROM Restroom r;
         """ )

      restroom_data = data.fetchall()

      restrooms = []

      for restroom in restroom_data:
         restrooms.append(
            zoo.Restroom(
               title=restroom['TITLE'],
               x_coord=restroom['X_COORD'],
               y_coord=restroom['Y_COORD'] ) )

      cur.close()

      return restrooms
   

   def get_gift_shops( self, month, day, include_closed_gift_shops, gift_shops_to_include=[] ):
      cur = self.conn.cursor()

      target_date = date( datetime.now().year, self.zoo_util.get_month_int( month ), int( day ) )

      data = cur.execute(
         """   SELECT
                  g.NAME,
                  g.LOCATION,
                  g.DESCRIPTION,
                  g.X_COORD,
                  g.Y_COORD,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE,
                  s.CLOSED_START,
                  s.CLOSED_END,
                  os.SCHEDULE_START_DATE,
                  os.SCHEDULE_END_DATE,
                  os.MONDAY,
                  os.TUESDAY,
                  os.WEDNESDAY,
                  os.THURSDAY,
                  os.FRIDAY,
                  os.SATURDAY,
                  os.SUNDAY,
                  os.HOLIDAYS_ONLY,
                  os.SCHEDULE_MESSAGE
               FROM GiftShop g
               LEFT JOIN GiftShopStatus s
                  ON g.NAME = s.GIFT_SHOP
               LEFT JOIN GiftShopOpeningSchedule os
                  ON g.NAME = os.GIFT_SHOP;
         """ )

      gift_shop_data = data.fetchall()

      gift_shops = []

      for gift_shop in gift_shop_data:
         name = gift_shop['NAME']

         stored_is_closed = bool( gift_shop['IS_CLOSED'] ) if gift_shop['IS_CLOSED'] != None else False

         is_closed = False
         closed_message = None

         if stored_is_closed:
            start_ok = True
            end_ok = True

            if gift_shop['CLOSED_START'] != None:
               start_date = self.parse_date_value( value=gift_shop['CLOSED_START'] )
               start_ok = target_date >= start_date

            if gift_shop['CLOSED_END'] != None:
               end_date = self.parse_date_value( value=gift_shop['CLOSED_END'] )
               end_ok = target_date <= end_date

            if start_ok and end_ok:
               is_closed = True
               closed_message = gift_shop['CLOSED_MESSAGE']

         if not is_closed and gift_shop['SCHEDULE_START_DATE'] != None:
            schedule_start_ok = True
            schedule_end_ok = True

            if gift_shop['SCHEDULE_START_DATE'] != None:
               schedule_start_date = self.parse_date_value( value=gift_shop['SCHEDULE_START_DATE'] )
               schedule_start_ok = target_date >= schedule_start_date

            if gift_shop['SCHEDULE_END_DATE'] != None:
               schedule_end_date = self.parse_date_value( value=gift_shop['SCHEDULE_END_DATE'] )
               schedule_end_ok = target_date <= schedule_end_date

            if schedule_start_ok and schedule_end_ok:
               is_open_today = False

               if self.zoo_util.is_holiday( target_date ):
                  is_open_today = bool( gift_shop['HOLIDAYS_ONLY'] )

               if not is_open_today:
                  day_of_week = target_date.weekday()

                  if day_of_week == 0:
                     is_open_today = bool( gift_shop['MONDAY'] )
                  elif day_of_week == 1:
                     is_open_today = bool( gift_shop['TUESDAY'] )
                  elif day_of_week == 2:
                     is_open_today = bool( gift_shop['WEDNESDAY'] )
                  elif day_of_week == 3:
                     is_open_today = bool( gift_shop['THURSDAY'] )
                  elif day_of_week == 4:
                     is_open_today = bool( gift_shop['FRIDAY'] )
                  elif day_of_week == 5:
                     is_open_today = bool( gift_shop['SATURDAY'] )
                  elif day_of_week == 6:
                     is_open_today = bool( gift_shop['SUNDAY'] )

               if not is_open_today:
                  is_closed = True
                  closed_message = gift_shop['SCHEDULE_MESSAGE']

         if include_closed_gift_shops or not is_closed or name in gift_shops_to_include:
            gift_shops.append(
               zoo.GiftShop(
                  name=name,
                  location=gift_shop['LOCATION'],
                  description=gift_shop['DESCRIPTION'],
                  x_coord=gift_shop['X_COORD'],
                  y_coord=gift_shop['Y_COORD'],
                  is_closed=is_closed,
                  closed_message=closed_message ) )

      cur.close()

      return gift_shops
   

   def get_attractions( self, month, day, include_closed_attractions=False, attractions_to_include=[], itinerary_mode=False ):
      cur = self.conn.cursor()

      target_date = date( datetime.now().year, self.zoo_util.get_month_int( month ), int( day ) )
      weekday = target_date.weekday()

      data = cur.execute(
         """   SELECT
                  a.NAME,
                  a.FREE_WITH_ADMISSION,
                  a.DESCRIPTION,
                  a.INFO_LINK,
                  a.HYPERLINK_TEXT,
                  a.X_COORD,
                  a.Y_COORD,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE,
                  s.CLOSED_START,
                  s.CLOSED_END
               FROM Attraction a
               LEFT JOIN AttractionStatus s
                  ON a.NAME = s.ATTRACTION;
         """ )

      attraction_data = data.fetchall()

      attractions = []

      for attraction in attraction_data:
         name = attraction['NAME']

         is_closed = self.is_attraction_manually_closed( attraction=attraction, target_date=target_date )
         closed_message = attraction['CLOSED_MESSAGE'] if is_closed else None

         if not is_closed:
            is_closed, schedule_message = self.is_attraction_closed_by_schedule(
               attraction_name=name,
               target_date=target_date,
               weekday=weekday )

            if is_closed:
               closed_message = schedule_message

         should_include = False

         if not itinerary_mode:
            should_include = (
               (not is_closed)
               or include_closed_attractions
               or name in attractions_to_include
            )
         else:
            should_include = name in attractions_to_include

         if not should_include:
            continue

         attractions.append(
            zoo.Attraction(
               name=name,
               free_with_admission=attraction['FREE_WITH_ADMISSION'],
               description=attraction['DESCRIPTION'],
               info_link=attraction['INFO_LINK'],
               hyperlink_text=attraction['HYPERLINK_TEXT'],
               x_coord=attraction['X_COORD'],
               y_coord=attraction['Y_COORD'],
               is_closed=is_closed,
               closed_message=closed_message ) )

      cur.close()

      return attractions


   def is_attraction_manually_closed( self, attraction, target_date ):
      stored_is_closed = bool( attraction['IS_CLOSED'] ) if attraction['IS_CLOSED'] != None else False

      if not stored_is_closed:
         return False

      start_ok = True
      end_ok = True

      if attraction['CLOSED_START'] != None:
         start_date = self.parse_date_value( value=attraction['CLOSED_START'] )
         start_ok = target_date >= start_date

      if attraction['CLOSED_END'] != None:
         end_date = self.parse_date_value( value=attraction['CLOSED_END'] )
         end_ok = target_date <= end_date

      return start_ok and end_ok


   def is_attraction_closed_by_schedule( self, attraction_name, target_date, weekday ):
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
         return False, None

      for schedule in schedule_rows:
         start_ok = True
         end_ok = True

         if schedule['SCHEDULE_START_DATE'] != None:
            start_date = self.parse_date_value( value=schedule['SCHEDULE_START_DATE'] )
            start_ok = target_date >= start_date

         if schedule['SCHEDULE_END_DATE'] != None:
            end_date = self.parse_date_value( value=schedule['SCHEDULE_END_DATE'] )
            end_ok = target_date <= end_date

         if not ( start_ok and end_ok ):
            continue

         is_holiday = self.zoo_util.is_holiday( d=target_date ) if hasattr( self.zoo_util, 'is_holiday' ) else False

         open_on_day = False

         if weekday == 0 and schedule['MONDAY']:
            open_on_day = True
         elif weekday == 1 and schedule['TUESDAY']:
            open_on_day = True
         elif weekday == 2 and schedule['WEDNESDAY']:
            open_on_day = True
         elif weekday == 3 and schedule['THURSDAY']:
            open_on_day = True
         elif weekday == 4 and schedule['FRIDAY']:
            open_on_day = True
         elif weekday == 5 and schedule['SATURDAY']:
            open_on_day = True
         elif weekday == 6 and schedule['SUNDAY']:
            open_on_day = True
         elif schedule['HOLIDAYS_ONLY'] and is_holiday:
            open_on_day = True

         if open_on_day:
            return False, None

         message = schedule['SCHEDULE_MESSAGE']

         if not message:
            if schedule['SATURDAY'] and schedule['SUNDAY'] and schedule['HOLIDAYS_ONLY']:
               message = f'The {attraction_name} is open on weekends and holidays only.'
            else:
               message = f'The {attraction_name} is not scheduled to be open today.'

         return True, message

      return False, None
   

   def get_zoomobile_stations( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  s.NAME,
                  s.X_COORD,
                  s.Y_COORD
               FROM ZoomobileStation s;
         """ )

      zoomobile_station_data = data.fetchall()

      zoomobile_stations = []

      for zoomobile_station in zoomobile_station_data:
         zoomobile_stations.append(
            zoo.ZoomobileStation(
               name=zoomobile_station['NAME'],
               x_coord=zoomobile_station['X_COORD'],
               y_coord=zoomobile_station['Y_COORD'] ) )

      cur.close()

      return zoomobile_stations


   def get_zoomobile_route( self, route_type, zoomobile_stations_to_include=[] ):
      cur = self.conn.cursor()

      # Zoomobile stations
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
         name = zoomobile_station['NAME']
         on_winter_route = zoomobile_station['ON_WINTER_ROUTE']

         if route_type == 'summer' or on_winter_route or name in zoomobile_stations_to_include:
            zoomobile_stations.append(
               zoo.ZoomobileStation(
                  name=name,
                  description=zoomobile_station['DESCRIPTION'],
                  x_coord=zoomobile_station['X_COORD'],
                  y_coord=zoomobile_station['Y_COORD'] ) )

      # Zoomobile route markers
      data = cur.execute(
         """   SELECT
                  m.ON_WINTER_ROUTE,
                  m.ON_SUMMER_ROUTE,
                  m.X_COORD,
                  m.Y_COORD
               FROM ZoomobileRouteMarker m;
         """ )

      zoomobile_route_marker_data = data.fetchall()

      zoomobile_route_markers = []

      for zoomobile_route_marker in zoomobile_route_marker_data:
         on_winter_route = zoomobile_route_marker['ON_WINTER_ROUTE']
         on_summer_route = zoomobile_route_marker['ON_SUMMER_ROUTE']

         if (route_type == 'winter' and on_winter_route) or (route_type == 'summer' and on_summer_route):
            zoomobile_route_markers.append(
               zoo.ZoomobileRouteMarker(
                  route_type=route_type,
                  x_coord=zoomobile_route_marker['X_COORD'],
                  y_coord=zoomobile_route_marker['Y_COORD'] ) )

      cur.close()

      return [ zoomobile_stations, zoomobile_route_markers ]


   def get_meet_the_guardians_talks( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  t.NAME,
                  t.LOCATION,
                  t.X_COORD,
                  t.Y_COORD
               FROM MeetTheGuardiansTalk t;
         """ )

      meet_the_guardians_talk_data = data.fetchall()

      meet_the_guardians_talks = []

      for meet_the_guardians_talk in meet_the_guardians_talk_data:
         meet_the_guardians_talks.append(
            zoo.MeetTheGuardiansTalk(
               name=meet_the_guardians_talk['NAME'],
               location=meet_the_guardians_talk['LOCATION'],
               x_coord=meet_the_guardians_talk['X_COORD'],
               y_coord=meet_the_guardians_talk['Y_COORD'] ) )

      cur.close()

      return meet_the_guardians_talks


   def get_meet_the_guardians_talks_with_date_times( self, meet_the_guardians_talks_to_include=[], itinerary_mode=False ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  t.NAME,
                  t.LOCATION,
                  t.X_COORD,
                  t.Y_COORD,
                  d.DAY_OF_WEEK,
                  d.TIME_OF_DAY
               FROM MeetTheGuardiansTalk t
               JOIN MeetTheGuardiansTalkDateTime d
                  ON t.NAME = d.NAME;
         """ )
      
      meet_the_guardians_talk_data = data.fetchall()

      meet_the_guardians_talks = []

      for meet_the_guardians_talk in meet_the_guardians_talk_data:
         name = meet_the_guardians_talk['NAME']

         if not itinerary_mode or name in meet_the_guardians_talks_to_include:
            meet_the_guardians_talks.append(
               zoo.MeetTheGuardiansTalk(
                  name=name,
                  location=meet_the_guardians_talk['LOCATION'],
                  x_coord=meet_the_guardians_talk['X_COORD'],
                  y_coord=meet_the_guardians_talk['Y_COORD'],
                  day_of_week=meet_the_guardians_talk['DAY_OF_WEEK'],
                  time_of_day=meet_the_guardians_talk['TIME_OF_DAY'] ) )

      cur.close()

      return meet_the_guardians_talks
   

   def get_wild_encounter_meeting_spots( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  w.NAME,
                  w.X_COORD,
                  w.Y_COORD
               FROM WildEncounterMeetingSpot w;
         """ )
      
      wild_encounter_meeting_spot_data = data.fetchall()

      wild_encounter_meeting_spots = []

      for wild_encounter_meeting_spot in wild_encounter_meeting_spot_data:
         wild_encounter_meeting_spots.append(
            zoo.WildEncounterMeetingSpot(
               name=wild_encounter_meeting_spot['NAME'],
               x_coord=wild_encounter_meeting_spot['X_COORD'],
               y_coord=wild_encounter_meeting_spot['Y_COORD'] ) )

      cur.close()

      return wild_encounter_meeting_spots
   

   def get_wild_encounter_meeting_spots_for_wild_encounters( self, wild_encounters_to_include ):
      cur = self.conn.cursor()

      wild_encounters = []

      for wild_encounter in wild_encounters_to_include:
         cur.execute(
            """   SELECT
                     m.NAME,
                     m.X_COORD,
                     m.Y_COORD,
                     w.LINK
                  FROM WildEncounterMeetingSpot m
                  JOIN WildEncounter w
                     ON m.NAME = w.MEETING_SPOT
                  WHERE w.NAME = ?;
            """,
            ( wild_encounter, ) )

         wild_encounter_data = cur.fetchone()

         wild_encounters.append(
            zoo.WildEncounter(
               name=wild_encounter,
               meeting_spot=wild_encounter_data['NAME'],
               x_coord=wild_encounter_data['X_COORD'],
               y_coord=wild_encounter_data['Y_COORD'],
               link=wild_encounter_data['LINK'] ) )

      cur.close()

      return wild_encounters
   

   def get_wild_encounters( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  w.NAME,
                  w.MEETING_SPOT,
                  w.LINK,
                  m.DAY_OF_WEEK,
                  m.TIME_OF_DAY
               FROM WildEncounter w
               JOIN WildEncounterMeetingTime m
                  ON w.NAME = m.NAME;
         """ )

      wild_encounter_data = data.fetchall()

      wild_encounters = []

      for wild_encounter in wild_encounter_data:
         wild_encounters.append(
            zoo.WildEncounter(
               name=wild_encounter['NAME'],
               meeting_spot=wild_encounter['MEETING_SPOT'],
               link=wild_encounter['LINK'],
               day_of_week=wild_encounter['DAY_OF_WEEK'],
               time_of_day=wild_encounter['TIME_OF_DAY'] ) )

      cur.close()

      return wild_encounters
   

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

         if current is None or (a.likelihood or 0) > (current.likelihood or 0):
            best_by_species[species] = a

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
   

   def get_restrooms_matching_query( self, query ):
      if not query:
         return self.get_restrooms()

      query_lower = query.lower()

      return [
         r for r in self.get_restrooms()
         if r.title and query_lower in r.title.lower()
      ]
   

   def get_gift_shops_matching_query( self, query, month ):
      if not query:
         return self.get_gift_shops( month, include_seasonal_gift_shops=True )

      query_lower = query.lower()

      return [
         g for g in self.get_gift_shops( month, include_seasonal_gift_shops=True )
         if g.name and query_lower in g.name.lower()
      ]
   

   def get_attractions_matching_query( self, query, month, include_closed_attractions ):
      if not query:
         return self.get_attractions( month, include_closed_attractions=include_closed_attractions )

      query_lower = query.lower()

      return [
         a for a in self.get_attractions( month, include_closed_attractions=include_closed_attractions )
         if a.name and query_lower in a.name.lower()
      ]
   

   def get_zoomobile_stations_matching_query( self, query ):
      if not query:
         return self.get_zoomobile_stations()

      query_lower = query.lower()

      return [
         s for s in self.get_zoomobile_stations()
         if s.name and query_lower in s.name.lower()
      ]
   

   def get_meet_the_guardians_talks_with_date_times_matching_query( self, query, day_of_week=None ):
      talks = self.get_meet_the_guardians_talks_with_date_times()

      if not query:
         return [
            t for t in talks
            if day_of_week is None or t.day_of_week == day_of_week
         ]

      query_lower = query.lower()

      return [
         t for t in talks
         if (
            t.name
            and query_lower in t.name.lower()
            and (day_of_week is None or t.day_of_week == day_of_week)
         )
      ]
   

   def get_wild_encounter_meeting_spots_matching_query( self, query ):
      if not query:
         return self.get_wild_encounter_meeting_spots()

      query_lower = query.lower()

      return [
         m for m in self.get_wild_encounter_meeting_spots()
         if m.name and query_lower in m.name.lower()
      ]
   

   def get_wild_encounters_matching_query( self, query, day_of_week=None ):
      encounters = self.get_wild_encounters()

      if not query:
         return [
            w for w in encounters
            if day_of_week is None or w.day_of_week == day_of_week
         ]

      query_lower = query.lower()

      return [
         w for w in encounters
         if (
            w.name
            and query_lower in w.name.lower()
            and (day_of_week is None or w.day_of_week == day_of_week)
         )
      ]
   

   def get_species( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  a.SPECIES
               FROM Animal a;
         """ )
      
      species = [row[0] for row in data.fetchall()]
      cur.close()

      return species
   

   def get_exhibits( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  e.NAME
               FROM Exhibit e;
         """ )
      
      exhibits = [row[0] for row in data.fetchall()]
      cur.close()

      return exhibits
   

   def get_restaurant_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  r.NAME
               FROm Restaurant r;
         """ )

      restaurants = [row[0] for row in data.fetchall()]
      cur.close()

      return restaurants
   

   def get_gift_shop_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  g.NAME
               FROm GiftShop g;
         """ )

      gift_shops = [row[0] for row in data.fetchall()]
      cur.close()

      return gift_shops
   

   def get_attraction_names( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         f"""  SELECT
                  a.NAME
               FROm Attraction a;
         """ )

      attractions = [row[0] for row in data.fetchall()]
      cur.close()

      return attractions
   

   def set_animal_as_off_display( self, species, exhibit, start_date, end_date, message ):
      if not message:
         message = f'The {species} is temporarily off-display.'

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
         """, (species, exhibit, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
   

   def set_animal_limited_viewing_schedule( self, species, exhibit, schedule_start_date, schedule_end_date, daily_start_time,
                                            daily_end_time, message ):
      if not schedule_start_date:
         schedule_start_date = datetime.now().date().isoformat()

      if not schedule_end_date:
         schedule_end_date = None

      if not daily_start_time or not daily_end_time:
         return False

      if not message:

         formatted_daily_start_time = datetime.strptime( daily_start_time, '%H:%M' ).strftime( '%I:%M %p' ).lstrip( '0' )
         formatted_daily_end_time = datetime.strptime( daily_end_time, '%H:%M' ).strftime( '%I:%M %p' ).lstrip( '0' )

         if schedule_end_date != None:

            formatted_schedule_end_date = datetime.strptime( schedule_end_date, '%Y-%m-%d' ).strftime( '%A, %B %d, %Y' )

            message = (
               f'The {species} is viewable daily only from {formatted_daily_start_time} to {formatted_daily_end_time} '
               f'until {formatted_schedule_end_date}.'
            )

         else:
            message = (
               f'The {species} is viewable daily only from {formatted_daily_start_time} to {formatted_daily_end_time}.'
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
         """, ( species, exhibit, schedule_start_date, schedule_end_date, daily_start_time, daily_end_time, message ) )

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
         message = f'The {species} may be less visible than usual at this time.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO AnimalViewingAlert (
                  SPECIES,
                  EXHIBIT,
                  ALERT_MESSAGE,
                  ALERT_START_DATE,
                  ALERT_END_DATE
               )
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(SPECIES, EXHIBIT) DO UPDATE SET
                  ALERT_MESSAGE = excluded.ALERT_MESSAGE,
                  ALERT_START_DATE = excluded.ALERT_START_DATE,
                  ALERT_END_DATE = excluded.ALERT_END_DATE;
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
         message = f'The {exhibit} is temporarily closed.'

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
   

   def set_exhibit_as_open( self, exhibit ):
      if not exhibit:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """ DELETE FROM ExhibitStatus
            WHERE EXHIBIT = ?;
         """, ( exhibit, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
   

   def set_restaurant_as_closed( self, restaurant, start_date, end_date, message ):
      if not restaurant:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The {restaurant} is temporarily closed.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO RestaurantStatus (
                  RESTAURANT,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(RESTAURANT) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( restaurant, message, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_restaurant_as_open( self, restaurant ):
      if not restaurant:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM RestaurantStatus
               WHERE RESTAURANT = ?;
         """, ( restaurant, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
   

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
         message = f'The {restaurant} is not scheduled to be open today.'

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
   

   def remove_restaurant_opening_schedule( self, restaurant ):
      if not restaurant:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM RestaurantOpeningSchedule
               WHERE RESTAURANT = ?;
         """, ( restaurant, ) )

      self.conn.commit()
      removed = cur.rowcount
      cur.close()

      return removed > 0


   def set_gift_shop_as_closed( self, gift_shop, start_date, end_date, message ):
      if not gift_shop:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The {gift_shop} is temporarily closed.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO GiftShopStatus (
                  GIFT_SHOP,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(GIFT_SHOP) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( gift_shop, message, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0


   def set_gift_shop_as_open( self, gift_shop ):
      if not gift_shop:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM GiftShopStatus
               WHERE RESTAURANT = ?;
         """, ( gift_shop, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
   

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
         message = f'The {gift_shop} is not scheduled to be open today.'

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
   

   def remove_gift_shop_opening_schedule( self, gift_shop ):
      if not gift_shop:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM GiftShopOpeningSchedule
               WHERE RESTAURANT = ?;
         """, ( gift_shop, ) )

      self.conn.commit()
      removed = cur.rowcount
      cur.close()

      return removed > 0
   

   def set_attraction_as_closed( self, attraction, start_date, end_date, message ):
      if not attraction:
         return False

      if not start_date:
         start_date = datetime.now().date().isoformat()

      if not end_date:
         end_date = None

      if not message:
         message = f'The {attraction} is temporarily closed.'

      cur = self.conn.cursor()

      cur.execute(
         """   INSERT INTO AttractionStatus (
                  ATTRACTION,
                  IS_CLOSED,
                  CLOSED_MESSAGE,
                  CLOSED_START,
                  CLOSED_END
               )
               VALUES (?, 1, ?, ?, ?)
               ON CONFLICT(ATTRACTION) DO UPDATE SET
                  IS_CLOSED = 1,
                  CLOSED_MESSAGE = excluded.CLOSED_MESSAGE,
                  CLOSED_START = excluded.CLOSED_START,
                  CLOSED_END = excluded.CLOSED_END;
         """, ( attraction, message, start_date, end_date ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
   

   def set_attraction_as_open( self, attraction ):
      if not attraction:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM AttractionStatus
               WHERE ATTRACTION = ?;
         """, ( attraction, ) )

      self.conn.commit()
      updated = cur.rowcount
      cur.close()

      return updated > 0
   

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
         message = f'The {attraction} is not scheduled to be open today.'

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
   

   def remove_attraction_opening_schedule( self, attraction ):
      if not attraction:
         return False

      cur = self.conn.cursor()

      cur.execute(
         """   DELETE FROM AttractionOpeningSchedule
               WHERE ATTRACTION = ?;
         """, ( attraction, ) )

      self.conn.commit()
      removed = cur.rowcount
      cur.close()

      return removed > 0
   