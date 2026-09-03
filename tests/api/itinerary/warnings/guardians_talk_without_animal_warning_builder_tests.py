from __future__ import annotations

import pytest

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from api.guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.guardians_talk_without_animal_warning_builder import GuardiansTalkWithoutAnimalWarningBuilder
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.enums import ItineraryErrorType


LION_TALK = 'African Lion'
ZEBRA_TALK = "Grevy's Zebra"

LION_LINK = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}

LION_SPECIES_EXHIBIT = SpeciesExhibitKey.from_values( 'African Lion', 'Africa Savanna' )


def _validated_itinerary(
      *,
      animals: list[ AnimalDiff ] | None = None,
      guardians_talks: list[ GuardiansTalkDiff ] ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=animals or [],
      attractions=[],
      guardians_talks=guardians_talks,
      wild_encounters=[],
      events=[] )


@pytest.fixture
def stub_guardians_talk_animal_links( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkAnimalProvider,
      'fetch_linked_animals',
      lambda conn, talk_name: [ LION_LINK ] if talk_name == LION_TALK else [] )


def Test_TalksWithoutMatchingAnimal_TestDeletedTalk_ExpectOnlyActiveMissingTalk(
      stub_guardians_talk_animal_links: None ) -> None:
   missing = GuardiansTalkWithoutAnimalWarningBuilder.talks_without_matching_animal(
      _validated_itinerary(
         guardians_talks=[
            GuardiansTalkDiff(
               name=ZEBRA_TALK,
               is_deleted=True,
               location='Africa Savanna' ),
            GuardiansTalkDiff(
               name=LION_TALK,
               is_deleted=False,
               location='Africa Savanna' ),
         ] ),
      None )

   assert [ talk.name for talk in missing ] == [ LION_TALK ]


def Test_IsRequiredForTalk_TestDeletedTalk_ExpectFalse(
      stub_guardians_talk_animal_links: None ) -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=True,
      location='Africa Savanna' )

   assert not GuardiansTalkWithoutAnimalWarningBuilder.is_required_for_talk(
      talk,
      [],
      None,
      confirming_guardians_talk_without_animal=False )


def Test_NewlyAddedWithoutMatchingAnimal_TestSavedTalk_ExpectEmpty(
      stub_guardians_talk_animal_links: None ) -> None:
   missing = GuardiansTalkWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
      _validated_itinerary(
         guardians_talks=[
            GuardiansTalkDiff(
               name=LION_TALK,
               is_deleted=False,
               location='Africa Savanna' ),
         ] ),
      None,
      saved_itinerary=SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
         guardians_talk_rows=[
            ItineraryGuardiansTalkRecord(
               talk_name=LION_TALK,
               start_time='10:00 AM',
               end_time='10:30 AM',
               is_deleted=False ),
         ] ) )

   assert missing == []


def Test_IsRequired_TestConfirmingFlag_ExpectFalse(
      stub_guardians_talk_animal_links: None ) -> None:
   assert not GuardiansTalkWithoutAnimalWarningBuilder.is_required(
      _validated_itinerary(
         guardians_talks=[
            GuardiansTalkDiff(
               name=LION_TALK,
               is_deleted=False,
               location='Africa Savanna' ),
         ] ),
      None,
      confirming_guardians_talk_without_animal=True )


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


def Test_TalksWithoutMatchingAnimal_TestLinkedAnimalMatch_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkAnimalProvider,
      'fetch_linked_animals',
      lambda conn, talk_name: [ LION_SPECIES_EXHIBIT ] if talk_name == LION_TALK else [] )

   missing = GuardiansTalkWithoutAnimalWarningBuilder.talks_without_matching_animal(
      _validated_itinerary(
         animals=[
            AnimalDiff(
               species='African Lion',
               exhibit='Africa Savanna',
               old_likelihood=None,
               new_likelihood=100 ),
         ],
         guardians_talks=[
            GuardiansTalkDiff(
               name=LION_TALK,
               is_deleted=False,
               location='Africa Savanna' ),
         ] ),
      None )

   assert missing == []


def Test_NewlyAddedWithoutMatchingAnimal_TestNoSavedItinerary_ExpectMissingTalks(
      stub_guardians_talk_animal_links: None ) -> None:
   missing = GuardiansTalkWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
      _validated_itinerary(
         guardians_talks=[
            GuardiansTalkDiff(
               name=LION_TALK,
               is_deleted=False,
               location='Africa Savanna' ),
         ] ),
      None,
      saved_itinerary=None )

   assert [ talk.name for talk in missing ] == [ LION_TALK ]


def Test_IsRequired_TestMissingAnimalWithoutConfirmation_ExpectTrue(
      stub_guardians_talk_animal_links: None ) -> None:
   assert GuardiansTalkWithoutAnimalWarningBuilder.is_required(
      _validated_itinerary(
         guardians_talks=[
            GuardiansTalkDiff(
               name=LION_TALK,
               is_deleted=False,
               location='Africa Savanna' ),
         ] ),
      None,
      confirming_guardians_talk_without_animal=False,
      saved_itinerary=None ) is True


def Test_IsRequiredForTalk_TestMissingLinkedAnimal_ExpectTrue(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkAnimalProvider,
      'fetch_linked_animals',
      lambda conn, talk_name: [] )
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      location='Africa Savanna' )

   assert GuardiansTalkWithoutAnimalWarningBuilder.is_required_for_talk(
      talk,
      [],
      None,
      confirming_guardians_talk_without_animal=False ) is True
