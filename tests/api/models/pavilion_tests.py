from __future__ import annotations

from api.models.pavilion import Pavilion


def Test_ToDict_TestPavilionFields_ExpectFrontendShape() -> None:
   assert Pavilion( name='Pavilion', region='Region', x_coord=1, y_coord=2 ).to_dict() == {
      'name': 'Pavilion',
      'region': 'Region',
      'description': None,
      'x_coord': 1,
      'y_coord': 2,
   }
