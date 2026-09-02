from __future__ import annotations

from api.models.animal import Animal


def Test_ToDict_TestBooleanFlags_ExpectFrontendShape() -> None:
   animal = Animal(
      species='Amur Tiger',
      has_limited_viewing_schedule=1,
      viewing_alert_messages=[] )

   result = animal.to_dict()

   assert result[ 'species' ] == 'Amur Tiger'
   assert result[ 'has_limited_viewing_schedule' ] is True
   assert result[ 'has_viewing_alert' ] is False
   assert result[ 'is_deleted' ] is False
