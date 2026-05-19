from .itinerary_attraction_record import ItineraryAttractionRecord


def map_itinerary_attraction_record( row ):
   return ItineraryAttractionRecord(
      attraction=row[ 'ATTRACTION' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ] )


def map_itinerary_attraction_records( rows ):
   return [
      map_itinerary_attraction_record( row )
      for row in rows
   ]
