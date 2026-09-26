from __future__ import annotations

from api.models.guardians_talk import GuardiansTalk
from api.shared.value_conversion import ValueConversion


def Test_ToDict_TestGuardiansTalkFields_ExpectFrontendShape() -> None:
   talk = GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 )

   result = talk.to_dict()

   assert result[ 'name' ] == talk.name
   assert result[ 'location' ] == talk.location
   assert result[ 'is_available' ] is ValueConversion.as_boolean( talk.is_available )
   assert result[ 'is_deleted' ] is ValueConversion.as_boolean( talk.is_deleted )
