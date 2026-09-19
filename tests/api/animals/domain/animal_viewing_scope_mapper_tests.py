from __future__ import annotations

from api.animals.domain.animal_viewing_scope import AnimalViewingScope
from api.animals.domain.animal_viewing_scope_mapper import AnimalViewingScopeMapper


def Test_MapPayload_TestStrings_ExpectScopes() -> None:
   assert AnimalViewingScopeMapper.map_payload(
      [ 'Male Herd', '', '  Female Herd  ' ]
   ) == [
      AnimalViewingScope.from_enclosure_name( 'Male Herd' ),
      AnimalViewingScope.from_enclosure_name( '' ),
      AnimalViewingScope.from_enclosure_name( 'Female Herd' ),
   ]
