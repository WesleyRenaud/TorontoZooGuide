from __future__ import annotations

from ...itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from ...itinerary.data_access.itinerary_name_key import itinerary_name_key
from ...models import GuardiansTalk


def build_itinerary_guardians_talks(
      guardians_talks: list[ GuardiansTalk ],
      saved_guardians_talks: list[ ItineraryGuardiansTalkRecord ] ) -> list[ GuardiansTalk ]:
   guardians_talk_by_name = {
      saved_talk.name_key(): saved_talk
      for saved_talk in saved_guardians_talks
   }

   for guardians_talk in guardians_talks:
      saved_talk = guardians_talk_by_name.get(
         itinerary_name_key( guardians_talk.name ) )

      if saved_talk == None:
         continue

      guardians_talk.start_time = saved_talk.start_time
      guardians_talk.end_time = saved_talk.end_time
      guardians_talk.is_deleted = saved_talk.is_deleted

   guardians_talks.sort(
      key=lambda talk: (
         ( talk.name or '' ).lower(),
         talk.start_time or ''
      )
   )

   return guardians_talks
