from __future__ import annotations

from api.models.emergency_intercom import EmergencyIntercom


def Test_ToDict_TestCoordinates_ExpectFrontendShape() -> None:
   assert EmergencyIntercom( x_coord=7, y_coord=8 ).to_dict() == {
      'x_coord': 7,
      'y_coord': 8,
   }
