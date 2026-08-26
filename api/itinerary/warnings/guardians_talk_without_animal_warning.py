from __future__ import annotations

from ...animals.search.species_exhibit_key import SpeciesExhibitKey
from ...animals.search.species_exhibit_key_builder import SpeciesExhibitKeyBuilder
from ..data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ...guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
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
   animal_keys = SpeciesExhibitKeyBuilder.from_animals( validated_itinerary.animals )
   missing_talks: list[ GuardiansTalkDiff ] = []

   for talk in validated_itinerary.guardians_talks:
      if talk.is_deleted:
         continue

      if talk_matches_species_exhibit_pairs(
            animal_keys,
            linked_animals=GuardiansTalkAnimalProvider.fetch_linked_animals(
               conn,
               talk.name ) ):
         continue

      missing_talks.append( talk )

   return missing_talks


def newly_added_guardians_talks_without_matching_animal(
      validated_itinerary: ValidatedItinerary,
      conn: Connection,
      *,
      saved_itinerary: SavedItinerary | None ) -> list[ GuardiansTalkDiff ]:
   missing_talks = guardians_talks_without_matching_animal(
      validated_itinerary,
      conn )

   if saved_itinerary is None:
      return missing_talks

   saved_names = {
      row.name_key()
      for row in saved_itinerary.guardians_talk_rows
      if not row.is_deleted
   }

   return [
      talk
      for talk in missing_talks
      if ItineraryNameKeyBuilder.build( talk.name ) not in saved_names
   ]


def guardians_talk_without_animal_warning_is_required(
      validated_itinerary: ValidatedItinerary,
      conn: Connection,
      *,
      confirming_guardians_talk_without_animal: bool,
      saved_itinerary: SavedItinerary | None = None ) -> bool:
   if confirming_guardians_talk_without_animal:
      return False

   return bool(
      newly_added_guardians_talks_without_matching_animal(
         validated_itinerary,
         conn,
         saved_itinerary=saved_itinerary ) )


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
      linked_animals=GuardiansTalkAnimalProvider.fetch_linked_animals(
         conn,
         talk.name ) )


def build_guardians_talk_without_animal_issue_from_talks(
      talks: list[ GuardiansTalkDiff ],
      ) -> ItineraryResultReason:
   issue_items = [
      ItinerarySaveIssueItem(
         name=talk.name,
         start_time=talk.start_time,
         end_time=talk.end_time,
         item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
         location=ValueConversion.as_trimmed_string( getattr( talk, 'location', None ) ),
      )
      for talk in talks
   ]

   return ItineraryResultReason(
      code=ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items=issue_items )
