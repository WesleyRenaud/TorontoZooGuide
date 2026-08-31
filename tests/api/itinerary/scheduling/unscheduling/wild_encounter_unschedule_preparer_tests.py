from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.unscheduling.wild_encounter_unschedule_preparer import WildEncounterUnschedulePreparer
from api.models.animal_diff import AnimalDiff
from api.models.wild_encounter_diff import WildEncounterDiff


RAINFOREST = 'African Rainforest'
KANGAROO = 'Kangaroo'


def _empty_saved() -> SavedItinerary:
   return SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )


def Test_TimeBlocks_TestTimedEncounter_ExpectTimeBlock() -> None:
   encounter = WildEncounterDiff(
      name=RAINFOREST,
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )

   assert WildEncounterUnschedulePreparer.time_blocks( [ encounter ] ) == [
      TimeBlock( start_seconds=14 * 3600, end_seconds=14 * 3600 + 45 * 60 ),
   ]


def Test_NewlyAddedActive_TestNewTimedEncounter_ExpectEncounter() -> None:
   encounter = WildEncounterDiff(
      name=RAINFOREST,
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )

   assert WildEncounterUnschedulePreparer.newly_added_active(
      _empty_saved(),
      [ encounter ] ) == [ encounter ]


def Test_NewlyAddedActive_TestAlreadySavedOrDeletedOrUntimed_ExpectEmpty() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter=RAINFOREST,
            start_time='2:00 PM',
            end_time='2:45 PM',
            is_deleted=False ),
      ],
   )
   encounters = [
      WildEncounterDiff(
         name=RAINFOREST,
         is_deleted=False,
         start_time='2:00 PM',
         end_time='2:45 PM' ),
      WildEncounterDiff(
         name=KANGAROO,
         is_deleted=True,
         start_time='1:00 PM',
         end_time='1:45 PM' ),
      WildEncounterDiff(
         name='Guardians of White Rhinos',
         is_deleted=False,
         start_time=None,
         end_time=None ),
   ]

   assert WildEncounterUnschedulePreparer.newly_added_active( saved, encounters ) == []


def Test_SavedItineraryHasOverlap_TestOverlappingAnimal_ExpectTrue() -> None:
   saved = SavedItinerary(
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
   encounter = WildEncounterDiff(
      name=RAINFOREST,
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )

   assert WildEncounterUnschedulePreparer.saved_itinerary_has_overlap(
      saved,
      [ encounter ] )


def Test_PrepareValidatedForReschedule_TestClearsListedSchedules() -> None:
   encounter = WildEncounterDiff(
      name=RAINFOREST,
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:08 AM' ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ encounter ],
      events=[],
   )

   prepared = WildEncounterUnschedulePreparer.prepare_validated_for_reschedule(
      validated,
      [ encounter ] )

   assert prepared.animals[ 0 ].start_time is None
   assert prepared.animals[ 0 ].end_time is None
