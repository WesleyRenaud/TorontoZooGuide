from __future__ import annotations

import sqlite3

from ..itinerary.data_access.clear_itinerary_provider import ClearItineraryProvider
from ..itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from ..types import Types


class UserItineraryDataCleaner():
   @classmethod
   def clear( cls, cursor: Types.Cursor ) -> None:
      ClearItineraryProvider.clear_itinerary_exhibits( cursor )
      ClearItineraryProvider.clear_itinerary_animals( cursor )
      ClearItineraryProvider.clear_itinerary_attractions( cursor )
      ClearItineraryProvider.clear_itinerary_guardians_talks( cursor )
      ClearItineraryProvider.clear_itinerary_wild_encounters( cursor )
      ClearItineraryProvider.clear_itinerary_events( cursor )
      ItineraryWalkRouteProvider.clear_itinerary_walk_route( cursor )
      ClearItineraryProvider.clear_itinerary_date( cursor )


   @classmethod
   def main( cls, db_path: str = 'animals.db' ) -> None:
      conn = sqlite3.connect( db_path )
      cursor = conn.cursor()

      try:
         cls.clear( cursor )
         conn.commit()
      finally:
         cursor.close()
         conn.close()

      print( 'User itinerary data cleared successfully.' )


if __name__ == '__main__':
   UserItineraryDataCleaner.main()
