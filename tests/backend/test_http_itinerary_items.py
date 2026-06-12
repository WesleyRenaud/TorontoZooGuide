from __future__ import annotations

from http_support import make_handler, response_json, StubZooControllers

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
            'item_type': 'animals',
            'key': 'African Lion||Africa Savanna',
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
            'item_type': 'attractions',
            'key': 'Conservation Carousel',
         },
      ),
   ]
