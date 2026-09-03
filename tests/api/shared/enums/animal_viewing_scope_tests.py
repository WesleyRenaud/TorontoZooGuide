from __future__ import annotations

from api.shared.enums import AnimalViewingScope

def Test_Normalize_TestKnownValues_ExpectMatchingScope() -> None:
   assert AnimalViewingScope.normalize( 'ALL' ) == AnimalViewingScope.ALL
   assert AnimalViewingScope.normalize( ' indoor ' ) == AnimalViewingScope.INDOOR
   assert AnimalViewingScope.normalize( 'outdoor' ) == AnimalViewingScope.OUTDOOR

def Test_Normalize_TestUnknownOrNone_ExpectNone() -> None:
   assert AnimalViewingScope.normalize( None ) is None
   assert AnimalViewingScope.normalize( 'aviary' ) is None

def Test_OppositeScope_TestIndoorOutdoorAll_ExpectSwappedOrNone() -> None:
   assert AnimalViewingScope.opposite_scope(
      AnimalViewingScope.INDOOR ) == AnimalViewingScope.OUTDOOR
   assert AnimalViewingScope.opposite_scope(
      AnimalViewingScope.OUTDOOR ) == AnimalViewingScope.INDOOR
   assert AnimalViewingScope.opposite_scope( AnimalViewingScope.ALL ) is None
