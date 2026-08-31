from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.wild_encounter_unschedule_warning_builder import WildEncounterUnscheduleWarningBuilder
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType


RAINFOREST_ENCOUNTER = 'African Rainforest'


def _saved() -> SavedItinerary:
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
            start_time='2:00 PM',
            end_time='2:08 PM' ),
      ],
   )


def _validated( encounter: WildEncounterDiff ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ encounter ],
      events=[],
   )


def Test_NewEncountersOverlappingSavedSchedule_TestOverlap_ExpectEncounter() -> None:
   encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )

   overlapping = WildEncounterUnscheduleWarningBuilder.new_encounters_overlapping_saved_schedule(
      _saved(),
      _validated( encounter ) )

   assert [ item.name for item in overlapping ] == [ RAINFOREST_ENCOUNTER ]


def Test_NewEncountersOverlappingSavedSchedule_TestNoOverlap_ExpectEmpty() -> None:
   encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time='11:00 AM',
      end_time='11:45 AM' )

   overlapping = WildEncounterUnscheduleWarningBuilder.new_encounters_overlapping_saved_schedule(
      _saved(),
      _validated( encounter ) )

   assert overlapping == []


def Test_BuildIssue_TestEncounters_ExpectUnscheduleIssue() -> None:
   encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )

   issue = WildEncounterUnscheduleWarningBuilder.build_issue( [ encounter ] )

   assert issue.code == ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS
   assert [ item.name for item in issue.items ] == [ RAINFOREST_ENCOUNTER ]
