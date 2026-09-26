from __future__ import annotations

from api.models.defibrillator import Defibrillator


def Test_ToDict_TestCoordinates_ExpectFrontendShape() -> None:
   defibrillator = Defibrillator( x_coord=5, y_coord=6 )

   result = defibrillator.to_dict()

   assert result[ 'x_coord' ] == defibrillator.x_coord
   assert result[ 'y_coord' ] == defibrillator.y_coord
