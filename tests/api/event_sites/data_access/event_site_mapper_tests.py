from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.event_sites.data_access.event_site_mapper import EventSiteMapper


EVENT_SITE_NAME = 'Special Events Center'
X_COORD = 12.5
Y_COORD = 67.5


def Test_MapRecord_TestRow_ExpectNameAndCoordinatesMapped() -> None:
   event_site = EventSiteMapper.map_record(
      make_row( {
         'NAME': EVENT_SITE_NAME,
         'X_COORD': X_COORD,
         'Y_COORD': Y_COORD,
      } ) )

   assert event_site.name == EVENT_SITE_NAME
   assert event_site.x_coord == X_COORD
   assert event_site.y_coord == Y_COORD
