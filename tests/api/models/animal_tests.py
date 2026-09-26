from __future__ import annotations

from api.models.animal import Animal
from api.shared.value_conversion import ValueConversion


def Test_ToDict_TestBooleanFlags_ExpectFrontendShape() -> None:
   animal = Animal(
      species='Amur Tiger',
      has_limited_viewing_schedule=1,
      viewing_alert_messages=[] )

   result = animal.to_dict()

   assert result[ 'species' ] == animal.species
   assert result[ 'has_limited_viewing_schedule' ] is ValueConversion.as_boolean(
      animal.has_limited_viewing_schedule )
   assert result[ 'has_viewing_alert' ] is bool( animal.viewing_alert_messages )
   assert result[ 'added_by_transportation' ] is ValueConversion.as_boolean(
      animal.added_by_transportation )
   assert result[ 'is_zoomobile_only' ] is ValueConversion.as_boolean(
      animal.is_zoomobile_only )
   assert result[ 'transportation' ] is animal.transportation
   assert result[ 'is_deleted' ] is ValueConversion.as_boolean( animal.is_deleted )
