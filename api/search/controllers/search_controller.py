from __future__ import annotations

from ..coordinators.search_coordinator import SearchCoordinator
from ...json_handler import JsonRequestHandler
from ...shared.typed_dict import to_dict_with_type


class SearchController():
   @staticmethod
   def search( handler: JsonRequestHandler ) -> None:
      data = handler._read_json_body()

      query = ( data.get( 'query' ) or '' ).strip()
      include_animals = bool( data.get( 'includeAnimals' ) )
      include_pavilions = bool( data.get( 'includePavilions' ) )
      include_restaurants = bool( data.get( 'includeRestaurants' ) )
      include_restrooms = bool( data.get( 'includeRestrooms' ) )
      include_gift_shops = bool( data.get( 'includeGiftShops' ) )
      include_attractions = bool( data.get( 'includeAttractions' ) )
      include_zoomobile_stations = bool( data.get( 'includeZoomobileStations' ) )
      include_guardians_talks = bool( data.get( 'includeGuardiansTalks' ) )
      include_wild_encounters = bool( data.get( 'includeWildEncounters' ) )

      month = data.get( 'month' )
      day = data.get( 'day' )
      year = data.get( 'year' )
      temp = data.get( 'temp' )

      include_off_display_animals = bool( data.get( 'includeOffDisplayAnimals' ) )
      for_itinerary = bool( data.get( 'forItinerary' ) )
      include_closed_restaurants = bool( data.get( 'includeClosedRestaurants' ) )
      include_closed_restrooms = bool( data.get( 'includeClosedRestrooms' ) )
      include_closed_attractions = bool( data.get( 'includeClosedAttractions' ) )
      zoomobile_route = data.get( 'zoomobileRoute' )

      results = SearchCoordinator.search(
         query=query,
         include_animals=include_animals,
         include_pavilions=include_pavilions,
         include_restaurants=include_restaurants,
         include_restrooms=include_restrooms,
         include_gift_shops=include_gift_shops,
         include_attractions=include_attractions,
         include_zoomobile_stations=include_zoomobile_stations,
         include_guardians_talks=include_guardians_talks,
         include_wild_encounters=include_wild_encounters,
         month=month,
         day=day,
         year=year,
         temp=temp,
         include_off_display_animals=include_off_display_animals,
         for_itinerary=for_itinerary,
         include_closed_restaurants=include_closed_restaurants,
         include_closed_restrooms=include_closed_restrooms,
         include_closed_attractions=include_closed_attractions,
         zoomobile_route=zoomobile_route )

      handler._write_json( {
         'animals': [
            to_dict_with_type( animal, 'animal' )
            for animal in results[ 'animals' ]
         ],
         'pavilions': [
            to_dict_with_type( pavilion, 'pavilion' )
            for pavilion in results[ 'pavilions' ]
         ],
         'restaurants': [
            to_dict_with_type( restaurant, 'restaurant' )
            for restaurant in results[ 'restaurants' ]
         ],
         'restrooms': [
            to_dict_with_type( restroom, 'restroom' )
            for restroom in results[ 'restrooms' ]
         ],
         'gift_shops': [
            to_dict_with_type( gift_shop, 'giftShop' )
            for gift_shop in results[ 'gift_shops' ]
         ],
         'attractions': [
            to_dict_with_type( attraction, 'attraction' )
            for attraction in results[ 'attractions' ]
         ],
         'zoomobile_stations': [
            to_dict_with_type( zoomobile_station, 'zoomobileStation' )
            for zoomobile_station in results[ 'zoomobile_stations' ]
         ],
         'wild_encounters': [
            to_dict_with_type( wild_encounter, 'wildEncounter' )
            for wild_encounter in results[ 'wild_encounters' ]
         ],
         'guardians_talks': [
            to_dict_with_type( guardians_talk, 'guardiansTalk' )
            for guardians_talk in results[ 'guardians_talks' ]
         ],
      } )
