import sqlite3
import zoo


################################################################################

class Database():
   def __init__( self ):
      self.conn = sqlite3.connect( 'animals.db' )
      self.zoo_util = zoo.Zoo_Util()


   # Returns all animals which may be viewable in the given month with their likelihoods (probability from 0 to 1)
   def get_animals_viewable_on_day( self, month, day, temp=None, include_off_display_animals=False, speciesToInclude = False ):
      cur = self.conn.cursor()

      if temp == None:
         temp = self.zoo_util.get_average_temperature( month, day )
         sigma = 3
      else:
         sigma = 2
      snow_likelihood = self.zoo_util.get_snow_likelihood( month, day )
   
      # We need to know whether the animal is viewable indoors and/or outdoors. If they are viewable in both, then we need to calculate
      # whether they are viewable outside or not in this case.
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
                  v.Y_COORD
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               JOIN EnclosureViewing v
                  ON e.SPECIES = v.SPECIES
                  AND e.EXHIBIT = v.EXHIBIT;
         """ )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         species = animal[0]
         exhibit = animal[13]
         min_temperature = animal[2]
         snow_resistance = animal[3]
         part_of_seasonal_exhibit = animal[14]
         enclosure_type = animal[17]

         if enclosure_type == 'Outdoor':
            # The initial likelihood to see the animal is calculating via a probability that the temperature is warm enough for the animal
            # to be on display, which is retrieved via a normal distribution
            likelihood = self.zoo_util.get_temperature_probability( temp, sigma, min_temperature )
            
            # We also adjust (decrease) the likelihood based on the probability of snow, and the animal's resistance to snow. The animal's
            # snow resistance is between 0 and 5. For every point below five, the animal's likelihood decreases by the 10% of the
            # probability of snow on that day. For example, if the animal's snow resistance is 3, and there is an 80% chance of snow, then
            # their likelihood decreases by .16.
            likelihood = likelihood - (5 - snow_resistance) / 10 * snow_likelihood
         else:
            likelihood = 1

         # We need to consider if the animal is a part of a seasonal exhibit, and whether that exhibit will be open on the specific day
         if part_of_seasonal_exhibit:
            # Get the probability that the exhibit is open, and scale the likelihood to that
            likelihood = likelihood * self.get_exhibit_likelihood( exhibit, month, day )

         likelihood = max( round( likelihood * 100 ), 0 )

         if likelihood > 0 or include_off_display_animals or species in speciesToInclude:
            animals.append( zoo.Animal( species=species, latin_name=animal[1], general_viewing_tips=animal[4],
                                        seasonal_viewing_tips=animal[5], identification=animal[6], habitat_and_range=animal[7],
                                        diet_and_feeding=animal[8], behaviour_and_life_cycle=animal[9], adaptations=animal[10],
                                        reproduction_and_life_cycle=animal[11], animals_at_the_zoo=animal[12], exhibit=exhibit,
                                        seasonal_viewing_summary=animal[15], seasonal_viewing_information=animal[16],
                                        seasonally_off_display_message=animal[18], enclosure_type=enclosure_type, x_coord=animal[19],
                                        y_coord=animal[20], likelihood=likelihood ) )

      cur.close()

      return animals
   

   def get_exhibit_likelihood( self, exhibit, month, day ):
      next_month = self.zoo_util.get_next_month( month )

      month_likelihood = self.get_exhibit_month_likelihood( exhibit, month )
      next_month_likelihood = self.get_exhibit_month_likelihood( exhibit, next_month )

      days_in_month = self.zoo_util.get_number_of_days_in_month( month )
      
      return month_likelihood + (next_month_likelihood - month_likelihood)/days_in_month * day
      

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
         """, (species, ) )
      
      animal = data.fetchone()
      
      animal_info = zoo.Animal( species=species, latin_name=animal[0], general_viewing_tips=animal[1], seasonal_viewing_tips=animal[2],
                                identification=animal[3], habitat_and_range=animal[4],  diet_and_feeding=animal[5],
                                behaviour_and_life_cycle=animal[6], adaptations=animal[7], reproduction_and_life_cycle=animal[8],
                                animals_at_the_zoo=animal[9], exhibit=animal[10], seasonal_viewing_summary=animal[11],
                                seasonal_viewing_information=animal[12] )
      
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
         pavilions.append( zoo.Pavilion( name=pavilion[0], region=pavilion[1], description=pavilion[2], x_coord=pavilion[3],
                                         y_coord=pavilion[4] ) )

      cur.close()

      return pavilions
   

   def get_restaurants( self, month, include_seasonal_restaurants ):
      cur = self.conn.cursor()

      is_peak_season_month = self.zoo_util.is_peak_season_month( month )

      data = cur.execute(
         """   SELECT
                  r.NAME,
                  r.LOCATION,
                  r.SUB_LOCATION,
                  r.SEASONAL_SCHEDULE,
                  r.OPEN_SEASONALLY,
                  r.DESCRIPTION,
                  r.MENU_LINK,
                  r.X_COORD,
                  r.Y_COORD
               FROM Restaurant r;
         """ )
      
      restaurant_data = data.fetchall()

      restaurants = []
      for restaurant in restaurant_data: 
         open_seasonally = restaurant[4]
         if is_peak_season_month or include_seasonal_restaurants or not open_seasonally:
            restaurants.append( zoo.Restaurant( name=restaurant[0], location=restaurant[1], sub_location=restaurant[2],
                                                seasonal_schedule=restaurant[3], description=restaurant[5], menu_link=restaurant[6],
                                                x_coord=restaurant[7], y_coord=restaurant[8] ) )

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
         restrooms.append( zoo.Restroom( title=restroom[0], x_coord=restroom[1], y_coord=restroom[2] ) )

      cur.close()

      return restrooms
   

   def get_gift_shops( self, month, include_seasonal_gift_shops ):
      cur = self.conn.cursor()

      is_peak_season_month = self.zoo_util.is_peak_season_month( month )

      data = cur.execute(
         """   SELECT
                  g.NAME,
                  g.LOCATION,
                  g.OPEN_SEASONALLY,
                  g.SEASONAL_SCHEDULE,
                  g.DESCRIPTION,
                  g.X_COORD,
                  g.Y_COORD
               FROM GiftShop g;
         """ )
      
      gift_shop_data = data.fetchall()

      gift_shops = []
      for gift_shop in gift_shop_data: 
         open_seasonally = gift_shop[2]
         if is_peak_season_month or include_seasonal_gift_shops or not open_seasonally:
            gift_shops.append( zoo.GiftShop( name=gift_shop[0], location=gift_shop[1], seasonal_schedule=gift_shop[3],
                                             description=gift_shop[4], x_coord=gift_shop[5], y_coord=gift_shop[6] ) )

      cur.close()

      return gift_shops
      

   def get_animals_matching_query( self, query ):
      cur = self.conn.cursor()

      pattern = f"%{query}%"
      data = cur.execute(
         """   SELECT
                  a.SPECIES,
                  e.EXHIBIT
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               WHERE a.SPECIES LIKE ? ESCAPE '\\';
         """, (pattern, ) )
      
      animal_data = data.fetchall()

      animals = []
      for animal in animal_data: 
         animals.append( zoo.Animal( species=animal[0], exhibit=animal[1] ) )

      cur.close()

      return animals
   

   def get_pavilions_matching_query( self, query ):
      cur = self.conn.cursor()

      pattern = f"%{query}%"
      data = cur.execute(
         """   SELECT
                  p.NAME,
                  p.REGION,
                  p.X_COORD,
                  p.Y_COORD
               FROM Pavilion p
               WHERE p.NAME LIKE ? ESCAPE '\\';
         """, (pattern, ) )
      
      pavilion_data = data.fetchall()

      pavilions = []
      for pavilion in pavilion_data: 
         pavilions.append( zoo.Pavilion( name=pavilion[0], region=pavilion[1], x_coord=pavilion[2], y_coord=pavilion[3] ) )

      cur.close()

      return pavilions
   

   def get_restaurants_matching_query( self, query ):
      cur = self.conn.cursor()

      pattern = f"%{query}%"
      data = cur.execute(
         """   SELECT
                  r.NAME,
                  r.LOCATION,
                  r.SUB_LOCATION,
                  r.X_COORD,
                  r.Y_COORD
               FROM Restaurant r
               WHERE r.NAME LIKE ? ESCAPE '\\';
         """, (pattern, ) )
      
      restaurant_data = data.fetchall()

      restaurants = []
      for restaurant in restaurant_data: 
         restaurants.append( zoo.Restaurant( name=restaurant[0], location=restaurant[1], sub_location=restaurant[2],
                                             x_coord=restaurant[3], y_coord=restaurant[4] ) )

      cur.close()

      return restaurants
   

   def get_restrooms_matching_query( self, query ):
      cur = self.conn.cursor()

      pattern = f"%{query}%"
      data = cur.execute(
         """   SELECT
                  r.TITLE,
                  r.X_COORD,
                  r.Y_COORD
               FROM Restroom r
               WHERE r.TITLE LIKE ? ESCAPE '\\';
         """, (pattern, ) )
      
      restroom_data = data.fetchall()

      restrooms = []
      for restroom in restroom_data: 
         restrooms.append( zoo.Restroom( title=restroom[0], x_coord=restroom[1], y_coord=restroom[2] ) )

      cur.close()

      return restrooms
   

   def get_gift_shops_matching_query( self, query ):
      cur = self.conn.cursor()

      pattern = f"%{query}%"
      data = cur.execute(
         """   SELECT
                  g.NAME,
                  g.LOCATION,
                  g.X_COORD,
                  g.Y_COORD
               FROM GiftShop g
               WHERE g.NAME LIKE ? ESCAPE '\\';
         """, (pattern, ) )
      
      gift_shop_data = data.fetchall()

      gift_shops = []
      for gift_shop in gift_shop_data: 
         gift_shops.append( zoo.GiftShop( name=gift_shop[0], location=gift_shop[1], x_coord=gift_shop[2], y_coord=gift_shop[3] ) )

      cur.close()

      return gift_shops
   