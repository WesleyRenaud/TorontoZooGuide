from __future__ import annotations

from api.itinerary.warnings.guardians_talk_without_animal_warning_builder import GuardiansTalkWithoutAnimalWarningBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType


ZEBRA_TALK = "Grevy's Zebra"


def Test_BuildIssueFromTalks_TestTalkWithoutAnimal_ExpectWithoutAnimalIssue() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM',
      location='Africa Savanna' )

   issue = GuardiansTalkWithoutAnimalWarningBuilder.build_issue_from_talks( [ talk ] )

   assert issue.code == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert len( issue.items ) == 1
   assert issue.items[ 0 ].name == ZEBRA_TALK
   assert issue.items[ 0 ].location == 'Africa Savanna'
