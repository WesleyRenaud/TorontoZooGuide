from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.guardians_talk_unschedule_warning_builder import GuardiansTalkUnscheduleWarningBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType


ZEBRA_TALK = "Grevy's Zebra"


def _saved(
      *,
      animal_start: str | None = '10:00 AM',
      animal_end: str | None = '10:08 AM' ) -> SavedItinerary:
   return SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time=animal_start,
            end_time=animal_end ),
      ],
   )


def _validated( talk: GuardiansTalkDiff ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[ talk ],
      wild_encounters=[],
      events=[],
   )


def Test_IsRequired_TestConfirming_ExpectFalse() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM',
      location='Africa Savanna' )

   assert not GuardiansTalkUnscheduleWarningBuilder.is_required(
      _saved(),
      _validated( talk ),
      confirming_guardians_talk_unschedule=True )


def Test_IsRequired_TestNewTalkOverlapsSavedAnimal_ExpectTrue() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM',
      location='Africa Savanna' )

   assert GuardiansTalkUnscheduleWarningBuilder.is_required(
      _saved(),
      _validated( talk ),
      confirming_guardians_talk_unschedule=False )


def Test_IsRequired_TestNewTalkWithoutOverlap_ExpectFalse() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:30 PM',
      location='Africa Savanna' )

   assert not GuardiansTalkUnscheduleWarningBuilder.is_required(
      _saved(),
      _validated( talk ),
      confirming_guardians_talk_unschedule=False )


def Test_NewTalksOverlappingSavedSchedule_TestOverlap_ExpectTalk() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM',
      location='Africa Savanna' )

   overlapping = GuardiansTalkUnscheduleWarningBuilder.new_talks_overlapping_saved_schedule(
      _saved(),
      _validated( talk ) )

   assert [ item.name for item in overlapping ] == [ ZEBRA_TALK ]


def Test_BuildIssue_TestTalks_ExpectUnscheduleIssue() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM',
      location='Africa Savanna' )

   issue = GuardiansTalkUnscheduleWarningBuilder.build_issue( [ talk ] )

   assert issue.code == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert [ item.name for item in issue.items ] == [ ZEBRA_TALK ]
