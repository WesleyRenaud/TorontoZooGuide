from __future__ import annotations

from ....models import GuardiansTalk
from ....models import GuardiansTalkDiff
from ....models import WildEncounter
from ....models import WildEncounterDiff
from ....shared.calendar_dates import DateValues
from ....types import ScheduleTimeKey


def schedule_guardians_talk_for_itinerary(
      name: str,
      talk: GuardiansTalk | None,
      *,
      start_time_override: ScheduleTimeKey = None,
      end_time_override: ScheduleTimeKey = None ) -> GuardiansTalkDiff:
   if talk is None:
      return GuardiansTalkDiff(
         name=name,
         is_deleted=True,
         start_time=start_time_override,
         end_time=end_time_override )

   scheduled_end_time = DateValues.add_minutes_to_time(
      talk.start_time,
      talk.maximum_duration )

   return GuardiansTalkDiff(
      name=name,
      is_deleted=False,
      start_time=start_time_override or talk.start_time,
      end_time=end_time_override or scheduled_end_time,
      location=talk.location )


def schedule_wild_encounter_for_itinerary(
      name: str,
      encounter: WildEncounter | None,
      *,
      start_time_override: ScheduleTimeKey = None,
      end_time_override: ScheduleTimeKey = None ) -> WildEncounterDiff:
   if encounter is None:
      return WildEncounterDiff(
         name=name,
         is_deleted=True,
         start_time=start_time_override,
         end_time=end_time_override )

   scheduled_end_time = DateValues.add_minutes_to_time(
      encounter.start_time,
      encounter.maximum_duration )

   return WildEncounterDiff(
      name=name,
      is_deleted=not encounter.is_available,
      start_time=start_time_override or encounter.start_time,
      end_time=end_time_override or scheduled_end_time,
      meeting_spot=encounter.meeting_spot,
      link=encounter.link )
