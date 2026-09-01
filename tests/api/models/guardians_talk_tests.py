from __future__ import annotations

from api.models.guardians_talk import GuardiansTalk


def Test_ToDict_TestGuardiansTalkFields_ExpectFrontendShape() -> None:
   assert GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 ).to_dict()[ 'is_available' ] is True
   assert GuardiansTalk( name='Talk', location='Habitat', x_coord=1, y_coord=2 ).to_dict()[ 'is_deleted' ] is False
