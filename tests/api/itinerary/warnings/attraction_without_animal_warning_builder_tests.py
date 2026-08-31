from __future__ import annotations

from api.itinerary.warnings.attraction_without_animal_warning_builder import AttractionWithoutAnimalWarningBuilder
from api.models.attraction_diff import AttractionDiff
from api.shared.enums import ItineraryErrorType


KANGAROO_WALK_THRU = 'Kangaroo Walk-Thru'


def Test_BuildIssueFromAttractions_TestLinkedAttraction_ExpectWithoutAnimalIssue() -> None:
   issue = AttractionWithoutAnimalWarningBuilder.build_issue_from_attractions(
      [
         AttractionDiff(
            name=KANGAROO_WALK_THRU,
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   assert issue.code == ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL
   assert [ item.name for item in issue.items ] == [ KANGAROO_WALK_THRU ]
