from __future__ import annotations

from api.shared.enums.enclosure_type import EnclosureType


def Test_Normalize_TestIndoor_ExpectIndoorType() -> None:
   value = EnclosureType.INDOOR.value.title()

   enclosure_type = EnclosureType.normalize( value )

   assert enclosure_type == EnclosureType.INDOOR


def Test_Normalize_TestOutdoorWhitespace_ExpectOutdoorType() -> None:
   value = f' { EnclosureType.OUTDOOR.value.title() } '

   enclosure_type = EnclosureType.normalize( value )

   assert enclosure_type == EnclosureType.OUTDOOR


def Test_Normalize_TestNone_ExpectNone() -> None:
   value = None

   enclosure_type = EnclosureType.normalize( value )

   assert enclosure_type is None


def Test_Normalize_TestEmpty_ExpectNone() -> None:
   value = ''

   enclosure_type = EnclosureType.normalize( value )

   assert enclosure_type is None


def Test_Normalize_TestUnknown_ExpectNone() -> None:
   value = 'aviary'

   enclosure_type = EnclosureType.normalize( value )

   assert enclosure_type is None


def Test_NormalizedEnclosureType_TestIndoor_ExpectLowercaseValue() -> None:
   value = EnclosureType.INDOOR.value.title()

   normalized = EnclosureType.normalized_enclosure_type( value )

   assert normalized == value.strip().lower()


def Test_NormalizedEnclosureType_TestOutdoorWhitespace_ExpectLowercaseValue() -> None:
   value = f' { EnclosureType.OUTDOOR.value } '

   normalized = EnclosureType.normalized_enclosure_type( value )

   assert normalized == value.strip().lower()


def Test_NormalizedEnclosureType_TestNone_ExpectNone() -> None:
   value = None

   normalized = EnclosureType.normalized_enclosure_type( value )

   assert normalized is None


def Test_NormalizedEnclosureType_TestEmpty_ExpectNone() -> None:
   value = ''

   normalized = EnclosureType.normalized_enclosure_type( value )

   assert normalized is None


def Test_NormalizedEnclosureType_TestUnknown_ExpectNone() -> None:
   value = 'mixed'

   normalized = EnclosureType.normalized_enclosure_type( value )

   assert normalized is None


def Test_IsIndoor_TestIndoor_ExpectTrue() -> None:
   value = EnclosureType.INDOOR.value.title()

   is_indoor = EnclosureType.is_indoor( value )

   assert is_indoor


def Test_IsIndoor_TestOutdoor_ExpectFalse() -> None:
   value = EnclosureType.OUTDOOR.value.title()

   is_indoor = EnclosureType.is_indoor( value )

   assert not is_indoor


def Test_IsOutdoor_TestOutdoor_ExpectTrue() -> None:
   value = EnclosureType.OUTDOOR.value.title()

   is_outdoor = EnclosureType.is_outdoor( value )

   assert is_outdoor


def Test_IsOutdoor_TestIndoor_ExpectFalse() -> None:
   value = EnclosureType.INDOOR.value.title()

   is_outdoor = EnclosureType.is_outdoor( value )

   assert not is_outdoor


def Test_OppositeType_TestIndoor_ExpectOutdoor() -> None:
   enclosure_type = EnclosureType.INDOOR

   opposite = EnclosureType.opposite_type( enclosure_type )

   assert opposite == EnclosureType.OUTDOOR


def Test_OppositeType_TestOutdoor_ExpectIndoor() -> None:
   enclosure_type = EnclosureType.OUTDOOR

   opposite = EnclosureType.opposite_type( enclosure_type )

   assert opposite == EnclosureType.INDOOR


def Test_NormalizeViewingSpotName_TestNone_ExpectNone() -> None:
   value = None

   normalized = EnclosureType.normalize_viewing_spot_name( value )

   assert normalized is None


def Test_NormalizeViewingSpotName_TestIndoor_ExpectNone() -> None:
   value = EnclosureType.INDOOR.value.title()

   normalized = EnclosureType.normalize_viewing_spot_name( value )

   assert normalized is None


def Test_NormalizeViewingSpotName_TestOutdoor_ExpectNone() -> None:
   value = EnclosureType.OUTDOOR.value.title()

   normalized = EnclosureType.normalize_viewing_spot_name( value )

   assert normalized is None


def Test_NormalizeViewingSpotName_TestCustomSpotName_ExpectTrimmedValue() -> None:
   name = 'Penguin Beach'
   value = f'  { name }  '

   normalized = EnclosureType.normalize_viewing_spot_name( value )

   assert normalized == name
