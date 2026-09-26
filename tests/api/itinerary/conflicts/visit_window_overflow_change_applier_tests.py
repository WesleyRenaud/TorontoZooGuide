from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.conflicts.visit_window_overflow_change_applier import VisitWindowOverflowChangeApplier
from api.itinerary.conflicts.visit_window_overflow_keep_item import VisitWindowOverflowKeepItem
from api.itinerary.conflicts.visit_window_overflow_time_expander import VisitWindowOverflowTimeExpander
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.operations.itinerary_item_remover import ItineraryItemRemover
from api.itinerary.operations.itinerary_save_context import ItinerarySaveContext
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_issue_item import ItinerarySaveIssueItem
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.models.attraction_diff import AttractionDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums import ItineraryVisitWindowOverflowEnd
from api.shared.enums.position import Position


ARRIVAL_TIME = '11:00 AM'
DEPARTURE_TIME = '1:00 PM'
EXPANDED_ARRIVAL_TIME = '9:50 AM'
TALK_NAME = 'African Lion'
ATTRACTION_NAME = 'Splash Island'


def _talk_diff() -> GuardiansTalkDiff:
   return GuardiansTalkDiff(
      name=TALK_NAME,
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM' )


def _attraction_diff() -> AttractionDiff:
   return AttractionDiff(
      name=ATTRACTION_NAME,
      old_likelihood=None,
      new_likelihood=100,
      start_time='12:30 PM',
      end_time='2:00 PM' )


def _talk_issue() -> ItinerarySaveIssueItem:
   return ItinerarySaveIssueItem(
      name=TALK_NAME,
      start_time='10:00 AM',
      end_time='10:30 AM',
      item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
      overflow_end=ItineraryVisitWindowOverflowEnd.ARRIVAL )


def _attraction_issue() -> ItinerarySaveIssueItem:
   return ItinerarySaveIssueItem(
      name=ATTRACTION_NAME,
      start_time='12:30 PM',
      end_time='2:00 PM',
      item_type=ItinerarySaveIssueItemType.ATTRACTION,
      overflow_end=ItineraryVisitWindowOverflowEnd.DEPARTURE )


def _save_context( conn: sqlite3.Connection ) -> ItinerarySaveContext:
   return ItinerarySaveContext(
      conn=conn,
      save_input=ItinerarySaveInput(
         date=date( 2026, 6, 15 ),
         arrival_time=ARRIVAL_TIME,
         departure_time=DEPARTURE_TIME,
         attractions=[ ATTRACTION_NAME ],
         guardians_talks=[],
      ),
      validated_itinerary=ValidatedItinerary(
         arrival_time=ARRIVAL_TIME,
         departure_time=DEPARTURE_TIME,
         animals=[],
         attractions=[ _attraction_diff() ],
         guardians_talks=[ _talk_diff() ],
         wild_encounters=[],
         events=[] ),
      current_itinerary=ItineraryBuilder.empty(),
      old_visit_date=None,
      saved_itinerary=None,
      unschedule_requirements=object(),
      itinerary_controller_kwargs={} )


def Test_Resolve_TestKeepTalkDropAttraction_ExpectPartitionAndExpandedTimes(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      VisitWindowOverflowTimeExpander,
      'expand',
      lambda arrival_time, departure_time, kept_items: (
         EXPANDED_ARRIVAL_TIME,
         departure_time ) )
   talk_issue = _talk_issue()
   attraction_issue = _attraction_issue()

   resolution = VisitWindowOverflowChangeApplier.resolve(
      [ talk_issue, attraction_issue ],
      [
         VisitWindowOverflowKeepItem(
            name=TALK_NAME,
            item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
            start_time='10:00 AM' ),
      ],
      ARRIVAL_TIME,
      DEPARTURE_TIME )

   assert resolution.kept_items == [ talk_issue ]
   assert resolution.dropped_items == [ attraction_issue ]
   assert resolution.arrival_time == EXPANDED_ARRIVAL_TIME
   assert resolution.departure_time == DEPARTURE_TIME


def Test_Resolve_TestDropAll_ExpectUnchangedTimes() -> None:
   talk_issue = _talk_issue()

   resolution = VisitWindowOverflowChangeApplier.resolve(
      [ talk_issue ],
      [],
      ARRIVAL_TIME,
      DEPARTURE_TIME )

   assert resolution.kept_items == []
   assert resolution.dropped_items == [ talk_issue ]
   assert resolution.arrival_time == ARRIVAL_TIME
   assert resolution.departure_time == DEPARTURE_TIME


def Test_ApplyToContext_TestDropAttractionKeepTalk_ExpectFilteredAndExpanded(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   conn = sqlite3.connect( ':memory:' )
   monkeypatch.setattr(
      VisitWindowOverflowTimeExpander,
      'expand',
      lambda arrival_time, departure_time, kept_items: (
         EXPANDED_ARRIVAL_TIME,
         departure_time ) )
   overflow_reasons = [
      ItineraryResultReason(
         code=ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         items=[ _talk_issue(), _attraction_issue() ] ),
   ]

   updated_context = VisitWindowOverflowChangeApplier.apply_to_context(
      _save_context( conn ),
      overflow_reasons,
      [
         VisitWindowOverflowKeepItem(
            name=TALK_NAME,
            item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
            start_time='10:00 AM' ),
      ] )

   conn.close()

   assert updated_context.save_input.arrival_time == EXPANDED_ARRIVAL_TIME
   assert updated_context.validated_itinerary.arrival_time == EXPANDED_ARRIVAL_TIME
   assert updated_context.validated_itinerary.guardians_talks[ Position.FIRST ].name == TALK_NAME
   assert updated_context.validated_itinerary.attractions == []
   assert updated_context.save_input.attractions == []


def Test_DropSavedItems_TestAttraction_ExpectRemoverApplied(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   applied: list[ object ] = []
   conn = sqlite3.connect( ':memory:' )
   monkeypatch.setattr(
      ItineraryItemRemover,
      'apply',
      lambda cur, schedule_item_key: applied.append( schedule_item_key ) )

   VisitWindowOverflowChangeApplier.drop_saved_items(
      conn,
      [ _attraction_issue() ] )

   conn.close()

   assert len( applied ) == 1
   assert applied[ Position.FIRST ].name == ATTRACTION_NAME


def Test_DropSavedItems_TestTalkEncounterAndUnknown_ExpectTypedKeysAndSkip(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   applied: list[ object ] = []
   conn = sqlite3.connect( ':memory:' )
   monkeypatch.setattr(
      ItineraryItemRemover,
      'apply',
      lambda cur, schedule_item_key: applied.append( schedule_item_key ) )
   encounter_issue = ItinerarySaveIssueItem(
      name='African Rainforest',
      start_time='12:30 PM',
      end_time='2:00 PM',
      item_type=ItinerarySaveIssueItemType.WILD_ENCOUNTER,
      overflow_end=ItineraryVisitWindowOverflowEnd.DEPARTURE )
   unknown_issue = ItinerarySaveIssueItem(
      name='African Lion',
      start_time='10:00 AM',
      end_time='10:30 AM',
      item_type=ItinerarySaveIssueItemType.ANIMAL,
      overflow_end=ItineraryVisitWindowOverflowEnd.ARRIVAL )

   VisitWindowOverflowChangeApplier.drop_saved_items(
      conn,
      [ _talk_issue(), encounter_issue, unknown_issue ] )

   conn.close()

   assert applied == [
      GuardiansTalkScheduleItemKey(
         name=TALK_NAME,
         start_time='10:00 AM',
         end_time='10:30 AM' ),
      WildEncounterScheduleItemKey(
         name='African Rainforest',
         start_time='12:30 PM',
         end_time='2:00 PM' ),
   ]


def Test_DropSavedItems_TestEmpty_ExpectNoRemoverCalls(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   applied: list[ object ] = []
   conn = sqlite3.connect( ':memory:' )
   monkeypatch.setattr(
      ItineraryItemRemover,
      'apply',
      lambda cur, schedule_item_key: applied.append( schedule_item_key ) )

   VisitWindowOverflowChangeApplier.drop_saved_items( conn, [] )

   conn.close()

   assert applied == []


def Test_OverflowItems_TestReasons_ExpectFlattenedItems() -> None:
   talk_issue = _talk_issue()
   attraction_issue = _attraction_issue()
   overflow_reasons = [
      ItineraryResultReason(
         code=ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
         items=[ talk_issue, attraction_issue ] ),
   ]

   overflow_items = VisitWindowOverflowChangeApplier.overflow_items(
      overflow_reasons )

   assert overflow_items == [ talk_issue, attraction_issue ]
