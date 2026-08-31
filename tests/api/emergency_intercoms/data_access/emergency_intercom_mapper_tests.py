from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.emergency_intercoms.data_access.emergency_intercom_mapper import EmergencyIntercomMapper


X_COORD = 12.5
Y_COORD = 67.5


def Test_MapRecord_TestRow_ExpectCoordinatesMapped() -> None:
   emergency_intercom = EmergencyIntercomMapper.map_record(
      make_row( {
         'X_COORD': X_COORD,
         'Y_COORD': Y_COORD,
      } ) )

   assert emergency_intercom.x_coord == X_COORD
   assert emergency_intercom.y_coord == Y_COORD
