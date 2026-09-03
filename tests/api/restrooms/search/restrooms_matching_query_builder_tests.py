from __future__ import annotations

from api.models.restroom import Restroom
from api.restrooms.search.restrooms_matching_query_builder import RestroomsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingRestroomOnly() -> None:
   restrooms = [
      Restroom( 'Zootique Restroom' ),
      Restroom( 'Entrance Restroom' ),
   ]

   matches = RestroomsMatchingQueryBuilder.build( restrooms, 'zootique' )

   assert [ restroom.title for restroom in matches ] == [ 'Zootique Restroom' ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingRestroomOnly() -> None:
   restrooms = [
      Restroom( 'Zootique Restroom' ),
      Restroom( 'Entrance Restroom' ),
   ]

   matches = RestroomsMatchingQueryBuilder.filter_matching_query(
      restrooms,
      'zootique' )

   assert [ restroom.title for restroom in matches ] == [ 'Zootique Restroom' ]


def Test_Build_TestEmptyQuery_ExpectAllRestroomsInInputOrder() -> None:
   restrooms = [
      Restroom( 'Zootique Restroom' ),
      Restroom( 'Entrance Restroom' ),
   ]

   matches = RestroomsMatchingQueryBuilder.build( restrooms, '' )

   assert [ restroom.title for restroom in matches ] == [
      'Zootique Restroom',
      'Entrance Restroom',
   ]
