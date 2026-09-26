from __future__ import annotations

from api.models.pavilion import Pavilion
from api.pavilions.search.pavilions_matching_query_builder import PavilionsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingPavilionOnly() -> None:
   americas = Pavilion( 'Americas Pavilion', 'Americas' )
   australasia = Pavilion( 'Australasia Pavilion', 'Australasia' )
   pavilions = [ americas, australasia ]
   query = 'americas'

   matches = PavilionsMatchingQueryBuilder.build( pavilions, query )

   assert [ pavilion.name for pavilion in matches ] == [ americas.name ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingPavilionOnly() -> None:
   americas = Pavilion( 'Americas Pavilion', 'Americas' )
   australasia = Pavilion( 'Australasia Pavilion', 'Australasia' )
   pavilions = [ americas, australasia ]
   query = 'americas'

   matches = PavilionsMatchingQueryBuilder.filter_matching_query(
      pavilions,
      query )

   assert [ pavilion.name for pavilion in matches ] == [ americas.name ]


def Test_Build_TestEmptyQuery_ExpectAllPavilionsSortedByName() -> None:
   americas = Pavilion( 'Americas Pavilion', 'Americas' )
   australasia = Pavilion( 'Australasia Pavilion', 'Australasia' )
   pavilions = [ americas, australasia ]
   query = ''

   matches = PavilionsMatchingQueryBuilder.build( pavilions, query )

   assert [ pavilion.name for pavilion in matches ] == [
      americas.name,
      australasia.name,
   ]


def Test_SortByName_TestUnsortedPavilions_ExpectAlphabetical() -> None:
   australasia = Pavilion( 'Australasia Pavilion', 'Australasia' )
   americas = Pavilion( 'Americas Pavilion', 'Americas' )
   pavilions = [ australasia, americas ]

   sorted_pavilions = PavilionsMatchingQueryBuilder.sort_by_name( pavilions )

   assert [ pavilion.name for pavilion in sorted_pavilions ] == [
      americas.name,
      australasia.name,
   ]
