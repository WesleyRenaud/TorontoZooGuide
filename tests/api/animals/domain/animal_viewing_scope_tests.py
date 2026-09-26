from __future__ import annotations

from api.animals.domain.animal_viewing_scope import AnimalViewingScope


def Test_FromEnclosureName_TestBlank_ExpectUnnamedMain() -> None:
   name = '  '

   scope = AnimalViewingScope.from_enclosure_name( name )

   assert scope.enclosure_name == ''
   assert scope.label == AnimalViewingScope.UNNAMED_LABEL


def Test_FromEnclosureName_TestNone_ExpectUnnamedMain() -> None:
   name = None

   scope = AnimalViewingScope.from_enclosure_name( name )

   assert scope.enclosure_name == ''
   assert scope.label == AnimalViewingScope.UNNAMED_LABEL


def Test_FromEnclosureName_TestNamed_ExpectTrimmedName() -> None:
   enclosure_name = 'Male Herd'
   name = f' { enclosure_name } '

   scope = AnimalViewingScope.from_enclosure_name( name )

   assert scope.enclosure_name == enclosure_name
   assert scope.label == enclosure_name


def Test_ToDict_TestUnnamed_ExpectFrontendShape() -> None:
   scope = AnimalViewingScope.from_enclosure_name( '' )

   result = scope.to_dict()

   assert result[ 'enclosureName' ] == scope.enclosure_name
   assert result[ 'label' ] == scope.label


def Test_ToDict_TestNamed_ExpectFrontendShape() -> None:
   enclosure_name = 'Male Herd'
   scope = AnimalViewingScope.from_enclosure_name( enclosure_name )

   result = scope.to_dict()

   assert result[ 'enclosureName' ] == scope.enclosure_name
   assert result[ 'label' ] == scope.label
