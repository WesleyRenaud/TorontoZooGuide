from __future__ import annotations

from api.itinerary.conflicts.itinerary_schedule_time_conflict_warning_builder import ItineraryScheduleTimeConflictWarningBuilder
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType


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

   result = ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      ItineraryBuilder.empty(),
      overriding_conflicting_guardians_talks=False )

   assert result is not None
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.reasons ) == 1


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

   result = ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      ItineraryBuilder.empty(),
      overriding_conflicting_guardians_talks=False )

   assert result is not None
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert [ issue.to_dict() for issue in result.reasons ] == [
      {
         'code': 'wildEncounterTimeConflict',
         'items': [
            {
               'name': 'African Lion',
               'start_time': '2:00 PM',
               'end_time': '2:30 PM',
               'item_type': 'guardiansTalk',
               'meeting_spot': '',
               'location': 'Africa Savanna',
               'link': '',
            },
            {
               'name': 'African Rainforest',
               'start_time': '2:00 PM',
               'end_time': '2:45 PM',
               'item_type': 'wildEncounter',
               'meeting_spot': 'Wild Encounter - Africa Meeting Spot',
               'location': '',
               'link': 'https://www.torontozoo.com/tickets/weafricarainforest',
            },
         ],
      },
   ]


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

   assert ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      ItineraryBuilder.empty(),
      overriding_conflicting_guardians_talks=True ) is None


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

   assert ItineraryScheduleTimeConflictWarningBuilder.build(
      [ talk ],
      [ encounter ],
      ItineraryBuilder.empty(),
      overriding_conflicting_guardians_talks=False ) is None
