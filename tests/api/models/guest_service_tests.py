from __future__ import annotations

from api.models.guest_service import GuestService


def Test_ToDict_TestGuestServiceFields_ExpectFrontendShape() -> None:
   guest_service = GuestService(
      service_type='Information',
      x_coord=9,
      y_coord=10 )

   result = guest_service.to_dict()

   assert result[ 'service_type' ] == guest_service.service_type
   assert result[ 'x_coord' ] == guest_service.x_coord
   assert result[ 'y_coord' ] == guest_service.y_coord
