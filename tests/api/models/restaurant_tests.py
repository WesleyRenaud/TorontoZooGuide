from __future__ import annotations

from api.models.restaurant import Restaurant
from api.shared.value_conversion import ValueConversion


def Test_ToDict_TestClosedFlag_ExpectFrontendShape() -> None:
   restaurant = Restaurant(
      name='Cafe',
      location='North',
      sub_location='Inside',
      is_closed=1,
      likelihood=0 )

   result = restaurant.to_dict()

   assert result[ 'is_closed' ] is ValueConversion.as_boolean( restaurant.is_closed )
