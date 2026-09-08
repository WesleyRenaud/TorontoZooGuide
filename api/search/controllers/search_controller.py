from __future__ import annotations

from ..coordinators.search_coordinator import SearchCoordinator
from ...json_request_handler import JsonRequestHandler
from ...shared.enums.item_type import ItemType
from ...shared.typed_dict_mapper import TypedDictMapper


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
      include_transportations = bool( data.get( 'includeTransportations' ) )
      include_transportation_stations = bool( data.get( 'includeTransportationStations' ) )
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
      transportation_route = data.get( 'transportationRoute' )

      results = SearchCoordinator.search(
         query=query,
         include_animals=include_animals,
         include_pavilions=include_pavilions,
         include_restaurants=include_restaurants,
         include_restrooms=include_restrooms,
         include_gift_shops=include_gift_shops,
         include_attractions=include_attractions,
         include_transportations=include_transportations,
         include_transportation_stations=include_transportation_stations,
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
         transportation_route=transportation_route )

      handler._write_json( {
         'animals': [
            TypedDictMapper.to_dict_with_type( animal, ItemType.ANIMAL.value )
            for animal in results[ 'animals' ]
         ],
         'pavilions': [
            TypedDictMapper.to_dict_with_type( pavilion, ItemType.PAVILION.value )
            for pavilion in results[ 'pavilions' ]
         ],
         'restaurants': [
            TypedDictMapper.to_dict_with_type(
               restaurant,
               ItemType.RESTAURANT.value )
            for restaurant in results[ 'restaurants' ]
         ],
         'restrooms': [
            TypedDictMapper.to_dict_with_type( restroom, ItemType.RESTROOM.value )
            for restroom in results[ 'restrooms' ]
         ],
         'gift_shops': [
            TypedDictMapper.to_dict_with_type( gift_shop, ItemType.GIFT_SHOP.value )
            for gift_shop in results[ 'gift_shops' ]
         ],
         'attractions': [
            TypedDictMapper.to_dict_with_type(
               attraction,
               ItemType.ATTRACTION.value )
            for attraction in results[ 'attractions' ]
         ],
         'transportations': [
            TypedDictMapper.to_dict_with_type(
               transportation,
               ItemType.TRANSPORTATION.value )
            for transportation in results[ 'transportations' ]
         ],
         'transportation_stations': [
            TypedDictMapper.to_dict_with_type(
               transportation_station,
               ItemType.TRANSPORTATION_STATION.value )
            for transportation_station in results[ 'transportation_stations' ]
         ],
         'wild_encounters': [
            TypedDictMapper.to_dict_with_type(
               wild_encounter,
               ItemType.WILD_ENCOUNTER.value )
            for wild_encounter in results[ 'wild_encounters' ]
         ],
         'guardians_talks': [
            TypedDictMapper.to_dict_with_type(
               guardians_talk,
               ItemType.GUARDIANS_TALK.value )
            for guardians_talk in results[ 'guardians_talks' ]
         ],
      } )
