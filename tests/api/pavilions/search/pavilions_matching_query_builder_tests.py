from __future__ import annotations

from api.models.pavilion import Pavilion
from api.pavilions.search.pavilions_matching_query_builder import PavilionsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingPavilionOnly() -> None:
   pavilions = [
      Pavilion( 'Americas Pavilion', 'Americas' ),
      Pavilion( 'Australasia Pavilion', 'Australasia' ),
   ]

   matches = PavilionsMatchingQueryBuilder.build( pavilions, 'americas' )

   assert [ pavilion.name for pavilion in matches ] == [ 'Americas Pavilion' ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingPavilionOnly() -> None:
   pavilions = [
      Pavilion( 'Americas Pavilion', 'Americas' ),
      Pavilion( 'Australasia Pavilion', 'Australasia' ),
   ]

   matches = PavilionsMatchingQueryBuilder.filter_matching_query(
      pavilions,
      'americas' )

   assert [ pavilion.name for pavilion in matches ] == [ 'Americas Pavilion' ]


def Test_Build_TestEmptyQuery_ExpectAllPavilionsSortedByName() -> None:
   pavilions = [
      Pavilion( 'Americas Pavilion', 'Americas' ),
      Pavilion( 'Australasia Pavilion', 'Australasia' ),
   ]

   matches = PavilionsMatchingQueryBuilder.build( pavilions, '' )

   assert [ pavilion.name for pavilion in matches ] == [
      'Americas Pavilion',
      'Australasia Pavilion',
   ]


def Test_SortByName_TestUnsortedPavilions_ExpectAlphabetical() -> None:
   pavilions = [
      Pavilion( 'Australasia Pavilion', 'Australasia' ),
      Pavilion( 'Americas Pavilion', 'Americas' ),
   ]

   sorted_pavilions = PavilionsMatchingQueryBuilder.sort_by_name( pavilions )

   assert [ pavilion.name for pavilion in sorted_pavilions ] == [
      'Americas Pavilion',
      'Australasia Pavilion',
   ]
