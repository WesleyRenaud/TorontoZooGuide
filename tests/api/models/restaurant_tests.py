from __future__ import annotations

from api.models.restaurant import Restaurant


def Test_ToDict_TestClosedFlag_ExpectFrontendShape() -> None:
   assert Restaurant(
      name='Cafe',
      location='North',
      sub_location='Inside',
      is_closed=1,
      likelihood=0,
   ).to_dict()[ 'is_closed' ] is True
