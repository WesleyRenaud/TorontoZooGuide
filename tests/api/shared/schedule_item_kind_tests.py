from __future__ import annotations

from api.shared.enums import ScheduleItemKind


def Test_Normalize_TestEntrance_ExpectEntranceKind() -> None:
   assert ScheduleItemKind.normalize( 'entrance' ) == ScheduleItemKind.ENTRANCE


def Test_FromItemType_TestModuleTypes_ExpectMatchingKinds() -> None:
   assert ScheduleItemKind.from_item_type( 'animals' ) == ScheduleItemKind.ANIMAL
   assert ScheduleItemKind.from_item_type( 'attractions' ) == ScheduleItemKind.ATTRACTION
   assert ScheduleItemKind.ANIMAL.item_type == 'animals'
   assert ScheduleItemKind.ATTRACTION.item_type == 'attractions'
