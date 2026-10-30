from __future__ import annotations

from ...itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from ...itinerary.scheduling.core.scheduled_occurrence_builder import ScheduledOccurrenceBuilder
from ...models import GuardiansTalk
from ...models import GuardiansTalkDiff
from ..scheduling.guardians_talk_day_schedule_finder import GuardiansTalkDayScheduleFinder
from ...types import Types


class GuardiansTalkItineraryValidator():
   @classmethod
   def build_diff_for_visit_day(
         cls,
         name: str,
         talk: GuardiansTalk | None,
         *,
         start_time_override: Types.ScheduleTimeKey = None,
         end_time_override: Types.ScheduleTimeKey = None,
         enclosure_name: str ) -> GuardiansTalkDiff:
      return ScheduledOccurrenceBuilder.guardians_talk(
         name,
         talk,
         start_time_override=start_time_override,
         end_time_override=end_time_override,
         enclosure_name=enclosure_name )


   @classmethod
   def validate_for_itinerary(
         cls,
         guardians_talks_to_include: list[ ItineraryGuardiansTalkInput ] | None,
         day_schedule: list[ GuardiansTalk ] ) -> list[ GuardiansTalkDiff ]:
      diffs: list[ GuardiansTalkDiff ] = []

      for talk_input in guardians_talks_to_include or []:
         talk = GuardiansTalkDayScheduleFinder.find_on_day_schedule(
            day_schedule,
            talk_input.name,
            start_time=talk_input.start_time,
            enclosure_name=talk_input.enclosure_name )
         name = talk.name if talk is not None else talk_input.name

         diffs.append(
            cls.build_diff_for_visit_day(
               name,
               talk,
               start_time_override=talk_input.start_time,
               end_time_override=talk_input.end_time,
               enclosure_name=talk_input.enclosure_name )
         )

      return diffs
