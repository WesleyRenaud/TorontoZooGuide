from __future__ import annotations

from api.models.pavilion import Pavilion


def Test_ToDict_TestPavilionFields_ExpectFrontendShape() -> None:
   pavilion = Pavilion( name='Pavilion', region='Region', x_coord=1, y_coord=2 )

   result = pavilion.to_dict()

   assert result[ 'name' ] == pavilion.name
   assert result[ 'region' ] == pavilion.region
   assert result[ 'description' ] == pavilion.description
   assert result[ 'x_coord' ] == pavilion.x_coord
   assert result[ 'y_coord' ] == pavilion.y_coord
