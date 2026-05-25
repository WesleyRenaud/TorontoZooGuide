from __future__ import annotations

from .guardians_talk_schedule import find_guardians_talk_on_day_schedule
from ...itinerary.data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from ...models import GuardiansTalk
from ...models import GuardiansTalkDiff
from ...shared.date_values import DateValues
from ...types import ScheduleTimeKey


def build_guardians_talk_diff_for_visit_day(
      name: str,
      talk: GuardiansTalk | None,
      *,
      start_time_override: ScheduleTimeKey = None,
      end_time_override: ScheduleTimeKey = None ) -> GuardiansTalkDiff:
   if talk is None:
      return GuardiansTalkDiff(
         name=name,
         is_deleted=True,
         start_time=None,
         end_time=None,
      )

   scheduled_end_time = DateValues.add_minutes_to_time(
      talk.start_time,
      talk.maximum_duration )

   return GuardiansTalkDiff(
      name=name,
      is_deleted=False,
      start_time=start_time_override or talk.start_time,
      end_time=end_time_override or scheduled_end_time,
      location=talk.location,
   )


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
