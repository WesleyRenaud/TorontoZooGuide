from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.picnic_sites.data_access.picnic_site_mapper import PicnicSiteMapper


X_COORD = 12.5
Y_COORD = 67.5


def Test_MapRecord_TestRow_ExpectCoordinatesMapped() -> None:
   picnic_site = PicnicSiteMapper.map_record(
      make_row( {
         'X_COORD': X_COORD,
         'Y_COORD': Y_COORD,
      } ) )

   assert picnic_site.x_coord == X_COORD
   assert picnic_site.y_coord == Y_COORD
