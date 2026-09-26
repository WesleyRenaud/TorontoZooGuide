from __future__ import annotations

from api.models.picnic_site import PicnicSite


def Test_ToDict_TestCoordinates_ExpectFrontendShape() -> None:
   picnic_site = PicnicSite(
      x_coord=11,
      y_coord=12 )

   result = picnic_site.to_dict()

   assert result[ 'x_coord' ] == picnic_site.x_coord
   assert result[ 'y_coord' ] == picnic_site.y_coord
