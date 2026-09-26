from __future__ import annotations

from api.models.restroom import Restroom
from api.restrooms.search.restrooms_matching_query_builder import RestroomsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingRestroomOnly() -> None:
   zootique_restroom = Restroom( 'Zootique Restroom' )
   entrance_restroom = Restroom( 'Entrance Restroom' )
   restrooms = [ zootique_restroom, entrance_restroom ]
   query = 'zootique'

   matches = RestroomsMatchingQueryBuilder.build( restrooms, query )

   assert [ restroom.title for restroom in matches ] == [ zootique_restroom.title ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingRestroomOnly() -> None:
   zootique_restroom = Restroom( 'Zootique Restroom' )
   entrance_restroom = Restroom( 'Entrance Restroom' )
   restrooms = [ zootique_restroom, entrance_restroom ]
   query = 'zootique'

   matches = RestroomsMatchingQueryBuilder.filter_matching_query(
      restrooms,
      query )

   assert [ restroom.title for restroom in matches ] == [ zootique_restroom.title ]


def Test_Build_TestEmptyQuery_ExpectAllRestroomsInInputOrder() -> None:
   zootique_restroom = Restroom( 'Zootique Restroom' )
   entrance_restroom = Restroom( 'Entrance Restroom' )
   restrooms = [ zootique_restroom, entrance_restroom ]
   query = ''

   matches = RestroomsMatchingQueryBuilder.build( restrooms, query )

   assert [ restroom.title for restroom in matches ] == [
      zootique_restroom.title,
      entrance_restroom.title,
   ]
