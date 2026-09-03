from __future__ import annotations

from api.attractions.search.attractions_matching_query_builder import AttractionsMatchingQueryBuilder
from api.models.attraction import Attraction


CAROUSEL_NAME = 'Conservation Carousel'
ZOOMOBILE_NAME = 'Zoomobile'
SEARCH_QUERY = 'carousel'


def _attraction( name: str ) -> Attraction:
   return Attraction(
      name=name,
      free_with_admission=True )


def Test_Build_TestMatchingQuery_ExpectMatchingAttractionsOnly() -> None:
   attractions = [
      _attraction( CAROUSEL_NAME ),
      _attraction( ZOOMOBILE_NAME ),
   ]

   matches = AttractionsMatchingQueryBuilder.build( attractions, SEARCH_QUERY )

   assert [ attraction.name for attraction in matches ] == [ CAROUSEL_NAME ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingAttractionsOnly() -> None:
   attractions = [
      _attraction( CAROUSEL_NAME ),
      _attraction( ZOOMOBILE_NAME ),
   ]

   matches = AttractionsMatchingQueryBuilder.filter_matching_query(
      attractions,
      SEARCH_QUERY )

   assert [ attraction.name for attraction in matches ] == [ CAROUSEL_NAME ]
