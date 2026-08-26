from __future__ import annotations

from ..data_access.itinerary_event_record import ItineraryEventRecord
from ..domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.itinerary_event import ItineraryEvent
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.enums import ItineraryEventType
from ...types import ScheduleTimeKey


class ItineraryVisitWindowContentBuilder():
   @classmethod
   def filter_guardians_talks(
         cls,
         guardians_talks: list[ GuardiansTalkDiff ],
         *,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey ) -> list[ GuardiansTalkDiff ]:
      return [
         talk
         for talk in guardians_talks
         if not ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
               talk.start_time,
               talk.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time )
      ]


   @classmethod
   def filter_wild_encounters(
         cls,
         wild_encounters: list[ WildEncounterDiff ],
         *,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey ) -> list[ WildEncounterDiff ]:
      return [
         encounter
         for encounter in wild_encounters
         if not ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
               encounter.start_time,
               encounter.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time )
      ]


   @classmethod
   def events_from_saved_rows(
         cls,
         event_rows: list[ ItineraryEventRecord ],
         *,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey ) -> list[ ItineraryEvent ]:
      events: list[ ItineraryEvent ] = []

      for event in event_rows:
         if event.event_type in (
               ItineraryEventType.ARRIVAL,
               ItineraryEventType.DEPARTURE ):
            continue

         if ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
               event.start_time,
               event.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ):
            continue

         events.append(
            ItineraryEvent(
               event_type=event.event_type,
               start_time=event.start_time,
               end_time=event.end_time,
            )
         )

      return events
