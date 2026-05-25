from __future__ import annotations

from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ...shared.date_values import DateValues
from ...shared.strings import SharedStrings
from ...types import ScheduledItem, ScheduleTimeKey


def schedule_time_range(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
) -> tuple[ int, int ]:
   start = DateValues.time_value_in_minutes( start_time )
   end = DateValues.time_value_in_minutes( end_time )

   return ( start, end )


def trim_range_against_blocker(
      start: int,
      end: int,
      blocker_start: int,
      blocker_end: int,
) -> tuple[ int, int ]:
   if blocker_end <= start or blocker_start >= end:
      return ( start, end )

   if blocker_start <= start and blocker_end >= end:
      raise ValueError(
         SharedStrings.Itinerary.guardians_talk_fully_covered_by_blocker() )

   if blocker_start <= start and blocker_end < end:
      return ( blocker_end, end )

   if blocker_start > start and blocker_end >= end:
      return ( start, blocker_start )

   if blocker_start > start and blocker_end < end:
      return ( blocker_end, end )

   raise ValueError(
      SharedStrings.Itinerary.guardians_talk_unexpected_blocker_overlap() )


def trim_guardians_talk_times(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      blockers: list[ ScheduledItem ],
) -> tuple[ ScheduleTimeKey, ScheduleTimeKey ]:
   start, end = schedule_time_range( start_time, end_time )

   for blocker in blockers:
      blocker_start, blocker_end = schedule_time_range(
         blocker.start_time,
         blocker.end_time )

      start, end = trim_range_against_blocker(
         start,
         end,
         blocker_start,
         blocker_end,
      )

   if start >= end:
      raise ValueError(
         SharedStrings.Itinerary.guardians_talk_no_remaining_time_after_trimming() )

   return (
      DateValues.schedule_time_key_from_minutes( start ),
      DateValues.schedule_time_key_from_minutes( end ),
   )


def active_blockers(
      scheduled_items: list[ ScheduledItem ],
) -> list[ ScheduledItem ]:
   return [
      scheduled_item
      for scheduled_item in scheduled_items
      if not scheduled_item.is_deleted
   ]


def apply_guardians_talk_trimming(
      guardians_talks: list[ GuardiansTalkDiff ],
      wild_encounters: list[ WildEncounterDiff ],
) -> list[ GuardiansTalkDiff ]:
   encounter_blockers = active_blockers( wild_encounters )
   trimmed_talks: list[ GuardiansTalkDiff ] = []
   talk_blockers: list[ GuardiansTalkDiff ] = []

   for guardians_talk in guardians_talks:
      if guardians_talk.is_deleted:
         trimmed_talks.append( guardians_talk )
         continue

      blockers = [
         *encounter_blockers,
         *talk_blockers,
      ]
      trimmed_start_time, trimmed_end_time = trim_guardians_talk_times(
         guardians_talk.start_time,
         guardians_talk.end_time,
         blockers )

      trimmed_talk = GuardiansTalkDiff(
         name=guardians_talk.name,
         is_deleted=guardians_talk.is_deleted,
         start_time=trimmed_start_time,
         end_time=trimmed_end_time,
         location=guardians_talk.location,
      )
      trimmed_talks.append( trimmed_talk )
      talk_blockers.append( trimmed_talk )

   return trimmed_talks
