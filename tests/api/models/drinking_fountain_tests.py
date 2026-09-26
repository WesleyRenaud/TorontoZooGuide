from __future__ import annotations

from api.models.drinking_fountain import DrinkingFountain


def Test_ToDict_TestClosedFountain_ExpectFrontendShape() -> None:
   fountain = DrinkingFountain( x_coord=1, y_coord=2, is_closed=1, likelihood=0.0 )

   result = fountain.to_dict()

   assert result[ 'x_coord' ] == fountain.x_coord
   assert result[ 'y_coord' ] == fountain.y_coord
   assert result[ 'is_closed' ] is fountain.is_closed
   assert result[ 'closed_message' ] == fountain.closed_message
   assert result[ 'likelihood' ] == fountain.likelihood
