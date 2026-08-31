from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.defibrillators.data_access.defibrillator_mapper import DefibrillatorMapper


X_COORD = 12.5
Y_COORD = 67.5


def Test_MapRecord_TestRow_ExpectCoordinatesMapped() -> None:
   defibrillator = DefibrillatorMapper.map_record(
      make_row( {
         'X_COORD': X_COORD,
         'Y_COORD': Y_COORD,
      } ) )

   assert defibrillator.x_coord == X_COORD
   assert defibrillator.y_coord == Y_COORD
