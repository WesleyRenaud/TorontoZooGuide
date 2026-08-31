from __future__ import annotations

from api.itinerary.results.itinerary_save_issue_item import ItinerarySaveIssueItem
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItinerarySaveIssueItemType


def Test_FromGuardiansTalkDiff_TestTalk_ExpectIssueItemDict() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:30 PM',
      location='Africa Savanna' )

   issue_item = ItinerarySaveIssueItem.from_guardians_talk_diff( talk )

   assert issue_item.to_dict() == {
      'name': 'African Lion',
      'start_time': '2:00 PM',
      'end_time': '2:30 PM',
      'item_type': ItinerarySaveIssueItemType.GUARDIANS_TALK,
      'meeting_spot': '',
      'location': 'Africa Savanna',
      'link': '',
   }


def Test_FromWildEncounterDiff_TestEncounter_ExpectIssueItemDict() -> None:
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM',
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      link='https://www.torontozoo.com/tickets/weafricarainforest' )

   issue_item = ItinerarySaveIssueItem.from_wild_encounter_diff( encounter )

   assert issue_item.to_dict() == {
      'name': 'African Rainforest',
      'start_time': '2:00 PM',
      'end_time': '2:45 PM',
      'item_type': ItinerarySaveIssueItemType.WILD_ENCOUNTER,
      'meeting_spot': 'Wild Encounter - Africa Meeting Spot',
      'location': '',
      'link': 'https://www.torontozoo.com/tickets/weafricarainforest',
   }
