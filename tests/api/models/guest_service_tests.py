from __future__ import annotations

from api.models.guest_service import GuestService


def Test_ToDict_TestGuestServiceFields_ExpectFrontendShape() -> None:
   assert GuestService(
      service_type='Information',
      x_coord=9,
      y_coord=10,
   ).to_dict() == {
      'service_type': 'Information',
      'x_coord': 9,
      'y_coord': 10,
   }
