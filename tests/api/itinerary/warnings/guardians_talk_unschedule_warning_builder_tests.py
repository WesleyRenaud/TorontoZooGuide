from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.guardians_talk_unschedule_warning_builder import GuardiansTalkUnscheduleWarningBuilder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.calendar_dates import DateValues
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
   start_time = '10:00 AM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa Savanna' )
   confirming_guardians_talk_unschedule = True

   required = GuardiansTalkUnscheduleWarningBuilder.is_required(
      _saved(),
      _validated( talk ),
      confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule )

   assert required is False


def Test_IsRequired_TestNewTalkOverlapsSavedAnimal_ExpectTrue() -> None:
   start_time = '10:00 AM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa Savanna' )
   confirming_guardians_talk_unschedule = False

   required = GuardiansTalkUnscheduleWarningBuilder.is_required(
      _saved(),
      _validated( talk ),
      confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule )

   assert required is True


def Test_IsRequired_TestNewTalkWithoutOverlap_ExpectFalse() -> None:
   start_time = '1:00 PM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa Savanna' )
   confirming_guardians_talk_unschedule = False

   required = GuardiansTalkUnscheduleWarningBuilder.is_required(
      _saved(),
      _validated( talk ),
      confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule )

   assert required is False


def Test_NewTalksOverlappingSavedSchedule_TestOverlap_ExpectTalk() -> None:
   start_time = '10:00 AM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa Savanna' )
   saved = _saved()
   validated = _validated( talk )

   overlapping = GuardiansTalkUnscheduleWarningBuilder.new_talks_overlapping_saved_schedule(
      saved,
      validated )

   assert [ item.name for item in overlapping ] == [ talk.name ]


def Test_BuildIssue_TestTalks_ExpectUnscheduleIssue() -> None:
   start_time = '10:00 AM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa Savanna' )
   talks = [ talk ]

   issue = GuardiansTalkUnscheduleWarningBuilder.build_issue( talks )

   assert issue.code == ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS
   assert [ item.name for item in issue.items ] == [ talk.name ]


def Test_IsRequired_TestNoNewTalks_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )
   validated = ValidatedItinerary(
      animals=[],
      attractions=[],
      transportations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )
   confirming_guardians_talk_unschedule = False

   required = GuardiansTalkUnscheduleWarningBuilder.is_required(
      saved,
      validated,
      confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule )

   assert required is False
