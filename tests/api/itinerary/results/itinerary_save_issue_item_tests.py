from __future__ import annotations

from api.itinerary.results.itinerary_save_issue_item import ItinerarySaveIssueItem
from api.models.attraction_diff import AttractionDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums import ItineraryVisitWindowOverflowEnd


def Test_FromGuardiansTalkDiff_TestTalk_ExpectIssueItemDict() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:30 PM',
      location='Africa Savanna' )

   issue_item = ItinerarySaveIssueItem.from_guardians_talk_diff( talk )
   result = issue_item.to_dict()

   assert result[ 'name' ] == talk.name
   assert result[ 'start_time' ] == talk.start_time
   assert result[ 'end_time' ] == talk.end_time
   assert result[ 'item_type' ] == ItinerarySaveIssueItemType.GUARDIANS_TALK
   assert result[ 'meeting_spot' ] == ''
   assert result[ 'location' ] == talk.location
   assert result[ 'link' ] == ''
   assert result[ 'overflow_end' ] is None


def Test_FromAttractionDiff_TestAttraction_ExpectIssueItemDict() -> None:
   attraction = AttractionDiff(
      name='Splash Island',
      old_likelihood=None,
      new_likelihood=100,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   overflow_end = ItineraryVisitWindowOverflowEnd.DEPARTURE

   issue_item = ItinerarySaveIssueItem.from_attraction_diff(
      attraction,
      overflow_end=overflow_end )
   result = issue_item.to_dict()

   assert result[ 'name' ] == attraction.name
   assert result[ 'start_time' ] == attraction.start_time
   assert result[ 'end_time' ] == attraction.end_time
   assert result[ 'item_type' ] == ItinerarySaveIssueItemType.ATTRACTION
   assert result[ 'overflow_end' ] == overflow_end.value


def Test_FromWildEncounterDiff_TestEncounter_ExpectIssueItemDict() -> None:
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM',
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      link='https://www.torontozoo.com/tickets/weafricarainforest' )

   issue_item = ItinerarySaveIssueItem.from_wild_encounter_diff( encounter )
   result = issue_item.to_dict()

   assert result[ 'name' ] == encounter.name
   assert result[ 'start_time' ] == encounter.start_time
   assert result[ 'end_time' ] == encounter.end_time
   assert result[ 'item_type' ] == ItinerarySaveIssueItemType.WILD_ENCOUNTER
   assert result[ 'meeting_spot' ] == encounter.meeting_spot
   assert result[ 'location' ] == ''
   assert result[ 'link' ] == encounter.link
   assert result[ 'overflow_end' ] is None
