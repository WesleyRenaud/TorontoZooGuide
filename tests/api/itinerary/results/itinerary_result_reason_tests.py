from __future__ import annotations

from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_issue_item import ItinerarySaveIssueItem
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType


def Test_ToDict_TestReasonWithoutItems_ExpectCodeOnly() -> None:
   reason = ItineraryResultReason(
      code=ItineraryErrorType.ITEM_NOT_ON_ITINERARY )

   assert reason.to_dict() == {
      'code': 'itemNotOnItinerary',
      'items': [],
   }


def Test_ToDict_TestReasonWithItems_ExpectSerializedItems() -> None:
   reason = ItineraryResultReason(
      code=ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items=[
         ItinerarySaveIssueItem(
            name='African Lion',
            start_time='2:00 PM',
            end_time='2:30 PM',
            item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
            location='Africa Savanna',
         ),
      ],
   )

   assert reason.to_dict() == {
      'code': 'guardiansTalkWithoutAnimal',
      'items': [
         {
            'name': 'African Lion',
            'start_time': '2:00 PM',
            'end_time': '2:30 PM',
            'item_type': ItinerarySaveIssueItemType.GUARDIANS_TALK,
            'meeting_spot': '',
            'location': 'Africa Savanna',
            'link': '',
         },
      ],
   }
