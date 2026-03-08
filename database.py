import sqlite3
import zoo


################################################################################

class Database():
   def __init__( self ):
      self.conn = sqlite3.connect( 'animals.db' )
      self.zoo_util = zoo.Zoo_Util()


   # Returns all animals which may be viewable in the given month with their likelihoods (probability from 0 to 1)
   def get_animals_viewable_on_day( self, month, day, temp=None, include_off_display_animals=False, threshold=0, species_to_include=[],
                                    itinerary_mode=False ):
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
            avg_temp = self.zoo_util.get_average_temperature( month, day )
            effective_temp = avg_temp + 0.5 * ( temp - avg_temp )

            likelihood = self.zoo_util.get_temperature_probability( effective_temp, sigma, min_temperature )
            likelihood = likelihood - (1.0 - snow_resistance) * snow_likelihood
         else:
            likelihood = 1

         # We need to consider if the animal is a part of a seasonal exhibit, and whether that exhibit will be open on the specific day
         if part_of_seasonal_exhibit:
            # Get the probability that the exhibit is open, and scale the likelihood to that
            likelihood = likelihood * self.get_exhibit_likelihood( exhibit, month, day )

         likelihood = max( round( likelihood * 100 ), 0 )

         if (not itinerary_mode and (likelihood > threshold or include_off_display_animals or species in species_to_include)) \
            or (itinerary_mode and species in species_to_include):
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
   

   def get_restaurants( self, month, include_seasonal_restaurants, restaurants_to_include=[] ):
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
         name = restaurant[0]
         open_seasonally = restaurant[4]
         if is_peak_season_month or include_seasonal_restaurants or not open_seasonally or name in restaurants_to_include:
            restaurants.append( zoo.Restaurant( name=name, location=restaurant[1], sub_location=restaurant[2],
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
   

   def get_gift_shops( self, month, include_seasonal_gift_shops, gift_shops_to_include=[] ):
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
         name = gift_shop[0]
         open_seasonally = gift_shop[2]
         if is_peak_season_month or include_seasonal_gift_shops or not open_seasonally or name in gift_shops_to_include:
            gift_shops.append( zoo.GiftShop( name=name, location=gift_shop[1], seasonal_schedule=gift_shop[3],
                                             description=gift_shop[4], x_coord=gift_shop[5], y_coord=gift_shop[6] ) )

      cur.close()

      return gift_shops
   

   def get_attractions( self, month, include_seasonal_attractions=False, attractions_to_include=[], itinerary_mode=False ):
      cur = self.conn.cursor()

      is_peak_season_month = self.zoo_util.is_peak_season_month( month )

      data = cur.execute(
         """   SELECT
                  a.NAME,
                  a.OPEN_SEASONALLY,
                  a.FREE_WITH_ADMISSION,
                  a.SEASONAL_SCHEDULE,
                  a.DESCRIPTION,
                  a.INFO_LINK,
                  a.HYPERLINK_TEXT,
                  a.X_COORD,
                  a.Y_COORD
               FROM Attraction a;
         """ )
      
      attraction_data = data.fetchall()

      attractions = []
      for attraction in attraction_data:
         name = attraction[0]
         open_seasonally = attraction[1]
         if ((not itinerary_mode) and (is_peak_season_month or include_seasonal_attractions or (not open_seasonally) \
            or (name in attractions_to_include))) \
            or (itinerary_mode and (name in attractions_to_include)):
            is_closed = open_seasonally and not is_peak_season_month
            attractions.append( zoo.Attraction( name=name, free_with_admission=attraction[2], seasonal_schedule=attraction[3],
                                                description=attraction[4], info_link=attraction[5], hyperlink_text=attraction[6],
                                                x_coord=attraction[7], y_coord=attraction[8], is_closed=is_closed ) )

      cur.close()

      return attractions
   

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
         zoomobile_stations.append( zoo.ZoomobileStation( name=zoomobile_station[0], x_coord=zoomobile_station[1],
                                                          y_coord=zoomobile_station[2] ) )

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
         name = zoomobile_station[0]
         on_winter_route = zoomobile_station[1]
         if route_type == 'summer' or on_winter_route or name in zoomobile_stations_to_include:
            zoomobile_stations.append( zoo.ZoomobileStation( name=zoomobile_station[0], description=zoomobile_station[2],
                                                             x_coord=zoomobile_station[3], y_coord=zoomobile_station[4] ) )
            
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
         on_winter_route = zoomobile_route_marker[0]
         on_summer_route = zoomobile_route_marker[1]
         if route_type == 'winter' and on_winter_route or route_type == 'summer' and on_summer_route:
            zoomobile_route_markers.append( zoo.ZoomobileRouteMarker( route_type=route_type, x_coord=zoomobile_route_marker[2],
                                                                      y_coord=zoomobile_route_marker[3] ) )

      cur.close()

      return [zoomobile_stations, zoomobile_route_markers]
   


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
         meet_the_guardians_talks.append( zoo.MeetTheGuardiansTalk( name=meet_the_guardians_talk[0],
                                                                    location=meet_the_guardians_talk[1],
                                                                    x_coord=meet_the_guardians_talk[2],
                                                                    y_coord=meet_the_guardians_talk[3] ) )

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
         name = meet_the_guardians_talk[0]
         if (not itinerary_mode) or (name in meet_the_guardians_talks_to_include):
            meet_the_guardians_talks.append( zoo.MeetTheGuardiansTalk( name=name, location=meet_the_guardians_talk[1],
                                                                       x_coord=meet_the_guardians_talk[2],
                                                                       y_coord=meet_the_guardians_talk[3],
                                                                       day_of_week=meet_the_guardians_talk[4],
                                                                       time_of_day=meet_the_guardians_talk[5] ) )

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
         wild_encounter_meeting_spots.append( zoo.WildEncounterMeetingSpot( name=wild_encounter_meeting_spot[0],
                                                                           x_coord=wild_encounter_meeting_spot[1],
                                                                           y_coord=wild_encounter_meeting_spot[2] ) )

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
            """, (wild_encounter, ) )

         wild_encounter_data = cur.fetchone()

         wild_encounters.append( zoo.WildEncounter( name=wild_encounter, meeting_spot=wild_encounter_data[0],
                                                    x_coord=wild_encounter_data[1], y_coord=wild_encounter_data[2],
                                                    link=wild_encounter_data[3] ) )

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
         wild_encounters.append( zoo.WildEncounter( name=wild_encounter[0], meeting_spot=wild_encounter[1], link=wild_encounter[2],
                                                    day_of_week=wild_encounter[3], time_of_day=wild_encounter[4] ) )

      cur.close()

      return wild_encounters
   

   def get_animals_matching_query( self, query, month, day, temp, include_off_display_animals ):
      animals = self.get_animals_viewable_on_day( month=month, day=day, temp=temp,
                                                  include_off_display_animals=include_off_display_animals, threshold=80 )

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
   

   def get_restaurants_matching_query( self, query, month ):
      if not query:
         return self.get_restaurants( month, include_seasonal_restaurants=True )

      query_lower = query.lower()

      return [
         r for r in self.get_restaurants( month, include_seasonal_restaurants=True )
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
   

   def get_attractions_matching_query( self, query, month, include_season_attractions ):
      if not query:
         return self.get_attractions( month, include_seasonal_attractions=include_season_attractions )

      query_lower = query.lower()

      return [
         a for a in self.get_attractions( month, include_seasonal_attractions=include_season_attractions )
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