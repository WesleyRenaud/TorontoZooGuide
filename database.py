import sqlite3
import zoo


################################################################################

class Database():
   def __init__( self ):
      self.conn = sqlite3.connect( 'animals.db' )
      self.zoo_util = zoo.Zoo_Util()


   # Returns all animals which may be viewable in the given month with their likelihoods (probability from 0 to 1)
   def get_animals_viewable_on_day( self, month, day, temp=None ):
      if temp == None:
         temp = self.zoo_util.get_average_temperature( month, day )
         sigma = 3
      else:
         sigma = 2
      snow_likelihood = self.zoo_util.get_snow_likelihood( month, day )

      cur = self.conn.cursor()
   
      # We need to know whether the animal is viewable indoors and/or outdoors. If they are viewable in both, then we need to calculate
      # whether they are viewable outside or not in this case.
      data = cur.execute(
         """   SELECT
                  a.SPECIES,
                  a.EXHIBIT,
                  a.MIN_TEMPERATURE,
                  a.SNOW_RESISTANCE,
                  a.PART_OF_SEASONAL_EXHIBIT,
                  a.SEASONAL_VIEWING_SUMMARY,
                  a.SEASONAL_VIEWING_TIPS,
                  a.GENERAL_VIEWING_TIPS,
                  a.ANIMAL_INFO,
                  a.SPECIFIC_ANIMAL_INFO,
                  e.EXHIBIT_TYPE,
                  e.X_COORD,
                  e.Y_COORD
               FROM Animal a
               JOIN Enclosure e
               ON a.SPECIES = e.SPECIES
               AND a.exhibit = e.exhibit;
         """ )

      animal_data = data.fetchall()
      animals = []

      for animal in animal_data:
         species = animal[0]
         exhibit = animal[1]
         min_temperature = animal[2]
         snow_resistance = animal[3]
         part_of_seasonal_exhibit = animal[4]
         exhibit_type = animal[10]

         if exhibit_type == 'Outdoor':
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
            data = cur.execute(
               f"""  SELECT
                        e.{month}_PROBABILITY
                     FROM Exhibit e
                     WHERE e.NAME = ?;
               """, (exhibit, ) )
            
            exhibit_probability = data.fetchone()[0]
            likelihood = likelihood * exhibit_probability

         likelihood = round( likelihood * 100 )

         if likelihood > 0:
            animals.append( zoo.Animal( species=species, exhibit=exhibit, seasonal_viewing_summary=animal[5],
                                        seasonal_viewing_tips=animal[6], general_viewing_tips=animal[7], animal_info=animal[8],
                                        specific_animal_info=animal[9], exhibit_type=exhibit_type, likelihood=likelihood,
                                        x_coord=animal[11], y_coord=animal[12] ) )

      return animals
