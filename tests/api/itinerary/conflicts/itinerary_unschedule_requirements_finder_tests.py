from __future__ import annotations

from api.itinerary.conflicts.itinerary_unschedule_requirements_finder import ItineraryUnscheduleRequirementsFinder
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff


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
            start_time='12:00 PM',
            end_time='12:08 PM' ),
      ],
   )


def Test_Find_TestOverlappingTalkAndEncounter_ExpectRequirements() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:45 PM' )
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[ talk ],
      wild_encounters=[ encounter ],
      events=[],
   )

   requirements = ItineraryUnscheduleRequirementsFinder.find( _saved(), validated )

   assert [ item.name for item in requirements.talks ] == [ "Grevy's Zebra" ]
   assert [ item.name for item in requirements.encounters ] == [ 'African Rainforest' ]


def Test_Find_TestNoOverlaps_ExpectEmptyRequirements() -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name="Grevy's Zebra",
            is_deleted=False,
            start_time='2:00 PM',
            end_time='2:30 PM' ),
      ],
      wild_encounters=[],
      events=[],
   )

   requirements = ItineraryUnscheduleRequirementsFinder.find( _saved(), validated )

   assert requirements.talks == []
   assert requirements.encounters == []
