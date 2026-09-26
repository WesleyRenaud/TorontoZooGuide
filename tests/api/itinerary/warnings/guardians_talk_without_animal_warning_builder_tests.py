from __future__ import annotations

import pytest

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.warnings.guardians_talk_without_animal_warning_builder import GuardiansTalkWithoutAnimalWarningBuilder
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType, Position


LION_TALK = 'African Lion'
ZEBRA_TALK = "Grevy's Zebra"

LION_LINK = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}

LION_SPECIES_EXHIBIT = SpeciesExhibitKey.from_values(
   LION_LINK[ 'species' ],
   LION_LINK[ 'exhibit' ] )


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
   deleted = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=True,
      location='Africa Savanna' )
   active = GuardiansTalkDiff(
      name=LION_TALK,
      is_deleted=False,
      location='Africa Savanna' )
   validated = _validated_itinerary( guardians_talks=[ deleted, active ] )

   missing = GuardiansTalkWithoutAnimalWarningBuilder.talks_without_matching_animal(
      validated,
      None )

   assert [ talk.name for talk in missing ] == [ active.name ]


def Test_IsRequiredForTalk_TestDeletedTalk_ExpectFalse(
      stub_guardians_talk_animal_links: None ) -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=True,
      location='Africa Savanna' )
   confirming_guardians_talk_without_animal = False

   required = GuardiansTalkWithoutAnimalWarningBuilder.is_required_for_talk(
      talk,
      [],
      None,
      confirming_guardians_talk_without_animal=confirming_guardians_talk_without_animal )

   assert required is False


def Test_NewlyAddedWithoutMatchingAnimal_TestSavedTalk_ExpectEmpty(
      stub_guardians_talk_animal_links: None ) -> None:
   talk = GuardiansTalkDiff(
      name=LION_TALK,
      is_deleted=False,
      location='Africa Savanna' )
   start_time = '10:00 AM'
   duration_minutes = 30
   validated = _validated_itinerary( guardians_talks=[ talk ] )
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=talk.name,
            start_time=start_time,
            end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
            is_deleted=False ),
      ] )

   missing = GuardiansTalkWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
      validated,
      None,
      saved_itinerary=saved_itinerary )

   assert missing == []


def Test_IsRequired_TestConfirmingFlag_ExpectFalse(
      stub_guardians_talk_animal_links: None ) -> None:
   talk = GuardiansTalkDiff(
      name=LION_TALK,
      is_deleted=False,
      location='Africa Savanna' )
   validated = _validated_itinerary( guardians_talks=[ talk ] )
   confirming_guardians_talk_without_animal = True

   required = GuardiansTalkWithoutAnimalWarningBuilder.is_required(
      validated,
      None,
      confirming_guardians_talk_without_animal=confirming_guardians_talk_without_animal )

   assert required is False


def Test_BuildIssueFromTalks_TestTalkWithoutAnimal_ExpectWithoutAnimalIssue() -> None:
   start_time = '12:00 PM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa Savanna' )
   talks = [ talk ]

   issue = GuardiansTalkWithoutAnimalWarningBuilder.build_issue_from_talks( talks )

   assert issue.code == ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL
   assert issue.items[ Position.FIRST ].name == talk.name
   assert issue.items[ Position.FIRST ].location == talk.location


def Test_TalksWithoutMatchingAnimal_TestLinkedAnimalMatch_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkAnimalProvider,
      'fetch_linked_animals',
      lambda conn, talk_name: [ LION_SPECIES_EXHIBIT ] if talk_name == LION_TALK else [] )
   animal = AnimalDiff(
      species=LION_SPECIES_EXHIBIT.species,
      exhibit=LION_SPECIES_EXHIBIT.exhibit,
      old_likelihood=None,
      new_likelihood=100 )
   talk = GuardiansTalkDiff(
      name=LION_TALK,
      is_deleted=False,
      location='Africa Savanna' )
   validated = _validated_itinerary(
      animals=[ animal ],
      guardians_talks=[ talk ] )

   missing = GuardiansTalkWithoutAnimalWarningBuilder.talks_without_matching_animal(
      validated,
      None )

   assert missing == []


def Test_NewlyAddedWithoutMatchingAnimal_TestNoSavedItinerary_ExpectMissingTalks(
      stub_guardians_talk_animal_links: None ) -> None:
   talk = GuardiansTalkDiff(
      name=LION_TALK,
      is_deleted=False,
      location='Africa Savanna' )
   validated = _validated_itinerary( guardians_talks=[ talk ] )

   missing = GuardiansTalkWithoutAnimalWarningBuilder.newly_added_without_matching_animal(
      validated,
      None,
      saved_itinerary=None )

   assert [ item.name for item in missing ] == [ talk.name ]


def Test_IsRequired_TestMissingAnimalWithoutConfirmation_ExpectTrue(
      stub_guardians_talk_animal_links: None ) -> None:
   talk = GuardiansTalkDiff(
      name=LION_TALK,
      is_deleted=False,
      location='Africa Savanna' )
   validated = _validated_itinerary( guardians_talks=[ talk ] )
   confirming_guardians_talk_without_animal = False

   required = GuardiansTalkWithoutAnimalWarningBuilder.is_required(
      validated,
      None,
      confirming_guardians_talk_without_animal=confirming_guardians_talk_without_animal,
      saved_itinerary=None )

   assert required is True


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
   confirming_guardians_talk_without_animal = False

   required = GuardiansTalkWithoutAnimalWarningBuilder.is_required_for_talk(
      talk,
      [],
      None,
      confirming_guardians_talk_without_animal=confirming_guardians_talk_without_animal )

   assert required is True
