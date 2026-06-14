from __future__ import annotations

from ...itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from ...itinerary.scheduling import schedule_guardians_talk_for_itinerary
from ...models import GuardiansTalk
from ...models import GuardiansTalkDiff
from ..scheduling.guardians_talk_schedule import find_guardians_talk_on_day_schedule
from ...types import ScheduleTimeKey


def build_guardians_talk_diff_for_visit_day(
      name: str,
      talk: GuardiansTalk | None,
      *,
      start_time_override: ScheduleTimeKey = None,
      end_time_override: ScheduleTimeKey = None ) -> GuardiansTalkDiff:
   return schedule_guardians_talk_for_itinerary(
      name,
      talk,
      start_time_override=start_time_override,
      end_time_override=end_time_override )


def validate_guardians_talks_for_itinerary(
      guardians_talks_to_include: list[ ItineraryGuardiansTalkInput ] | None,
      day_schedule: list[ GuardiansTalk ] ) -> list[ GuardiansTalkDiff ]:

   diffs: list[ GuardiansTalkDiff ] = []

   for talk_input in guardians_talks_to_include or []:
      talk = find_guardians_talk_on_day_schedule(
         day_schedule,
         talk_input.name )
      name = talk.name if talk is not None else talk_input.name

      diffs.append(
         build_guardians_talk_diff_for_visit_day(
            name,
            talk,
            start_time_override=talk_input.start_time,
            end_time_override=talk_input.end_time )
      )

   return diffs
