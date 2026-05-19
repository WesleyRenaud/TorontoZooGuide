from .itinerary_animal_record import ItineraryAnimalRecord


def map_itinerary_animal_record( row ):
   return ItineraryAnimalRecord(
      species=row[ 'SPECIES' ],
      exhibit=row[ 'EXHIBIT' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ] )


def map_itinerary_animal_records( rows ):
   return [
      map_itinerary_animal_record( row )
      for row in rows
   ]
