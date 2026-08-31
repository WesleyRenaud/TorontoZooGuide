from __future__ import annotations

from api.itinerary.conflicts.itinerary_unschedule_confirmation_warning_builder import ItineraryUnscheduleConfirmationWarningBuilder
from api.itinerary.conflicts.itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType


ZEBRA_TALK = GuardiansTalkDiff(
   name="Grevy's Zebra",
   is_deleted=False,
   start_time='12:00 PM',
   end_time='12:30 PM',
   location='Africa Savanna',
)
RAINFOREST = WildEncounterDiff(
   name='African Rainforest',
   is_deleted=False,
   start_time='12:00 PM',
   end_time='12:45 PM',
)


def Test_Build_TestPendingTalkAndEncounter_ExpectSaveResultWithReasons() -> None:
   result = ItineraryUnscheduleConfirmationWarningBuilder.build(
      ItineraryUnscheduleRequirements( talks=[ ZEBRA_TALK ], encounters=[ RAINFOREST ] ),
      ItineraryBuilder.empty(),
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False )

   assert result is not None
   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert [ reason.code for reason in result.reasons ] == [
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
   ]


def Test_Build_TestBothConfirmed_ExpectNone() -> None:
   result = ItineraryUnscheduleConfirmationWarningBuilder.build(
      ItineraryUnscheduleRequirements( talks=[ ZEBRA_TALK ], encounters=[ RAINFOREST ] ),
      ItineraryBuilder.empty(),
      confirming_guardians_talk_unschedule=True,
      confirming_wild_encounter_unschedule=True )

   assert result is None


def Test_Build_TestEmptyRequirements_ExpectNone() -> None:
   result = ItineraryUnscheduleConfirmationWarningBuilder.build(
      ItineraryUnscheduleRequirements( talks=[], encounters=[] ),
      ItineraryBuilder.empty(),
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False )

   assert result is None
