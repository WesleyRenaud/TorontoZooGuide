from ... import zoo
from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_save_input import ItinerarySaveInput


def map_named_strings( names ):
   return tuple(
      name.strip()
      for name in names or []
      if str( name ).strip()
   )



def map_animal_inputs( animals ):
   return tuple(
      ItineraryAnimalInput(
         species=animal[ 'species' ],
         exhibit=animal[ 'exhibit' ] )
      for animal in animals or []
   )



def map_itinerary_save_input(
      date,
      animals,
      attractions,
      guardians_talks,
      wild_encounters ):

   return ItinerarySaveInput(
      date=zoo.ZooUtil.parse_date_value( date ),
      animals=map_animal_inputs( animals ),
      attractions=map_named_strings( attractions ),
      guardians_talks=map_named_strings( guardians_talks ),
      wild_encounters=map_named_strings( wild_encounters ) )
