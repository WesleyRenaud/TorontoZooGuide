from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.guest_services.data_access.guest_service_mapper import GuestServiceMapper


SERVICE_TYPE = 'Information'
X_COORD = 12.5
Y_COORD = 67.5


def Test_MapRecord_TestRow_ExpectServiceTypeAndCoordinatesMapped() -> None:
   guest_service = GuestServiceMapper.map_record(
      make_row( {
         'SERVICE_TYPE': SERVICE_TYPE,
         'X_COORD': X_COORD,
         'Y_COORD': Y_COORD,
      } ) )

   assert guest_service.service_type == SERVICE_TYPE
   assert guest_service.x_coord == X_COORD
   assert guest_service.y_coord == Y_COORD
