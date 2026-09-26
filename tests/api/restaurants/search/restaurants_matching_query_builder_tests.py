from __future__ import annotations

from api.models.restaurant import Restaurant
from api.restaurants.search.restaurants_matching_query_builder import RestaurantsMatchingQueryBuilder


def Test_Build_TestMatchingQuery_ExpectMatchingRestaurantOnly() -> None:
   africa_restaurant = Restaurant(
      name='Africa Restaurant',
      location='Africa',
      sub_location=None )
   beavertails = Restaurant(
      name='Beavertails',
      location='Tundra Trek',
      sub_location=None )
   restaurants = [ africa_restaurant, beavertails ]
   query = 'africa'

   matches = RestaurantsMatchingQueryBuilder.build( restaurants, query )

   assert [ restaurant.name for restaurant in matches ] == [ africa_restaurant.name ]


def Test_FilterMatchingQuery_TestMatchingQuery_ExpectMatchingRestaurantOnly() -> None:
   africa_restaurant = Restaurant(
      name='Africa Restaurant',
      location='Africa',
      sub_location=None )
   beavertails = Restaurant(
      name='Beavertails',
      location='Tundra Trek',
      sub_location=None )
   restaurants = [ africa_restaurant, beavertails ]
   query = 'africa'

   matches = RestaurantsMatchingQueryBuilder.filter_matching_query(
      restaurants,
      query )

   assert [ restaurant.name for restaurant in matches ] == [ africa_restaurant.name ]
