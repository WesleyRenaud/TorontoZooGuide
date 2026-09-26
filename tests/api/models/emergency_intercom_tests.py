from __future__ import annotations

from api.models.emergency_intercom import EmergencyIntercom


def Test_ToDict_TestCoordinates_ExpectFrontendShape() -> None:
   intercom = EmergencyIntercom( x_coord=7, y_coord=8 )

   result = intercom.to_dict()

   assert result[ 'x_coord' ] == intercom.x_coord
   assert result[ 'y_coord' ] == intercom.y_coord
