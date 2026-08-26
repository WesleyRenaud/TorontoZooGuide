from __future__ import annotations

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.guardians.search.guardians_talks_matching_query import build_guardians_talks_matching_query
from api.models import GuardiansTalk
from api.models import Pavilion
from api.models import Restroom
from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
from api.pavilions.search.pavilions_matching_query import build_pavilions_matching_query
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from api.restrooms.search.restrooms_matching_query_builder import RestroomsMatchingQueryBuilder
from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from conftest import DbControllers

def test_search_helpers_filter_case_insensitively( db: DbControllers ) -> None:
   assert [
      restaurant.name
      for restaurant in RestaurantCoordinator.get_restaurants_matching_query( 'AFRICA', 15, 'June', 2026, True )
   ] == [ 'Africa Restaurant' ]

   assert [
      shop.name
      for shop in GiftShopCoordinator.get_gift_shops_matching_query( 'ZOOTIQUE', 15, 'June', 2026 )
   ] == [ 'Zootique' ]

   assert [
      attraction.name
      for attraction in AttractionCoordinator.get_attractions_matching_query( 'CAROUSEL', 15, 'June', 2026, True )
   ] == [ 'Conservation Carousel' ]

   assert {
      station.name
      for station in TransportationCoordinator.get_transportation_stations_matching_query(
         query='MAIN',
         route='summer',
         day=15,
         month='June',
         year=2026 )
   } == {
      'Main Zoomobile Station',
      'Canadian Domain Zoomobile Station',
   }

   assert [
      pavilion.name
      for pavilion in PavilionCoordinator.get_pavilions_matching_query( 'AUSTRALASIA' )
   ] == [ 'Australasia Pavilion' ]

   assert [
      restroom.title
      for restroom in RestroomCoordinator.get_restrooms_matching_query(
         query='ZOOTIQUE',
         day=15,
         month='June',
         year=2026,
         include_closed_restrooms=True )
   ] == [ 'Zootique Restroom' ]


def test_matching_query_filters_and_handles_empty_query() -> None:
   pavilions = [
      Pavilion( 'Americas Pavilion', 'Americas' ),
      Pavilion( 'Australasia Pavilion', 'Australasia' ),
   ]

   assert [
      pavilion.name
      for pavilion in build_pavilions_matching_query( pavilions, 'americas' )
   ] == [ 'Americas Pavilion' ]

   assert [
      pavilion.name
      for pavilion in build_pavilions_matching_query( pavilions, '' )
   ] == [
      'Americas Pavilion',
      'Australasia Pavilion',
   ]

   guardians_talks = [
      GuardiansTalk( 'Komodo Dragon', 'Australasia Pavilion', 0, 0 ),
      GuardiansTalk( 'Arctic Wolf', 'Tundra Trek', 0, 0 ),
   ]

   assert [
      talk.name
      for talk in build_guardians_talks_matching_query( guardians_talks, 'komodo' )
   ] == [ 'Komodo Dragon' ]

   assert [
      talk.name
      for talk in build_guardians_talks_matching_query( guardians_talks, '' )
   ] == [
      'Komodo Dragon',
      'Arctic Wolf',
   ]

   restrooms = [
      Restroom( 'Zootique Restroom' ),
      Restroom( 'Entrance Restroom' ),
   ]

   assert [
      restroom.title
      for restroom in RestroomsMatchingQueryBuilder.build( restrooms, 'zootique' )
   ] == [ 'Zootique Restroom' ]

   assert [
      restroom.title
      for restroom in RestroomsMatchingQueryBuilder.build( restrooms, '' )
   ] == [
      'Zootique Restroom',
      'Entrance Restroom',
   ]
