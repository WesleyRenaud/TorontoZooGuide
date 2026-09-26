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
   items = _items()
   query = 'africa'

   matches = NameMatchingQueryBuilder.filter_matching(
      items,
      query,
      lambda item: item.name.lower() )

   assert [ item.name for item in matches ] == [
      item.name for item in items if query in item.name.lower()
   ]


def Test_FilterMatching_TestEmptyQuery_ExpectAllItems() -> None:
   items = _items()
   query = ''

   matches = NameMatchingQueryBuilder.filter_matching(
      items,
      query,
      lambda item: item.name.lower() )

   assert [ item.name for item in matches ] == [ item.name for item in items ]


def Test_SortByKey_TestUnsortedItems_ExpectSortedByKey() -> None:
   items = _items()

   sorted_items = NameMatchingQueryBuilder.sort_by_key(
      items,
      lambda item: item.name.lower() )

   assert [ item.name for item in sorted_items ] == [
      item.name for item in sorted( items, key=lambda item: item.name.lower() )
   ]


def Test_Build_TestMatchingQueryWithSort_ExpectFilteredAndSortedItems() -> None:
   items = _items()
   query = 'zoo'

   matches = NameMatchingQueryBuilder.build(
      items,
      query,
      lambda item: item.name.lower(),
      sort=True )

   assert [ item.name for item in matches ] == [
      item.name for item in items if query in item.name.lower()
   ]
