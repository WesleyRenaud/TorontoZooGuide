from __future__ import annotations

from api.itinerary.conflicts.visit_window_overflow_item_matcher import VisitWindowOverflowItemMatcher
from api.itinerary.conflicts.visit_window_overflow_keep_item import VisitWindowOverflowKeepItem
from api.itinerary.results.itinerary_save_issue_item import ItinerarySaveIssueItem
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums import ItineraryVisitWindowOverflowEnd


TALK_NAME = 'African Lion'
ATTRACTION_NAME = 'Splash Island'


def _talk_item() -> ItinerarySaveIssueItem:
   return ItinerarySaveIssueItem(
      name=TALK_NAME,
      start_time='10:00 AM',
      end_time='10:30 AM',
      item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
      overflow_end=ItineraryVisitWindowOverflowEnd.ARRIVAL )


def _attraction_item() -> ItinerarySaveIssueItem:
   return ItinerarySaveIssueItem(
      name=ATTRACTION_NAME,
      start_time='12:30 PM',
      end_time='2:00 PM',
      item_type=ItinerarySaveIssueItemType.ATTRACTION,
      overflow_end=ItineraryVisitWindowOverflowEnd.DEPARTURE )


def Test_Partition_TestKeepTalkDropAttraction_ExpectSplit() -> None:
   talk_item = _talk_item()
   attraction_item = _attraction_item()
   kept_items = [
      VisitWindowOverflowKeepItem(
         name=TALK_NAME,
         item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
         start_time='10:00 AM' ),
   ]

   kept, dropped = VisitWindowOverflowItemMatcher.partition(
      [ talk_item, attraction_item ],
      kept_items )

   assert kept == [ talk_item ]
   assert dropped == [ attraction_item ]


def Test_Partition_TestEmptyKeepList_ExpectDropAll() -> None:
   overflow_items = [ _talk_item(), _attraction_item() ]

   kept, dropped = VisitWindowOverflowItemMatcher.partition(
      overflow_items,
      [] )

   assert kept == []
   assert dropped == overflow_items


def Test_Partition_TestKeepBoth_ExpectNoDrops() -> None:
   talk_item = _talk_item()
   attraction_item = _attraction_item()
   kept_items = [
      VisitWindowOverflowKeepItem(
         name=TALK_NAME,
         item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
         start_time='10:00 AM' ),
      VisitWindowOverflowKeepItem(
         name=ATTRACTION_NAME,
         item_type=ItinerarySaveIssueItemType.ATTRACTION ),
   ]

   kept, dropped = VisitWindowOverflowItemMatcher.partition(
      [ talk_item, attraction_item ],
      kept_items )

   assert kept == [ talk_item, attraction_item ]
   assert dropped == []


def Test_IsKept_TestItemTypeMismatch_ExpectFalse() -> None:
   is_kept = VisitWindowOverflowItemMatcher.is_kept(
      _talk_item(),
      [
         VisitWindowOverflowKeepItem(
            name=TALK_NAME,
            item_type=ItinerarySaveIssueItemType.ATTRACTION,
            start_time='10:00 AM' ),
      ] )

   assert is_kept is False


def Test_IsKept_TestStartTimeMismatch_ExpectFalse() -> None:
   is_kept = VisitWindowOverflowItemMatcher.is_kept(
      _talk_item(),
      [
         VisitWindowOverflowKeepItem(
            name=TALK_NAME,
            item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
            start_time='11:00 AM' ),
      ] )

   assert is_kept is False
