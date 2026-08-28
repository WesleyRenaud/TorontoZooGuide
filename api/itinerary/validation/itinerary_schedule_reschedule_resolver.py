from __future__ import annotations

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ..domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from ...shared.enums import ItineraryEventType
from ...types import Types
from ..warnings.guardians_talk_unschedule_warning_builder import GuardiansTalkUnscheduleWarningBuilder
from ..warnings.wild_encounter_unschedule_warning_builder import WildEncounterUnscheduleWarningBuilder


class ItineraryScheduleRescheduleResolver():
   @classmethod
   def needs_reschedule(
         cls,
         saved_itinerary: SavedItinerary,
         validated_itinerary: ValidatedItinerary,
         *,
         requested_departure_time: Types.ScheduleTimeKey ) -> bool:
      if GuardiansTalkUnscheduleWarningBuilder.new_talks_overlapping_saved_schedule(
            saved_itinerary,
            validated_itinerary ):
         return True

      if WildEncounterUnscheduleWarningBuilder.new_encounters_overlapping_saved_schedule(
            saved_itinerary,
            validated_itinerary ):
         return True

      if not cls._visit_window_changed(
            saved_itinerary,
            arrival_time=validated_itinerary.arrival_time,
            departure_time=requested_departure_time ):
         return False

      return cls._visit_window_cuts_off_saved_schedules(
         saved_itinerary,
         arrival_time=validated_itinerary.arrival_time,
         departure_time=requested_departure_time )


   @classmethod
   def _visit_window_changed(
         cls,
         saved_itinerary: SavedItinerary,
         *,
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey ) -> bool:
      return (
         saved_itinerary.arrival_time != arrival_time
         or saved_itinerary.departure_time != departure_time
      )


   @classmethod
   def _visit_window_cuts_off_saved_schedules(
         cls,
         saved_itinerary: SavedItinerary,
         *,
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey ) -> bool:
      for animal in saved_itinerary.animal_rows:
         if ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
               animal.start_time,
               animal.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            return True

      for attraction in saved_itinerary.attraction_rows:
         if ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
               attraction.start_time,
               attraction.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            return True

      for transportation in saved_itinerary.transportation_rows:
         if ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
               transportation.start_time,
               transportation.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            return True

      for event in saved_itinerary.event_rows:
         if event.event_type in (
               ItineraryEventType.ARRIVAL,
               ItineraryEventType.DEPARTURE ):
            continue

         if ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
               event.start_time,
               event.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            return True

      return False
