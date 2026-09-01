from __future__ import annotations

from api.models.attraction import Attraction


def Test_ToDict_TestAttractionFields_ExpectFrontendShape() -> None:
   assert Attraction(
      name='Ride',
      free_with_admission=1,
      region='Front Courtyard',
   ).to_dict()[ 'free_with_admission' ] is True
   assert Attraction(
      name='Ride',
      free_with_admission=1,
      region='Front Courtyard',
   ).to_dict()[ 'region' ] == 'Front Courtyard'
   assert Attraction( name='Ride', free_with_admission=1 ).to_dict()[ 'is_deleted' ] is False
