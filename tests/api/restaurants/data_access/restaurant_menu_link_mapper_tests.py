from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.restaurants.data_access.restaurant_menu_link_mapper import RestaurantMenuLinkMapper
from api.restaurants.domain.restaurant_menu_link import RestaurantMenuLink


NAME = 'Simba Spot'
MENU_LINK = 'https://www.torontozoo.com/!/pdfs/food/simba.pdf'


def Test_MapRecord_TestRow_ExpectNameAndMenuLink() -> None:
   row = make_row( {
      'NAME': NAME,
      'MENU_LINK': MENU_LINK,
   } )

   restaurant = RestaurantMenuLinkMapper.map_record( row )

   assert restaurant == RestaurantMenuLink( name=NAME, menu_link=MENU_LINK )


def Test_MapRecord_TestBlankLink_ExpectEmptyLink() -> None:
   row = make_row( {
      'NAME': NAME,
      'MENU_LINK': '  ',
   } )

   restaurant = RestaurantMenuLinkMapper.map_record( row )

   assert restaurant == RestaurantMenuLink( name=NAME, menu_link='' )
