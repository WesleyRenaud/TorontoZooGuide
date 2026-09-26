from __future__ import annotations

from api.animals.domain.animal_viewing_scope import AnimalViewingScope
from api.animals.domain.animal_viewing_scope_mapper import AnimalViewingScopeMapper


def Test_MapPayload_TestStrings_ExpectScopes() -> None:
   male_herd = 'Male Herd'
   unnamed = ''
   female_herd = '  Female Herd  '
   values = [ male_herd, unnamed, female_herd ]

   scopes = AnimalViewingScopeMapper.map_payload( values )

   assert scopes == [
      AnimalViewingScope.from_enclosure_name( male_herd ),
      AnimalViewingScope.from_enclosure_name( unnamed ),
      AnimalViewingScope.from_enclosure_name( female_herd ),
   ]
