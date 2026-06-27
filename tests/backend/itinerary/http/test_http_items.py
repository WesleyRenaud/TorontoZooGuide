from __future__ import annotations

from http_support import make_handler, response_json, StubZooControllers

from api.itinerary.animal_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_item_key import AttractionScheduleItemKey
import api.server as server


def test_unschedule_itinerary_item_endpoint(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/unschedule-itinerary-item',
      {
         'itemType': 'animals',
         'key': 'African Lion||Africa Savanna',
      } )

   server.MyHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'unschedule_itinerary_item',
         {
            'schedule_item_key': AnimalScheduleItemKey(
               species='African Lion',
               exhibit='Africa Savanna' ),
         },
      ),
   ]


def test_unschedule_all_itinerary_items_endpoint(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/unschedule-all-itinerary-items',
      {
         'temp': True,
      } )

   server.MyHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert response[ 'itinerary_config' ] is not None
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'unschedule_all_itinerary_items',
         {
            'visit_date_temp': True,
         },
      ),
   ]


def test_remove_item_from_itinerary_endpoint(
      stub_database: type[ StubZooControllers ] ) -> None:
   handler = make_handler(
      '/remove-item-from-itinerary',
      {
         'itemType': 'attractions',
         'key': 'Conservation Carousel',
      } )

   server.MyHandler.do_POST( handler )

   response = response_json( handler )
   assert response[ 'status' ] == 'success'
   assert response[ 'reasons' ] == []
   assert response[ 'itinerary' ] is not None
   assert StubZooControllers.instances[ 0 ].calls == [
      (
         'remove_itinerary_item',
         {
            'schedule_item_key': AttractionScheduleItemKey(
               name='Conservation Carousel' ),
         },
      ),
   ]
