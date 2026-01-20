import sqlite3
import zoo


################################################################################

class Database():
   def __init__( self ):
      self.conn = sqlite3.connect( 'animals.db' )
      self.zoo_util = zoo.Zoo_Util()


   # Returns all animals, their locations at the zoo, and whether they are viewable indoors or outdoors in the summer
   def get_summer_animals( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  a.SPECIES,
                  a.LOCATION,
                  a.HAS_OUTDOOR_VIEWING,
                  a.SEASONAL_VIEWING_SUMMARY,
                  a.SEASONAL_VIEWING_TIPS,
                  a.GENERAL_VIEWING_TIPS,
                  a.ANIMAL_INFO,
                  a.SPECIFIC_ANIMAL_INFO,
                  e.EXHIBIT_TYPE,
                  e.X_COORD,
                  e.Y_COORD
               FROM ANIMAL a
               JOIN ENCLOSURE e
               ON a.SPECIES = e.SPECIES
               AND a.LOCATION = e.LOCATION;
         """ )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_outdoor_viewing = animal[2]
         exhibit_type = animal[8]

         # If the animal has outdoor viewing, then it will be viewable outdoors in the heat of summer
         if has_outdoor_viewing:
            if exhibit_type == 'Outdoor':
               animals.append( zoo.Animal( species=animal[0], location=animal[1], seasonal_viewing_summary=animal[3],
                                           seasonal_viewing_tips=animal[4], general_viewing_tips=animal[5], animal_info=animal[6],
                                           specific_animal_info=animal[7], exhibit_type="Outdoor", x_coord=animal[9],
                                           y_coord=animal[10], likelihood=9 ) )
            
            # Check if the animal can be viewed outside and inside at the same time (it can also be viewed inside)
            if self.zoo_util.species_viewable_inside_and_outside( species=animal[0] ):
               animals.append( zoo.Animal( species=animal[0], location=animal[1], seasonal_viewing_summary=animal[3],
                                           seasonal_viewing_tips=animal[4], general_viewing_tips=animal[5], animal_info=animal[6],
                                           specific_animal_info=animal[7], exhibit_type="Indoor", x_coord=animal[9],
                                           y_coord=animal[10], likelihood=9 ) )
         else:
            if exhibit_type == 'Indoor':
               animals.append( zoo.Animal( species=animal[0], location=animal[1], seasonal_viewing_summary=animal[3],
                                           seasonal_viewing_tips=animal[4], general_viewing_tips=animal[5], animal_info=animal[6],
                                           specific_animal_info=animal[7], exhibit_type="Indoor", x_coord=animal[9],
                                           y_coord=animal[10], likelihood=9 ) )

      return animals

   
   # Returns all animals which are viewable year-round
   def get_winter_animals( self ):
      cur = self.conn.cursor()

      data = cur.execute(
         """   SELECT
                  a.SPECIES,
                  a.LOCATION,
                  a.HAS_INDOOR_VIEWING,
                  a.SEASONAL_VIEWING_SUMMARY,
                  a.SEASONAL_VIEWING_TIPS,
                  a.GENERAL_VIEWING_TIPS,
                  a.ANIMAL_INFO,
                  a.SPECIFIC_ANIMAL_INFO,
                  a.WINTER_VISIBILITY,
                  e.EXHIBIT_TYPE,
                  e.X_COORD,
                  e.Y_COORD
               FROM ANIMAL a
               JOIN ENCLOSURE e
               ON a.SPECIES = e.SPECIES
               AND a.LOCATION = e.LOCATION
               WHERE a.ALWAYS_VIEWABLE = 1;
         """ )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_indoor_viewing = animal[2]
         winter_visibility = animal[8]
         exhibit_type = animal[9]

         # Indoor viewing: always reliable in winter
         if exhibit_type == 'Indoor' and has_indoor_viewing:
            animals.append(
               zoo.Animal(
                  species=animal[0],
                  location=animal[1],
                  seasonal_viewing_summary=animal[3],
                  seasonal_viewing_tips=animal[4],
                  general_viewing_tips=animal[5],
                  animal_info=animal[6],
                  specific_animal_info=animal[7],
                  exhibit_type="Indoor",
                  likelihood=5,
                  x_coord=animal[10],
                  y_coord=animal[11]
               )
            )

         # Outdoor viewing: depends on winter visibility
         elif exhibit_type == 'Outdoor' and winter_visibility > 0:
            animals.append(
               zoo.Animal(
                  species=animal[0],
                  location=animal[1],
                  seasonal_viewing_summary=animal[3],
                  seasonal_viewing_tips=animal[4],
                  general_viewing_tips=animal[5],
                  animal_info=animal[6],
                  specific_animal_info=animal[7],
                  exhibit_type="Outdoor",
                  likelihood=winter_visibility,
                  x_coord=animal[10],
                  y_coord=animal[11]
               )
            )

      return animals


   # Returns all animals which may be viewable in the given month plus their likelihoods (integer 1 to 5), and where they are viewable
   # (outdoors or indoors)
   def get_animals_viewable_in_month( self, month ):
      cur = self.conn.cursor()
   
      # We need to know whether the animal is viewable indoors and/or outdoors. If they are viewable in both, then we need to calculate
      # whether they are viewable outside or not in this case.
      data = cur.execute(
         f"""   SELECT
                  a.SPECIES,
                  a.LOCATION,
                  a.HAS_OUTDOOR_VIEWING,
                  a.HAS_INDOOR_VIEWING,
                  a.{month}_VISIBILITY,
                  a.SEASONAL_VIEWING_SUMMARY,
                  a.SEASONAL_VIEWING_TIPS,
                  a.GENERAL_VIEWING_TIPS,
                  a.ANIMAL_INFO,
                  a.SPECIFIC_ANIMAL_INFO,
                  e.EXHIBIT_TYPE,
                  e.X_COORD,
                  e.Y_COORD
               FROM ANIMAL a
               JOIN ENCLOSURE e
               ON a.SPECIES = e.SPECIES
               AND a.LOCATION = e.LOCATION
               WHERE
                  a.ALWAYS_VIEWABLE = 1
                  OR a.{month}_VISIBILITY > 0;
         """ )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_outdoor_viewing = animal[2]
         has_indoor_viewing = animal[3]
         month_visibility = animal[4]
         exhibit_type = animal[10]

         # If the animal is only viewable outdoors, then we can determine that it is viewable outdoors
         if has_outdoor_viewing and not has_indoor_viewing:
            if exhibit_type == 'Outdoor':
               animals.append( zoo.Animal( species=animal[0], location=animal[1], seasonal_viewing_summary=animal[5],
                                           seasonal_viewing_tips=animal[6], general_viewing_tips=animal[7], animal_info=animal[8],
                                           specific_animal_info=animal[9], exhibit_type="Outdoor", likelihood=month_visibility,
                                           x_coord=animal[11], y_coord=animal[12] ) )

         # The same logic for indoor-viewable-only animals
         elif has_indoor_viewing and not has_outdoor_viewing:
            if exhibit_type == 'Indoor':
               animals.append( zoo.Animal( species=animal[0], location=animal[1], seasonal_viewing_summary=animal[5],
                                           seasonal_viewing_tips=animal[6], general_viewing_tips=animal[7], animal_info=animal[8],
                                           specific_animal_info=animal[9], exhibit_type="Indoor", likelihood=5, x_coord=animal[11],
                                           y_coord=animal[12] ) )

         # If the animal is viewable outdoors and indoors, we must check whether they are viewable outdoors in this specific case.
         # More specifically, we must check the chance of the animal being viewable and if it is not either 0% or 100%, we must record
         # this.
         else:
            species = animal[0]

            if month_visibility < 5:
               if exhibit_type == 'Indoor':
                  animals.append( zoo.Animal( species=species, location=animal[1], seasonal_viewing_summary=animal[5],
                                              seasonal_viewing_tips=animal[6], general_viewing_tips=animal[7], animal_info=animal[8],
                                              specific_animal_info=animal[9], exhibit_type="Indoor", likelihood=5, x_coord=animal[11],
                                              y_coord=animal[12] ) )
            if month_visibility > 0:
               if exhibit_type == 'Outdoor':
                  animals.append( zoo.Animal( species=species, location=animal[1], seasonal_viewing_summary=animal[5],
                                              seasonal_viewing_tips=animal[6], general_viewing_tips=animal[7], animal_info=animal[8],
                                              specific_animal_info=animal[9], exhibit_type="Outdoor", likelihood=month_visibility,
                                              x_coord=animal[11], y_coord=animal[12] ) )

      return animals
   

   # Returns all animals which may be viewable on the given day plus their likelihoods (integer 1 to 5), and where they are viewable
   # (outdoors or indoors)
   def get_animals_viewable_on_day( self, month, day, temp ):
      if temp == None:
         temp = self.zoo_util.get_estimated_temp( month, day )

      cur = self.conn.cursor()
   
      # We need to know whether the animal is viewable indoors and/or outdoors. If they are viewable in both, then we need to calculate
      # whether they are viewable outside or not in this case.
      data = cur.execute(
         f"""   SELECT
                  a.SPECIES,
                  a.LOCATION,
                  a.HAS_OUTDOOR_VIEWING,
                  a.HAS_INDOOR_VIEWING,
                  a.{month}_VISIBILITY,
                  a.MIN_TEMPERATURE,
                  a.SNOW_RESISTANCE,
                  a.SEASONAL_VIEWING_SUMMARY,
                  a.SEASONAL_VIEWING_TIPS,
                  a.GENERAL_VIEWING_TIPS,
                  a.ANIMAL_INFO,
                  a.SPECIFIC_ANIMAL_INFO,
                  e.EXHIBIT_TYPE,
                  e.X_COORD,
                  e.Y_COORD
               FROM ANIMAL a
               JOIN ENCLOSURE e
               ON a.SPECIES = e.SPECIES
               AND a.LOCATION = e.LOCATION
               WHERE
                  a.ALWAYS_VIEWABLE = 1
                  OR (a.{month}_VISIBILITY > 0 AND a.MIN_TEMPERATURE > ?);
         """, (temp, ) )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_outdoor_viewing = animal[2]
         has_indoor_viewing = animal[3]
         month_visibility = animal[4]
         min_temperature = animal[5]
         snow_resistance = animal[6]
         exhibit_type = animal[12]

         # If the animal is only viewable outdoors, then we can determine that it is viewable outdoors
         if has_outdoor_viewing and not has_indoor_viewing:
            if exhibit_type == 'Outdoor':
               # The likelihood increases by 1 for every two 5 degrees that the temperature is warmer than their minimum temperature
               likelihood = min( month_visibility + (temp - min_temperature) / 5, 5 )

               # Also consider snow/ice based on the month + day
               month_int = self.zoo_util.get_month_int( month )
               snow_likelihood = self.zoo_util.snow_probability( month_int, day )
               
               # For every point below 5 (the max) an animal's snow resistance is, the more their likelihood of being viewable is tanked
               # by the likelihood of snow on the ground
               likelihood = max( likelihood - (5 - snow_resistance) * snow_likelihood / 2, 0 )

               if likelihood > 0:
                  animals.append( zoo.Animal( species=animal[0], location=animal[1], seasonal_viewing_summary=animal[7],
                                              seasonal_viewing_tips=animal[8], general_viewing_tips=animal[9], animal_info=animal[10],
                                              specific_animal_info=animal[11], exhibit_type="Outdoor", likelihood=likelihood,
                                              x_coord=animal[13], y_coord=animal[14] ) )

         # The same logic for indoor-viewable-only animals
         elif has_indoor_viewing and not has_outdoor_viewing:
            if exhibit_type == 'Indoor':
               animals.append( zoo.Animal( species=animal[0], location=animal[1], seasonal_viewing_summary=animal[7],
                                           seasonal_viewing_tips=animal[8], general_viewing_tips=animal[9], animal_info=animal[10],
                                           specific_animal_info=animal[11], exhibit_type="Indoor", likelihood=5, x_coord=animal[13],
                                           y_coord=animal[14] ) )

         # If the animal is viewable outdoors and indoors, we must check whether they are viewable outdoors in this specific case.
         # More specifically, we must check the chance of the animal being viewable and if it is not either 0% or 100%, we must record
         # this.
         else:
            species = animal[0]

            if month_visibility < 5:
               if exhibit_type == 'Indoor':
                  animals.append( zoo.Animal( species=species, location=animal[1], seasonal_viewing_summary=animal[7],
                                              seasonal_viewing_tips=animal[8], general_viewing_tips=animal[9], animal_info=animal[10],
                                              specific_animal_info=animal[11], exhibit_type="Indoor", likelihood=5, x_coord=animal[13],
                                              y_coord=animal[14] ) )
            if month_visibility > 0:
               if exhibit_type == 'Outdoor':
                  # Calculate their outdoor visibility
                  # The likelihood increases by 1 for every two 5 degrees that the temperature is warmer than their minimum temperature
                  likelihood = min( month_visibility + (temp - min_temperature) / 5, 5 )

                  # Also consider snow/ice based on the month + day
                  month_int = self.zoo_util.get_month_int( month )
                  snow_likelihood = self.zoo_util.snow_probability( month_int, day )
                  
                  # For every point below 5 (the max) an animal's snow resistance is, the more their likelihood of being viewable is tanked
                  # by the likelihood of snow on the ground
                  likelihood = likelihood - (5 - snow_resistance) * snow_likelihood / 2

                  animals.append( zoo.Animal( species=species, location=animal[1], seasonal_viewing_summary=animal[7],
                                              seasonal_viewing_tips=animal[8], general_viewing_tips=animal[9], animal_info=animal[10],
                                              specific_animal_info=animal[11], exhibit_type="Outdoor", likelihood=likelihood,
                                              x_coord=animal[13], y_coord=animal[14] ) )

      return animals
