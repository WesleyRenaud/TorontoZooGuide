from __future__ import annotations

from api.models.defibrillator import Defibrillator


def Test_ToDict_TestCoordinates_ExpectFrontendShape() -> None:
   assert Defibrillator( x_coord=5, y_coord=6 ).to_dict() == {
      'x_coord': 5,
      'y_coord': 6,
   }
