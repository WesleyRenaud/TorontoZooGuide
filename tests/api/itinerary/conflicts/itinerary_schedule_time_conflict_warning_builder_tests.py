from __future__ import annotations

from api.itinerary.conflicts.itinerary_schedule_time_conflict_warning_builder import ItineraryScheduleTimeConflictWarningBuilder
from api.itinerary.conflicts.schedule_time_conflict_issue_finder import ScheduleTimeConflictIssueFinder
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_issue_item import ItinerarySaveIssueItem
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType
from api.shared.enums.position import Position


def Test_Build_TestOverlappingWithoutOverride_ExpectConflictResult() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='12:15 PM',
      end_time='1:00 PM' )
   itinerary = ItineraryBuilder.empty()
   conflict_issues = ScheduleTimeConflictIssueFinder.find( [ talk ], [ encounter ] )

   result = ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      itinerary,
      overriding_conflicting_guardians_talks=False )

   assert result is not None
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert result.reasons == conflict_issues
   assert result.itinerary is itinerary


def Test_Build_TestOverlappingWithoutOverride_ExpectFullIssueDict() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:30 PM',
      location='Africa Savanna' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM',
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      link='https://www.torontozoo.com/tickets/weafricarainforest' )
   expected_issue = ItineraryResultReason(
      code=ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items=[
         ItinerarySaveIssueItem.from_guardians_talk_diff( talk ),
         ItinerarySaveIssueItem.from_wild_encounter_diff( encounter ),
      ] )

   result = ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      ItineraryBuilder.empty(),
      overriding_conflicting_guardians_talks=False )

   assert result is not None
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert [ issue.to_dict() for issue in result.reasons ] == [
      expected_issue.to_dict(),
   ]
   assert result.reasons[ Position.FIRST ].items[ Position.FIRST ].name == talk.name


def Test_Build_TestOverlappingWithOverride_ExpectNone() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='12:15 PM',
      end_time='1:00 PM' )

   result = ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      ItineraryBuilder.empty(),
      overriding_conflicting_guardians_talks=True )

   assert result is None


def Test_Build_TestNoConflict_ExpectNone() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )

   result = ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      ItineraryBuilder.empty(),
      overriding_conflicting_guardians_talks=False )

   assert result is None
