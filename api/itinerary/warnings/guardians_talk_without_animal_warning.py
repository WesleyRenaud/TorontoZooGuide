from __future__ import annotations

from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from ...animals.search.animals_matching_query import species_exhibit_keys
from ..data_access.validated_itinerary import ValidatedItinerary
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType
from ...shared.value_conversion import ValueConversion


def talk_matches_species_exhibit_pairs(
      talk: GuardiansTalkDiff,
      animal_species_exhibit_pairs: list[ tuple[ str, str ] ] | set[ tuple[ str, str ] ],
      ) -> bool:
   location = ValueConversion.as_nullable_string( talk.location )

   if location is None:
      return True

   talk_key = species_exhibit_key_from_values( talk.name, location )
   return talk_key in set( animal_species_exhibit_pairs )


def guardians_talks_without_matching_animal(
      validated_itinerary: ValidatedItinerary ) -> list[ GuardiansTalkDiff ]:
   animal_keys = species_exhibit_keys( validated_itinerary.animals )
   missing_talks: list[ GuardiansTalkDiff ] = []

   for talk in validated_itinerary.guardians_talks:
      if talk.is_deleted:
         continue

      if talk_matches_species_exhibit_pairs( talk, animal_keys ):
         continue

      missing_talks.append( talk )

   return missing_talks


def guardians_talk_without_animal_warning_is_required(
      validated_itinerary: ValidatedItinerary,
      *,
      confirming_guardians_talk_without_animal: bool ) -> bool:
   if confirming_guardians_talk_without_animal:
      return False

   return bool( guardians_talks_without_matching_animal( validated_itinerary ) )


def guardians_talk_without_animal_warning_is_required_for_talk(
      talk: GuardiansTalkDiff,
      species_exhibit_pairs: list[ tuple[ str, str ] ] | set[ tuple[ str, str ] ],
      *,
      confirming_guardians_talk_without_animal: bool ) -> bool:
   if confirming_guardians_talk_without_animal:
      return False

   if talk.is_deleted:
      return False

   return not talk_matches_species_exhibit_pairs(
      talk,
      species_exhibit_pairs )


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
