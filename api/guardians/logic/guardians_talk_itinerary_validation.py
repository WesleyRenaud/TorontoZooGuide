from __future__ import annotations

from ... import zoo
from .guardians_talk_schedule import find_guardians_talk_on_day_schedule


def build_guardians_talk_diff_for_visit_day(
      name: str,
      talk: zoo.GuardiansTalk | None ) -> zoo.GuardiansTalkDiff:
   if talk is None:
      return zoo.GuardiansTalkDiff(
         name=name,
         is_deleted=True,
         start_time=None,
         end_time=None,
      )

   end_time = zoo.ZooUtil.add_minutes_to_time(
      talk.start_time,
      talk.maximum_duration )

   return zoo.GuardiansTalkDiff(
      name=name,
      is_deleted=False,
      start_time=talk.start_time,
      end_time=end_time,
   )


def validate_guardians_talks_for_itinerary(
      guardians_talks_to_include: list[ str ] | None,
      day_schedule: list[ zoo.GuardiansTalk ] ) -> list[ zoo.GuardiansTalkDiff ]:

   diffs: list[ zoo.GuardiansTalkDiff ] = []

   for talk_name in guardians_talks_to_include or []:
      talk = find_guardians_talk_on_day_schedule(
         day_schedule,
         talk_name )
      name = talk.name if talk is not None else talk_name

      diffs.append(
         build_guardians_talk_diff_for_visit_day( name, talk )
      )

   return diffs
