from __future__ import annotations

from ..data_access.itinerary_save_input import ItinerarySaveInput
from ..data_access.saved_itinerary import SavedItinerary
from ...types import ScheduleTimeKey


class FixedZooScheduleStartTimesBuilder():
   @classmethod
   def from_saved_itinerary(
         cls,
         saved_itinerary: SavedItinerary | None ) -> list[ ScheduleTimeKey ]:
      if saved_itinerary is None:
         return []

      start_times: list[ ScheduleTimeKey ] = []

      for talk in saved_itinerary.guardians_talk_rows:
         if talk.is_deleted or talk.start_time is None:
            continue

         start_times.append( talk.start_time )

      for encounter in saved_itinerary.wild_encounter_rows:
         if encounter.is_deleted or encounter.start_time is None:
            continue

         start_times.append( encounter.start_time )

      return start_times


   @classmethod
   def from_save_input(
         cls,
         save_input: ItinerarySaveInput ) -> list[ ScheduleTimeKey ]:
      start_times: list[ ScheduleTimeKey ] = []

      for talk in save_input.guardians_talks:
         if talk.start_time is None:
            continue

         start_times.append( talk.start_time )

      for encounter in save_input.wild_encounters:
         if encounter.start_time is None:
            continue

         start_times.append( encounter.start_time )

      return start_times


   @classmethod
   def merge(
         cls,
         *groups: list[ ScheduleTimeKey ] ) -> list[ ScheduleTimeKey ]:
      merged: list[ ScheduleTimeKey ] = []

      for group in groups:
         merged.extend( group )

      return merged
