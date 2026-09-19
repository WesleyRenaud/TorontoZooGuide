from __future__ import annotations

from api.animals.domain.animal_viewing_scope import AnimalViewingScope


def Test_FromEnclosureName_TestBlankAndNamed_ExpectNormalizedScope() -> None:
   unnamed = AnimalViewingScope.from_enclosure_name( '  ' )
   named = AnimalViewingScope.from_enclosure_name( ' Male Herd ' )

   assert AnimalViewingScope.from_enclosure_name( None ) == unnamed

   assert unnamed.enclosure_name == ''
   assert unnamed.label == 'Main'
   assert unnamed.to_dict() == {
      'enclosureName': '',
      'label': 'Main',
   }
   assert named.enclosure_name == 'Male Herd'
   assert named.label == 'Male Herd'
   assert named.to_dict() == {
      'enclosureName': 'Male Herd',
      'label': 'Male Herd',
   }
