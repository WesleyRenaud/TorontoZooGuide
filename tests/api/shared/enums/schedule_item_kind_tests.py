from __future__ import annotations

from api.shared.enums import ScheduleItemKind
from api.shared.enums.shared_enum_values import SharedEnumValues

def Test_Members_TestSharedJson_ExpectKindsAndItemTypes() -> None:
   members = SharedEnumValues.load_object_members( 'scheduleItemKind.json' )

   assert {
      name: member.value
      for name, member in ScheduleItemKind.__members__.items()
   } == { name: definition[ 'kind' ] for name, definition in members.items() }
   assert {
      name: member.item_type
      for name, member in ScheduleItemKind.__members__.items()
      if member.item_type is not None
   } == {
      name: definition[ 'itemType' ]
      for name, definition in members.items()
      if 'itemType' in definition
   }

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
