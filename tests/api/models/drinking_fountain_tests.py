from __future__ import annotations

from api.models.drinking_fountain import DrinkingFountain


def Test_ToDict_TestClosedFountain_ExpectFrontendShape() -> None:
   assert DrinkingFountain( x_coord=1, y_coord=2, is_closed=1, likelihood=0.0 ).to_dict() == {
      'x_coord': 1,
      'y_coord': 2,
      'is_closed': True,
      'closed_message': None,
      'likelihood': 0.0,
   }
