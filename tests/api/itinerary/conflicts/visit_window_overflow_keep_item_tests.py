from __future__ import annotations

from api.itinerary.conflicts.visit_window_overflow_keep_item import VisitWindowOverflowKeepItem
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums.position import Position


def Test_FromWire_TestTalk_ExpectKeepItem() -> None:
   keep_item = VisitWindowOverflowKeepItem.from_wire(
      {
         'name': 'African Lion',
         'item_type': ItinerarySaveIssueItemType.GUARDIANS_TALK.value,
         'start_time': '10:00 AM',
      } )

   assert keep_item.name == 'African Lion'
   assert keep_item.item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK
   assert keep_item.start_time == '10:00 AM'


def Test_FromWire_TestAttractionWithoutStart_ExpectKeepItem() -> None:
   keep_item = VisitWindowOverflowKeepItem.from_wire(
      {
         'name': 'Splash Island',
         'item_type': ItinerarySaveIssueItemType.ATTRACTION.value,
      } )

   assert keep_item.name == 'Splash Island'
   assert keep_item.item_type == ItinerarySaveIssueItemType.ATTRACTION
   assert keep_item.start_time is None


def Test_FromWires_TestItems_ExpectParsedItems() -> None:
   keep_items = VisitWindowOverflowKeepItem.from_wires(
      [
         {
            'name': 'African Lion',
            'item_type': ItinerarySaveIssueItemType.GUARDIANS_TALK.value,
            'start_time': '10:00 AM',
         },
         {
            'name': 'Splash Island',
            'item_type': ItinerarySaveIssueItemType.ATTRACTION.value,
         },
      ] )

   assert len( keep_items ) == 2
   assert keep_items[ Position.FIRST ].name == 'African Lion'
   assert keep_items[ Position.SECOND ].name == 'Splash Island'


def Test_FromWires_TestNone_ExpectEmpty() -> None:
   keep_items = VisitWindowOverflowKeepItem.from_wires( None )

   assert keep_items == []
