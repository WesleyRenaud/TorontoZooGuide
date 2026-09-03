from __future__ import annotations

from api.shared.enums import ScheduleItemKind

def Test_Normalize_TestEntrance_ExpectEntranceKind() -> None:
   assert ScheduleItemKind.normalize( 'entrance' ) == ScheduleItemKind.ENTRANCE

def Test_Normalize_TestNoneOrUnknown_ExpectNone() -> None:
   assert ScheduleItemKind.normalize( None ) is None
   assert ScheduleItemKind.normalize( 'picnic' ) is None

def Test_FromItemType_TestKnownTypes_ExpectMatchingKind() -> None:
   assert ScheduleItemKind.from_item_type( 'animals' ) == ScheduleItemKind.ANIMAL
   assert ScheduleItemKind.from_item_type( 'guardians_talks' ) == ScheduleItemKind.GUARDIANS_TALK

def Test_FromItemType_TestUnknown_ExpectNone() -> None:
   assert ScheduleItemKind.from_item_type( 'picnic' ) is None

def Test_ItemType_TestMappedKinds_ExpectItemTypeStrings() -> None:
   assert ScheduleItemKind.ANIMAL.item_type == 'animals'
   assert ScheduleItemKind.ENTRANCE.item_type is None

def Test_FromItemType_TestNone_ExpectNone() -> None:
   assert ScheduleItemKind.from_item_type( None ) is None
