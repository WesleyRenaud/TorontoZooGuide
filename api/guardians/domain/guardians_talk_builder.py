from __future__ import annotations

from ..data_access.meet_the_guardians_talk_record import MeetTheGuardiansTalkRecord
from .guardians_talk_include_filter import GuardiansTalkIncludeFilter
from ...models import GuardiansTalk


class GuardiansTalkBuilder():
   @classmethod
   def _record_to_model( cls, record: MeetTheGuardiansTalkRecord ) -> GuardiansTalk:
      return GuardiansTalk(
         name=record.name,
         location=record.location,
         x_coord=record.x_coord,
         y_coord=record.y_coord,
         maximum_duration=record.maximum_duration )


   @classmethod
   def build_details(
         cls,
         talk_records: list[ MeetTheGuardiansTalkRecord ],
         guardians_talks_to_include: list[ str ] | None = None ) -> list[ GuardiansTalk ]:
      include_filter = GuardiansTalkIncludeFilter.from_optional_list(
         guardians_talks_to_include )

      if include_filter.should_return_empty():
         return []

      talks: list[ GuardiansTalk ] = []

      for record in talk_records:
         if not include_filter.allows_talk_name( record.name ):
            continue

         talks.append( cls._record_to_model( record ) )

      talks.sort(
         key=lambda t: (
            ( t.name or '' ).lower(),
            ( t.location or '' ).lower()
         )
      )

      return talks
