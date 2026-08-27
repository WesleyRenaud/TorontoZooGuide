from __future__ import annotations

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from .itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from ..warnings.guardians_talk_unschedule_warning_builder import GuardiansTalkUnscheduleWarningBuilder
from ..warnings.wild_encounter_unschedule_warning_builder import WildEncounterUnscheduleWarningBuilder


class ItineraryUnscheduleRequirementsFinder():
   @classmethod
   def find(
         cls,
         saved_itinerary: SavedItinerary,
         validated_itinerary: ValidatedItinerary ) -> ItineraryUnscheduleRequirements:
      return ItineraryUnscheduleRequirements(
         talks=GuardiansTalkUnscheduleWarningBuilder.new_talks_overlapping_saved_schedule(
            saved_itinerary,
            validated_itinerary ),
         encounters=WildEncounterUnscheduleWarningBuilder.new_encounters_overlapping_saved_schedule(
            saved_itinerary,
            validated_itinerary ),
      )
