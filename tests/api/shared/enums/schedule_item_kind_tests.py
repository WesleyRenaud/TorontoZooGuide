from __future__ import annotations

from api.shared.enums import ScheduleItemKind
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_Members_TestSharedJson_ExpectKindsAndItemTypes() -> None:
   members = SharedEnumValues.load_object_members( 'scheduleItemKind.json' )

   kinds = {
      name: member.value
      for name, member in ScheduleItemKind.__members__.items()
   }
   item_types = {
      name: member.item_type
      for name, member in ScheduleItemKind.__members__.items()
      if member.item_type is not None
   }

   assert kinds == { name: definition[ 'kind' ] for name, definition in members.items() }
   assert item_types == {
      name: definition[ 'itemType' ]
      for name, definition in members.items()
      if 'itemType' in definition
   }


def Test_Normalize_TestEntrance_ExpectEntranceKind() -> None:
   value = ScheduleItemKind.ENTRANCE.value

   kind = ScheduleItemKind.normalize( value )

   assert kind == ScheduleItemKind.ENTRANCE


def Test_Normalize_TestNone_ExpectNone() -> None:
   value = None

   kind = ScheduleItemKind.normalize( value )

   assert kind is None


def Test_Normalize_TestUnknown_ExpectNone() -> None:
   value = 'picnic'

   kind = ScheduleItemKind.normalize( value )

   assert kind is None


def Test_FromItemType_TestAnimal_ExpectAnimalKind() -> None:
   item_type = ScheduleItemKind.ANIMAL.item_type

   kind = ScheduleItemKind.from_item_type( item_type )

   assert kind == ScheduleItemKind.ANIMAL


def Test_FromItemType_TestGuardiansTalk_ExpectGuardiansTalkKind() -> None:
   item_type = ScheduleItemKind.GUARDIANS_TALK.item_type

   kind = ScheduleItemKind.from_item_type( item_type )

   assert kind == ScheduleItemKind.GUARDIANS_TALK


def Test_FromItemType_TestUnknown_ExpectNone() -> None:
   value = 'picnic'

   kind = ScheduleItemKind.from_item_type( value )

   assert kind is None


def Test_FromItemType_TestNone_ExpectNone() -> None:
   value = None

   kind = ScheduleItemKind.from_item_type( value )

   assert kind is None


def Test_ItemType_TestAnimal_ExpectMappedItemType() -> None:
   members = SharedEnumValues.load_object_members( 'scheduleItemKind.json' )

   item_type = ScheduleItemKind.ANIMAL.item_type

   assert item_type == members[ 'ANIMAL' ][ 'itemType' ]


def Test_ItemType_TestEntrance_ExpectNone() -> None:
   item_type = ScheduleItemKind.ENTRANCE.item_type

   assert item_type is None
