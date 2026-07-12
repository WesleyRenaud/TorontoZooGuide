from __future__ import annotations

from ...animals.search.animals_matching_query import species_exhibit_keys
from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ..data_access.validated_itinerary import ValidatedItinerary
from ...guardians.data_access.guardians_talk_animal import fetch_guardians_talk_linked_animals
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType
from ...shared.value_conversion import ValueConversion
from ...types import Connection


def talk_matches_species_exhibit_pairs(
      animal_species_exhibit_keys: list[ SpeciesExhibitKey ],
      *,
      linked_animals: list[ SpeciesExhibitKey ] ) -> bool:
   return any(
      linked_animal in animal_species_exhibit_keys
      for linked_animal in linked_animals
   )


def guardians_talks_without_matching_animal(
      validated_itinerary: ValidatedItinerary,
      conn: Connection ) -> list[ GuardiansTalkDiff ]:
   animal_keys = species_exhibit_keys( validated_itinerary.animals )
   missing_talks: list[ GuardiansTalkDiff ] = []

   for talk in validated_itinerary.guardians_talks:
      if talk.is_deleted:
         continue

      if talk_matches_species_exhibit_pairs(
            animal_keys,
            linked_animals=fetch_guardians_talk_linked_animals(
               conn,
               talk.name ) ):
         continue

      missing_talks.append( talk )

   return missing_talks


def guardians_talk_without_animal_warning_is_required(
      validated_itinerary: ValidatedItinerary,
      conn: Connection,
      *,
      confirming_guardians_talk_without_animal: bool ) -> bool:
   if confirming_guardians_talk_without_animal:
      return False

   return bool(
      guardians_talks_without_matching_animal(
         validated_itinerary,
         conn ) )


def guardians_talk_without_animal_warning_is_required_for_talk(
      talk: GuardiansTalkDiff,
      species_exhibit_pairs: list[ SpeciesExhibitKey ],
      conn: Connection,
      *,
      confirming_guardians_talk_without_animal: bool ) -> bool:
   if confirming_guardians_talk_without_animal:
      return False

   if talk.is_deleted:
      return False

   return not talk_matches_species_exhibit_pairs(
      species_exhibit_pairs,
      linked_animals=fetch_guardians_talk_linked_animals(
         conn,
         talk.name ) )


def build_guardians_talk_without_animal_issue_from_talks(
      talks: list[ GuardiansTalkDiff ],
      ) -> ItineraryResultReason:
   issue_items = tuple(
      ItinerarySaveIssueItem(
         name=talk.name,
         start_time=talk.start_time,
         end_time=talk.end_time,
         item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
         location=ValueConversion.as_trimmed_string( getattr( talk, 'location', None ) ),
      )
      for talk in talks
   )

   return ItineraryResultReason(
      code=ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items=issue_items )
