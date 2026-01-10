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

      data = cur.execute( "SELECT SPECIES, LOCATION, HAS_OUTDOOR_VIEWING FROM ANIMAL;" )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_outdoor_viewing = animal[2]
         
         # If the animal has outdoor viewing, then it will be viewable outdoors in the heat of summer
         if has_outdoor_viewing:
            animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Outdoor", likelihood=5 ) )
            
            # Check if the animal can be viewed outside and inside at the same time (it can also be viewed inside)
            if self.zoo_util.species_viewable_inside_and_outside( species=animal[0] ):
               animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Indoor", likelihood=5 ) )
         else:
            animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Indoor", likelihood=5 ) )

      return animals

   
   # Returns all animals which are viewable year-round
   def get_winter_animals( self ):
      cur = self.conn.cursor()

      data = cur.execute( "SELECT SPECIES, LOCATION, HAS_INDOOR_VIEWING, WINTER_VIEWABILITY FROM ANIMAL WHERE ALWAYS_VIEWABLE = 1;" )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_indoor_viewing = animal[2]

         # If the animal is viewable indoors, then it will be viewable indoors in the den of winter (now cold weather animals have
         # indoor viewing)
         if has_indoor_viewing:
            animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Indoor", likelihood=5 ) )
         else:
            animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Outdoor", likelihood=animal[3] ) )

      return animals


   # Returns all animals which may be viewable in the given month plus their likelihoods (integer 1 to 5), and where they are viewable
   # (outdoors or indoors)
   def get_animals_viewable_in_month( self, month ):
      cur = self.conn.cursor()
   
      # We need to know whether the animal is viewable indoors and/or outdoors. If they are viewable in both, then we need to calculate
      # whether they are viewable outside or not in this case.
      data = cur.execute(
         f"""  SELECT
                  SPECIES,
                  LOCATION,
                  HAS_OUTDOOR_VIEWING,
                  HAS_INDOOR_VIEWING,
                  {month}_VIEWABILITY
               FROM ANIMAL
               WHERE
                  ALWAYS_VIEWABLE = 1
                  OR {month}_VIEWABILITY > 0;
         """ )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_outdoor_viewing = animal[2]
         has_indoor_viewing = animal[3]
         month_viewability = animal[4]

         # If the animal is only viewable outdoors, then we can determine that it is viewable outdoors
         if has_outdoor_viewing and not has_indoor_viewing:
            animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Outdoor", likelihood=month_viewability ) )

         # The same logic for indoor-viewable-only animals
         elif has_indoor_viewing and not has_outdoor_viewing:
            animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Indoor", likelihood=5 ) )

         # If the animal is viewable outdoors and indoors, we must check whether they are viewable outdoors in this specific case.
         # More specifically, we must check the chance of the animal being viewable and if it is not either 0% or 100%, we must record
         # this.
         else:
            species = animal[0]

            if month_viewability < 5:
               animals.append( zoo.Animal( species=species, location=animal[1], exhibit_type="Indoor", likelihood=5 ) )
            if month_viewability > 0:
               animals.append( zoo.Animal( species=species, location=animal[1], exhibit_type="Outdoor", likelihood=month_viewability ) )

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
         f"""  SELECT
                  SPECIES,
                  LOCATION,
                  HAS_OUTDOOR_VIEWING,
                  HAS_INDOOR_VIEWING,
                  {month}_VIEWABILITY,
                  MIN_TEMPERATURE,
                  SNOW_RESISTANCE
               FROM ANIMAL
               WHERE
                  ALWAYS_VIEWABLE = 1
                  OR {month}_VIEWABILITY > 0
                  AND MIN_TEMPERATURE > ?;
         """, (temp, ) )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         has_outdoor_viewing = animal[2]
         has_indoor_viewing = animal[3]
         month_viewability = animal[4]
         min_temperature = animal[5]
         snow_resistance = animal[6]

         # If the animal is only viewable outdoors, then we can determine that it is viewable outdoors
         if has_outdoor_viewing and not has_indoor_viewing:
            # The likelihood increases by 1 for every two 5 degrees that the temperature is warmer than their minimum temperature
            likelihood = min( month_viewability + (temp - min_temperature) / 5, 5 )

            # Also consider snow/ice based on the month + day
            month_int = self.zoo_util.get_month_int( month )
            snow_likelihood = self.zoo_util.snow_probability( month_int, day )
            
            # For every point below 5 (the max) an animal's snow resistance is, the more their likelihood of being viewable is tanked
            # by the likelihood of snow on the ground
            likelihood = max( likelihood - (5 - snow_resistance) * snow_likelihood / 2, 0 )

            if likelihood > 0:
               animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Outdoor", likelihood=likelihood ) )

         # The same logic for indoor-viewable-only animals
         elif has_indoor_viewing and not has_outdoor_viewing:
            animals.append( zoo.Animal( species=animal[0], location=animal[1], exhibit_type="Indoor", likelihood=5 ) )

         # If the animal is viewable outdoors and indoors, we must check whether they are viewable outdoors in this specific case.
         # More specifically, we must check the chance of the animal being viewable and if it is not either 0% or 100%, we must record
         # this.
         else:
            species = animal[0]

            if month_viewability < 5:
               animals.append( zoo.Animal( species=species, location=animal[1], exhibit_type="Indoor", likelihood=5 ) )
            if month_viewability > 0:
               # Calculate their outdoor viewability
               # The likelihood increases by 1 for every two 5 degrees that the temperature is warmer than their minimum temperature
               likelihood = min( month_viewability + (temp - min_temperature) / 5, 5 )

               # Also consider snow/ice based on the month + day
               month_int = self.zoo_util.get_month_int( month )
               snow_likelihood = self.zoo_util.snow_probability( month_int, day )
               
               # For every point below 5 (the max) an animal's snow resistance is, the more their likelihood of being viewable is tanked
               # by the likelihood of snow on the ground
               likelihood = likelihood - (5 - snow_resistance) * snow_likelihood / 2

               animals.append( zoo.Animal( species=species, location=animal[1], exhibit_type="Outdoor", likelihood=likelihood ) )

      return animals
