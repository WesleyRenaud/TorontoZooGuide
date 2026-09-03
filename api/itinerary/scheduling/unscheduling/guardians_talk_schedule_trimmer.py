from __future__ import annotations

from ....app_string_provider import AppStringProvider
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ....models.wild_encounter_diff import WildEncounterDiff
from ....scheduled_item import ScheduledItem
from ....shared.calendar_dates import DateValues
from ....types import Types


class GuardiansTalkScheduleTrimmer():
   @classmethod
   def time_range_minutes(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> tuple[ int, int ]:
      start = DateValues.time_value_in_minutes( start_time )
      end = DateValues.time_value_in_minutes( end_time )

      return ( start, end )


   @classmethod
   def trim_range_against_blocker(
         cls,
         start: int,
         end: int,
         blocker_start: int,
         blocker_end: int ) -> tuple[ int, int ]:
      if blocker_end <= start or blocker_start >= end:
         return ( start, end )

      if blocker_start <= start and blocker_end >= end:
         raise ValueError(
            AppStringProvider.format( 'guestStatus.itinerary.guardiansTalkFullyCoveredByBlocker' ) )

      if blocker_start <= start and blocker_end < end:
         return ( blocker_end, end )

      if blocker_start > start and blocker_end >= end:
         return ( start, blocker_start )

      if blocker_start > start and blocker_end < end:
         return ( blocker_end, end )


   @classmethod
   def trim_times(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey,
         blockers: list[ ScheduledItem.Item ] ) -> tuple[ Types.ScheduleTimeKey, Types.ScheduleTimeKey ]:
      start, end = cls.time_range_minutes( start_time, end_time )

      for blocker in blockers:
         blocker_start, blocker_end = cls.time_range_minutes(
            blocker.start_time,
            blocker.end_time )

         start, end = cls.trim_range_against_blocker(
            start,
            end,
            blocker_start,
            blocker_end,
         )

      if start >= end:
         raise ValueError(
            AppStringProvider.format( 'guestStatus.itinerary.guardiansTalkNoRemainingTimeAfterTrimming' ) )

      return (
         DateValues.schedule_time_key_from_minutes( start ),
         DateValues.schedule_time_key_from_minutes( end ),
      )


   @classmethod
   def active_blockers(
         cls,
         scheduled_items: list[ ScheduledItem.Item ] ) -> list[ ScheduledItem.Item ]:
      return [
         scheduled_item
         for scheduled_item in scheduled_items
         if not scheduled_item.is_deleted
      ]


   @classmethod
   def apply(
         cls,
         guardians_talks: list[ GuardiansTalkDiff ],
         wild_encounters: list[ WildEncounterDiff ] ) -> list[ GuardiansTalkDiff ]:
      encounter_blockers = cls.active_blockers( wild_encounters )
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
         trimmed_start_time, trimmed_end_time = cls.trim_times(
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
