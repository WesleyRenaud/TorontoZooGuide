from __future__ import annotations

from dataclasses import dataclass

from api.shared.name_matching_query_builder import NameMatchingQueryBuilder


@dataclass
class SampleItem():
   name: str


def _items() -> list[ SampleItem ]:
   return [
      SampleItem( name='Africa Restaurant' ),
      SampleItem( name='Zootique' ),
   ]


def Test_FilterMatching_TestCaseInsensitiveSubstring_ExpectMatchingItemsOnly() -> None:
   matches = NameMatchingQueryBuilder.filter_matching(
      _items(),
      'africa',
      lambda item: item.name.lower() )

   assert [ item.name for item in matches ] == [ 'Africa Restaurant' ]


def Test_FilterMatching_TestEmptyQuery_ExpectAllItems() -> None:
   matches = NameMatchingQueryBuilder.filter_matching(
      _items(),
      '',
      lambda item: item.name.lower() )

   assert [ item.name for item in matches ] == [ 'Africa Restaurant', 'Zootique' ]


def Test_SortByKey_TestUnsortedItems_ExpectSortedByKey() -> None:
   sorted_items = NameMatchingQueryBuilder.sort_by_key(
      _items(),
      lambda item: item.name.lower() )

   assert [ item.name for item in sorted_items ] == [ 'Africa Restaurant', 'Zootique' ]


def Test_Build_TestMatchingQueryWithSort_ExpectFilteredAndSortedItems() -> None:
   matches = NameMatchingQueryBuilder.build(
      _items(),
      'zoo',
      lambda item: item.name.lower(),
      sort=True )

   assert [ item.name for item in matches ] == [ 'Zootique' ]
