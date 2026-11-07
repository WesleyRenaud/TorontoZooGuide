from __future__ import annotations

from datetime import date

from api.restaurants.data_access.restaurant_closure_record import RestaurantClosureRecord
from api.restaurants.domain.restaurant_menu_link import RestaurantMenuLink
from api.restaurants.domain.seasonal_restaurant import SeasonalRestaurant
from api.restaurants.domain.seasonal_restaurant_builder import SeasonalRestaurantBuilder


AFRICA = 'Africa Restaurant'
MENU_LINK = 'https://www.torontozoo.com/!/pdfs/food/africa.pdf'


def Test_Build_TestClosures_ExpectRestaurantNameStatusAndDates() -> None:
   restaurants = SeasonalRestaurantBuilder.build(
      restaurants=[
         RestaurantMenuLink( name=AFRICA, menu_link=MENU_LINK ),
         RestaurantMenuLink( name='Savanna Snack Bar', menu_link='' ),
      ],
      closure_records=[
         RestaurantClosureRecord(
            restaurant=AFRICA,
            closed_start='2026-11-02',
            closed_end='2026-11-30',
            closed_message=None,
            is_closed_for_season=True,
         ),
         RestaurantClosureRecord(
            restaurant='Missing Start',
            closed_start=None,
            closed_end=None,
            closed_message=None,
            is_closed_for_season=True,
         ),
         RestaurantClosureRecord(
            restaurant='Tundra Tacos',
            closed_start='2026-10-01',
            closed_end=None,
            closed_message=None,
            is_closed_for_season=True,
         ),
      ],
   )

   assert restaurants == [
      SeasonalRestaurant(
         name=AFRICA,
         menu_link=MENU_LINK,
         is_closed=True,
         start=date( 2026, 11, 2 ),
         end=date( 2026, 11, 30 ),
         closed_for_season=True,
      ),
      SeasonalRestaurant(
         name='Savanna Snack Bar',
         menu_link='',
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      ),
      SeasonalRestaurant(
         name='Missing Start',
         menu_link='',
         is_closed=True,
         start=None,
         end=None,
         closed_for_season=True,
      ),
      SeasonalRestaurant(
         name='Tundra Tacos',
         menu_link='',
         is_closed=True,
         start=date( 2026, 10, 1 ),
         end=None,
         closed_for_season=True,
      ),
   ]


def Test_ClosedForSeasonOn_TestOpenEndedRange_ExpectOnlyCoveredDate() -> None:
   restaurant = SeasonalRestaurant(
      name=AFRICA,
      menu_link=MENU_LINK,
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
      closed_for_season=True,
   )

   assert restaurant.closed_for_season_on( date( 2026, 11, 2 ) )
   assert not restaurant.closed_for_season_on( date( 2026, 11, 1 ) )


def Test_ClosedForSeasonOn_TestMissingStart_ExpectClosed() -> None:
   restaurant = SeasonalRestaurant(
      name=AFRICA,
      menu_link=MENU_LINK,
      is_closed=True,
      start=None,
      end=None,
      closed_for_season=True,
   )

   assert restaurant.closed_for_season_on( date( 2026, 11, 2 ) )
