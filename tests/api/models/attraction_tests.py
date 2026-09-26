from __future__ import annotations

from api.models.attraction import Attraction
from api.shared.value_conversion import ValueConversion


def Test_ToDict_TestAttractionFields_ExpectFrontendShape() -> None:
   attraction = Attraction(
      name='Ride',
      free_with_admission=1,
      region='Front Courtyard' )

   result = attraction.to_dict()

   assert result[ 'name' ] == attraction.name
   assert result[ 'free_with_admission' ] is ValueConversion.as_boolean(
      attraction.free_with_admission )
   assert result[ 'region' ] == attraction.region
   assert result[ 'is_deleted' ] is ValueConversion.as_boolean( attraction.is_deleted )
