from __future__ import annotations

from ...itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from ...itinerary.data_access.itinerary_name_key_builder import ItineraryNameKeyBuilder
from ...models import GuardiansTalk


class ItineraryGuardiansTalksBuilder():
   @classmethod
   def build(
         cls,
         guardians_talks: list[ GuardiansTalk ],
         saved_guardians_talks: list[ ItineraryGuardiansTalkRecord ] ) -> list[ GuardiansTalk ]:
      saved_talk_by_key = {
         (
            saved_talk.name_key(),
            saved_talk.enclosure_name,
            saved_talk.location,
         ): saved_talk
         for saved_talk in saved_guardians_talks
      }

      for guardians_talk in guardians_talks:
         saved_talk = cls._saved_talk_for(
            saved_talk_by_key,
            guardians_talk )

         if saved_talk is None:
            continue

         guardians_talk.start_time = saved_talk.start_time
         guardians_talk.end_time = saved_talk.end_time
         guardians_talk.is_deleted = saved_talk.is_deleted

      guardians_talks.sort(
         key=lambda talk: (
            talk.name.lower(),
            talk.start_time or '',
         )
      )

      return guardians_talks


   @classmethod
   def _saved_talk_for(
         cls,
         saved_by_key: dict[ tuple[ str, str, str ], ItineraryGuardiansTalkRecord ],
         guardians_talk: GuardiansTalk ) -> ItineraryGuardiansTalkRecord | None:
      name_key = ItineraryNameKeyBuilder.build( guardians_talk.name )
      saved_talk = saved_by_key.get(
         ( name_key, guardians_talk.enclosure_name, guardians_talk.location ) )

      if saved_talk is not None:
         return saved_talk

      return saved_by_key.get( ( name_key, guardians_talk.enclosure_name, '' ) )
