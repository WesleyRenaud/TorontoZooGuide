from __future__ import annotations

from ..data_access.validated_itinerary import ValidatedItinerary
from .itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from ..scheduling.unscheduling.fixed_time_activity_unschedule_preparer import FixedTimeActivityUnschedulePreparer
from ..scheduling.unscheduling.guardians_talk_unschedule_preparer import GuardiansTalkUnschedulePreparer
from ..scheduling.unscheduling.wild_encounter_unschedule_preparer import WildEncounterUnschedulePreparer


class ItineraryUnscheduleChangeApplier():
   @classmethod
   def apply(
         cls,
         validated_itinerary: ValidatedItinerary,
         requirements: ItineraryUnscheduleRequirements ) -> ValidatedItinerary:
      activity_blocks = [
         *GuardiansTalkUnschedulePreparer.time_blocks( requirements.talks ),
         *WildEncounterUnschedulePreparer.time_blocks( requirements.encounters ),
      ]

      if not activity_blocks:
         return validated_itinerary

      return FixedTimeActivityUnschedulePreparer.prepare_validated_for_reschedule(
         validated_itinerary,
         activity_blocks )
