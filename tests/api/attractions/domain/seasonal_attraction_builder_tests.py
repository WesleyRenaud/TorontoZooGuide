from __future__ import annotations

from datetime import date

from api.attractions.data_access.attraction_closure_record import AttractionClosureRecord
from api.attractions.domain.attraction_info_link import AttractionInfoLink
from api.attractions.domain.seasonal_attraction import SeasonalAttraction
from api.attractions.domain.seasonal_attraction_builder import SeasonalAttractionBuilder


SPLASH = 'Splash Island'
LINK = 'https://www.torontozoo.com/tz/splash'


def Test_Build_TestClosures_ExpectAttractionNameStatusAndDates() -> None:
   attractions = SeasonalAttractionBuilder.build(
      attractions=[
         AttractionInfoLink( name=SPLASH, info_link=LINK ),
         AttractionInfoLink( name='Kangaroo Walk-Thru', info_link='https://www.torontozoo.com/tz/kangaroo' ),
      ],
      closure_records=[
         AttractionClosureRecord(
            attraction=SPLASH,
            closed_start='2026-11-02',
            closed_end='2026-11-30',
            closed_message=None,
            is_closed_for_season=True,
         ),
         AttractionClosureRecord(
            attraction='Missing Start',
            closed_start=None,
            closed_end=None,
            closed_message=None,
            is_closed_for_season=True,
         ),
         AttractionClosureRecord(
            attraction='Gorilla Climb',
            closed_start='2026-10-01',
            closed_end=None,
            closed_message=None,
            is_closed_for_season=True,
         ),
      ],
   )

   assert attractions == [
      SeasonalAttraction(
         name=SPLASH,
         info_link=LINK,
         is_closed=True,
         start=date( 2026, 11, 2 ),
         end=date( 2026, 11, 30 ),
         closed_for_season=True,
      ),
      SeasonalAttraction(
         name='Kangaroo Walk-Thru',
         info_link='https://www.torontozoo.com/tz/kangaroo',
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      ),
      SeasonalAttraction(
         name='Gorilla Climb',
         info_link='',
         is_closed=True,
         start=date( 2026, 10, 1 ),
         end=None,
         closed_for_season=True,
      ),
   ]


def Test_ClosedForSeasonOn_TestOpenEndedRange_ExpectOnlyCoveredDate() -> None:
   attraction = SeasonalAttraction(
      name=SPLASH,
      info_link=LINK,
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
      closed_for_season=True,
   )

   assert attraction.closed_for_season_on( date( 2026, 11, 1 ) ) is False
   assert attraction.closed_for_season_on( date( 2026, 11, 2 ) ) is True
