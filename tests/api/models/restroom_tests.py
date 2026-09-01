from __future__ import annotations

from api.models.restroom import Restroom


def Test_ToDict_TestTitle_ExpectFrontendShape() -> None:
   assert Restroom( title='Restroom', x_coord=3, y_coord=4 ).to_dict()[ 'title' ] == 'Restroom'
