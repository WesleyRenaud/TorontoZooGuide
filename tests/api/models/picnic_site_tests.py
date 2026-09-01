from __future__ import annotations

from api.models.picnic_site import PicnicSite


def Test_ToDict_TestCoordinates_ExpectFrontendShape() -> None:
   assert PicnicSite(
      x_coord=11,
      y_coord=12,
   ).to_dict() == {
      'x_coord': 11,
      'y_coord': 12,
   }
