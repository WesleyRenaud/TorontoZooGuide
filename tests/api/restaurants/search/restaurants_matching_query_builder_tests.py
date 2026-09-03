from __future__ import annotations

from api.models.restaurant import Restaurant
from api.restaurants.search.restaurants_matching_query_builder import RestaurantsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingRestaurantOnly() -> None:
   restaurants = [
      Restaurant( name='Africa Restaurant', location='Africa', sub_location=None ),
      Restaurant( name='Beavertails', location='Tundra Trek', sub_location=None ),
   ]

   matches = RestaurantsMatchingQueryBuilder.build( restaurants, 'africa' )

   assert [ restaurant.name for restaurant in matches ] == [ 'Africa Restaurant' ]

def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingRestaurantOnly() -> None:
   restaurants = [
      Restaurant( name='Africa Restaurant', location='Africa', sub_location=None ),
      Restaurant( name='Beavertails', location='Tundra Trek', sub_location=None ),
   ]
   matches = RestaurantsMatchingQueryBuilder.filter_matching_query( restaurants, 'africa' )
   assert [ restaurant.name for restaurant in matches ] == [ 'Africa Restaurant' ]
