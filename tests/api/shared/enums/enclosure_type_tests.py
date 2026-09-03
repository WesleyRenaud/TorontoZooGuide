from __future__ import annotations

import pytest

from api.shared.enums.enclosure_type import EnclosureType

def Test_Normalize_TestKnownValues_ExpectMatchingType() -> None:
   assert EnclosureType.normalize( 'Indoor' ) == EnclosureType.INDOOR
   assert EnclosureType.normalize( ' Outdoor ' ) == EnclosureType.OUTDOOR

def Test_Normalize_TestUnknownOrEmpty_ExpectNone() -> None:
   assert EnclosureType.normalize( None ) is None
   assert EnclosureType.normalize( '' ) is None
   assert EnclosureType.normalize( 'aviary' ) is None

def Test_NormalizedEnclosureType_TestKnownValues_ExpectLowercaseValue() -> None:
   assert EnclosureType.normalized_enclosure_type( 'Indoor' ) == 'indoor'
   assert EnclosureType.normalized_enclosure_type( ' outdoor ' ) == 'outdoor'

def Test_NormalizedEnclosureType_TestUnknownOrEmpty_ExpectNone() -> None:
   assert EnclosureType.normalized_enclosure_type( None ) is None
   assert EnclosureType.normalized_enclosure_type( '' ) is None
   assert EnclosureType.normalized_enclosure_type( 'mixed' ) is None

def Test_IsIndoorOrOutdoor_TestNormalizedValues_ExpectFlags() -> None:
   assert EnclosureType.is_indoor( 'Indoor' )
   assert not EnclosureType.is_indoor( 'Outdoor' )
   assert EnclosureType.is_outdoor( 'Outdoor' )
   assert not EnclosureType.is_outdoor( 'Indoor' )

def Test_OppositeType_TestIndoorOutdoor_ExpectSwapped() -> None:
   assert EnclosureType.opposite_type( EnclosureType.INDOOR ) == EnclosureType.OUTDOOR
   assert EnclosureType.opposite_type( EnclosureType.OUTDOOR ) == EnclosureType.INDOOR

def Test_NormalizeViewingSpotName_TestEnclosureTypeOrEmpty_ExpectNone() -> None:
   assert EnclosureType.normalize_viewing_spot_name( None ) is None
   assert EnclosureType.normalize_viewing_spot_name( 'Indoor' ) is None
   assert EnclosureType.normalize_viewing_spot_name( 'Outdoor' ) is None

def Test_NormalizeViewingSpotName_TestCustomSpotName_ExpectTrimmedValue() -> None:
   assert EnclosureType.normalize_viewing_spot_name( '  Penguin Beach  ' ) == 'Penguin Beach'
